"""One rate-limited HTTP layer for the whole crawl.

The repo had two independent scrapers with different retry rules and no cache; this
consolidates their good parts and closes the gaps that matter for a crawl this size:

  * Retry/backoff is `scraper/somaiya_faculty.py::_request`'s shape, with the jitter
    from `drive/client.py::_execute` added. Jitter matters here because the failure
    actually observed on this host was a TCP reset after a burst -- retrying a burst
    on a fixed schedule just re-creates the burst.
  * `ConnectionResetError` is treated as retryable. The default `requests` behaviour
    is to raise it straight through, which would strand a resource that a second
    attempt would have fetched.
  * Per-host pacing rather than one global delay, so a slow CDN never starves the
    page crawl and vice versa.
  * A disk cache with a real skip path, including conditional GET. The existing
    policy discovery re-downloads every PDF on every run; at this scale that would be
    both rude and slow.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
import urllib.parse as up

import requests

from crawl.site_urls import canonical_url

CACHE_DIR = "data/crawl/cache"

# Deliberately slower than the faculty scraper's 1.0s: this host has already reset a
# connection on us, and nothing here is urgent.
REQUEST_DELAY = 1.5
PAGE_TIMEOUT = 30
DOC_TIMEOUT = 90
MAX_RETRIES = 4
BACKOFF_BASE = 2.0
HTML_CACHE_TTL = 7 * 24 * 3600      # pages change; documents are keyed by checksum

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

RETRYABLE_STATUS = {429, 500, 502, 503, 504, 520, 521, 522, 524}


class FetchError(RuntimeError):
    """Raised when a URL could not be fetched after every retry."""


_last_request_at: dict[str, float] = {}
_session: requests.Session | None = None


def get_session() -> requests.Session:
    global _session
    if _session is None:
        s = requests.Session()
        s.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        })
        _session = s
    return _session


def close_session() -> None:
    global _session
    if _session is not None:
        _session.close()
        _session = None


def _pace(host: str) -> None:
    """Hold at least REQUEST_DELAY between two requests to the same host."""
    last = _last_request_at.get(host)
    if last is not None:
        wait = REQUEST_DELAY - (time.monotonic() - last)
        if wait > 0:
            time.sleep(wait)
    _last_request_at[host] = time.monotonic()


def _cache_paths(url: str) -> tuple[str, str]:
    digest = hashlib.sha1(canonical_url(url).encode("utf-8")).hexdigest()
    body = os.path.join(CACHE_DIR, digest[:2], digest + ".bin")
    meta = os.path.join(CACHE_DIR, digest[:2], digest + ".meta.json")
    return body, meta


def read_cache(url: str) -> tuple[bytes | None, dict]:
    body_path, meta_path = _cache_paths(url)
    if not (os.path.exists(body_path) and os.path.exists(meta_path)):
        return None, {}
    try:
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
        with open(body_path, "rb") as fh:
            return fh.read(), meta
    except (OSError, json.JSONDecodeError):
        return None, {}


def write_cache(url: str, content: bytes, meta: dict) -> str:
    body_path, meta_path = _cache_paths(url)
    os.makedirs(os.path.dirname(body_path), exist_ok=True)
    with open(body_path, "wb") as fh:
        fh.write(content)
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh)
    return body_path


def _request(method: str, url: str, *, timeout: int, headers: dict | None = None,
             data=None) -> requests.Response:
    """Retry 5xx/429 and connection resets with jittered exponential backoff."""
    host = up.urlsplit(url).netloc.lower()
    session = get_session()
    last_error = None

    for attempt in range(MAX_RETRIES):
        _pace(host)
        try:
            resp = session.request(method, url, timeout=timeout,
                                   headers=headers, data=data, allow_redirects=True)
            if resp.status_code in RETRYABLE_STATUS:
                last_error = f"HTTP {resp.status_code}"
            else:
                return resp
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError) as e:
            # The reset this host actually produces surfaces as ConnectionError.
            last_error = f"{type(e).__name__}: {e}"
        except requests.RequestException as e:
            last_error = f"{type(e).__name__}: {e}"

        if attempt < MAX_RETRIES - 1:
            time.sleep((BACKOFF_BASE ** attempt) + random.uniform(0, 1))

    raise FetchError(f"{url} failed after {MAX_RETRIES} attempts: {last_error}")


def fetch(url: str, *, is_document: bool = False, use_cache: bool = True) -> dict:
    """Fetch one URL, preferring the cache and revalidating when possible.

    Returns a dict with `content`, `sha256`, `from_cache`, `status`, `etag`,
    `last_modified`, `content_type`, `bytes` and `cache_path`. Raises FetchError.
    """
    canon = canonical_url(url)
    if not canon:
        raise FetchError(f"not a fetchable URL: {url!r}")

    cached, meta = read_cache(canon) if use_cache else (None, {})

    if cached is not None:
        fresh_enough = (
            is_document                                    # keyed by checksum, not time
            or (time.time() - meta.get("fetched_at_epoch", 0)) < HTML_CACHE_TTL
        )
        if fresh_enough and not (meta.get("etag") or meta.get("last_modified")):
            return {**meta, "content": cached, "from_cache": True,
                    "cache_path": _cache_paths(canon)[0]}

    headers = {}
    if cached is not None and meta.get("etag"):
        headers["If-None-Match"] = meta["etag"]
    if cached is not None and meta.get("last_modified"):
        headers["If-Modified-Since"] = meta["last_modified"]

    timeout = DOC_TIMEOUT if is_document else PAGE_TIMEOUT
    resp = _request("GET", canon, timeout=timeout, headers=headers or None)

    if resp.status_code == 304 and cached is not None:
        return {**meta, "content": cached, "from_cache": True, "status": 304,
                "cache_path": _cache_paths(canon)[0]}

    if resp.status_code >= 400:
        raise FetchError(f"{canon} returned HTTP {resp.status_code}")

    content = resp.content
    new_meta = {
        "status": resp.status_code,
        "content_type": (resp.headers.get("Content-Type") or "").split(";")[0].strip(),
        "etag": resp.headers.get("ETag"),
        "last_modified": resp.headers.get("Last-Modified"),
        "sha256": hashlib.sha256(content).hexdigest(),
        "bytes": len(content),
        "fetched_at_epoch": time.time(),
        "final_url": resp.url,
    }
    cache_path = write_cache(canon, content, new_meta) if use_cache else None
    return {**new_meta, "content": content, "from_cache": False,
            "cache_path": cache_path}


def post_form(url: str, data: str | dict, *, referer: str | None = None) -> str:
    """POST a form body and return text. Used for the documents AJAX endpoint."""
    headers = {"X-Requested-With": "XMLHttpRequest",
               "Content-Type": "application/x-www-form-urlencoded"}
    if referer:
        headers["Referer"] = referer
    resp = _request("POST", url, timeout=PAGE_TIMEOUT, headers=headers, data=data)
    if resp.status_code >= 400:
        raise FetchError(f"{url} returned HTTP {resp.status_code}")
    return resp.text


def looks_like_pdf(content: bytes) -> bool:
    return content[:4] == b"%PDF"
