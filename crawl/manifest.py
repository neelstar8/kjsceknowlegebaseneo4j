"""The crawl manifest: an append-only event log that makes a run resumable.

Why events rather than one rewritten JSON file. The earlier pipelines in this repo
each write a single JSON blob per stage, which is fine when a stage is fast and
offline. This crawl is neither: it talks to a host that has already dropped a
connection mid-run. A blob rewritten in place is corrupt and unrecoverable if the
process dies during the write; an appended line that never finished is one bad
trailing line that replay simply ignores. So every state change is appended to
`data/crawl/manifest_events.jsonl`, and the current state of a resource is the fold
of its events.

Resume is therefore trivial and needs no separate checkpoint file: replay the log,
keep the newest event per resource, and carry on with everything that is not in a
terminal state. Because every downstream write is an idempotent MERGE on a stable
id, re-processing a row that was already ingested is harmless.
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone

DEFAULT_PATH = "data/crawl/manifest_events.jsonl"


class Status:
    # --- in flight -------------------------------------------------------
    DISCOVERED = "DISCOVERED"
    FETCHING = "FETCHING"
    FETCHED = "FETCHED"
    EXTRACTED = "EXTRACTED"
    RECONCILED = "RECONCILED"
    FETCH_FAILED = "FETCH_FAILED"          # retryable while attempts < MAX_ATTEMPTS
    NEEDS_REVIEW = "NEEDS_REVIEW"          # a human decides; never auto-ingested

    # --- terminal --------------------------------------------------------
    INGESTED = "INGESTED"                  # new node written
    REUSED = "REUSED"                      # matched an existing node; no duplicate made
    RECORDED = "RECORDED"                  # reference host: link kept, never downloaded
    SKIPPED_PII = "SKIPPED_PII"            # student list: refused, never fetched
    OUT_OF_SCOPE = "OUT_OF_SCOPE"          # excluded by scope rules, kept for audit
    PERMANENTLY_FAILED = "PERMANENTLY_FAILED"


#: Reaching any of these means the resource needs nothing further at all.
TERMINAL = {Status.INGESTED, Status.REUSED, Status.RECORDED, Status.SKIPPED_PII,
            Status.OUT_OF_SCOPE, Status.PERMANENTLY_FAILED}

#: States where the *crawl* has finished with a resource even though the graph has
#: not. EXTRACTED belongs here: the bytes are fetched, hashed and read, and the only
#: thing left is reconciliation. Without this, every `--process` pass would walk the
#: whole corpus again -- harmless thanks to the cache, but slow and misleading.
CRAWL_DONE = TERMINAL | {Status.EXTRACTED, Status.NEEDS_REVIEW}

#: States that count toward coverage. Every one is a deliberate, named outcome --
#: a PII document we refused on purpose is processed, not missing.
RESOLVED = {Status.INGESTED, Status.REUSED, Status.RECORDED, Status.SKIPPED_PII}

#: OUT_OF_SCOPE rows were never in the denominator, so they are reported separately
#: rather than counted as either success or failure.
EXCLUDED_FROM_COVERAGE = {Status.OUT_OF_SCOPE}

MAX_ATTEMPTS = 3


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Manifest:
    """Append-only event log, folded into current state on load."""

    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.rows: dict[str, dict] = {}
        self._seq = 0

    # ------------------------------------------------------------ load/save
    def load(self) -> "Manifest":
        """Replay the log. A truncated trailing line is ignored, not fatal."""
        self.rows, self._seq = {}, 0
        if not os.path.exists(self.path):
            return self
        bad = 0
        with open(self.path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    bad += 1          # only ever the last line, after a hard kill
                    continue
                rid = event.get("resource_id")
                if not rid:
                    continue
                self.rows.setdefault(rid, {}).update(event)
                self._seq = max(self._seq, event.get("seq", 0))
        self.truncated_lines = bad
        return self

    def _append(self, event: dict) -> dict:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        self._seq += 1
        event["seq"] = self._seq
        event["event_at"] = _now()
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())     # the line is on disk before we act on it
        self.rows.setdefault(event["resource_id"], {}).update(event)
        return self.rows[event["resource_id"]]

    # --------------------------------------------------------------- writes
    def discover(self, resource_id: str, **fields) -> dict:
        """Record a resource the crawl has seen. Idempotent: a second sighting only
        adds provenance, it never resets progress."""
        existing = self.rows.get(resource_id)
        if existing:
            seen = existing.get("discovered_via") or []
            new = fields.get("discovered_via") or []
            merged = seen + [v for v in new if v not in seen]
            if merged != seen:
                return self._append({"resource_id": resource_id,
                                     "status": existing.get("status"),
                                     "discovered_via": merged})
            return existing
        return self._append({"resource_id": resource_id,
                             "status": Status.DISCOVERED,
                             "attempts": 0, "first_seen_at": _now(), **fields})

    def update(self, resource_id: str, status: str, **fields) -> dict:
        return self._append({"resource_id": resource_id, "status": status, **fields})

    def fail(self, resource_id: str, error: str) -> dict:
        """Count an attempt; park the row once the cross-run budget is spent."""
        attempts = (self.rows.get(resource_id, {}).get("attempts") or 0) + 1
        status = Status.PERMANENTLY_FAILED if attempts >= MAX_ATTEMPTS else Status.FETCH_FAILED
        return self._append({"resource_id": resource_id, "status": status,
                             "attempts": attempts, "last_error": str(error)[:400]})

    # ---------------------------------------------------------------- reads
    def get(self, resource_id: str) -> dict | None:
        return self.rows.get(resource_id)

    def pending(self, *, kinds: set[str] | None = None) -> list[dict]:
        """Everything the crawl still has to fetch, failures last so fresh work goes first."""
        out = [r for r in self.rows.values()
               if r.get("status") not in CRAWL_DONE
               and (kinds is None or r.get("kind") in kinds)]
        out.sort(key=lambda r: (r.get("status") == Status.FETCH_FAILED, r.get("seq", 0)))
        return out

    def by_status(self) -> Counter:
        return Counter(r.get("status") for r in self.rows.values())

    def in_scope(self) -> list[dict]:
        return [r for r in self.rows.values()
                if r.get("status") not in EXCLUDED_FROM_COVERAGE]

    def coverage(self) -> dict:
        """Coverage against the frozen denominator.

        Only resources that reached a deliberate outcome count. Anything still
        pending or failed is excluded from the numerator and listed by name, so the
        percentage can never quietly hide unfinished work.
        """
        scoped = self.in_scope()
        total = len(scoped)
        resolved = [r for r in scoped if r.get("status") in RESOLVED]
        outstanding = [r for r in scoped if r.get("status") not in RESOLVED]
        pct = (len(resolved) / total * 100) if total else 0.0
        return {
            "total_in_scope": total,
            "resolved": len(resolved),
            "coverage_pct": round(pct, 2),
            "by_status": dict(self.by_status()),
            "outstanding": [
                {"resource_id": r.get("resource_id"),
                 "canonical_url": r.get("canonical_url"),
                 "status": r.get("status"),
                 "attempts": r.get("attempts", 0),
                 "last_error": r.get("last_error")}
                for r in outstanding
            ],
            "excluded_out_of_scope": sum(
                1 for r in self.rows.values()
                if r.get("status") in EXCLUDED_FROM_COVERAGE),
        }
