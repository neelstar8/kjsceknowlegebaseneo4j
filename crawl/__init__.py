"""Shared crawl infrastructure for the official KJSCE site.

Three modules, deliberately small:

    site_urls.py   canonicalise a URL, derive a stable resource id, classify a host
    fetcher.py     one rate-limited HTTP layer with backoff, disk cache and conditional GET
    manifest.py    the append-only crawl log that makes a run resumable and coverage countable

Nothing here knows about Neo4j. Discovery and processing write JSON artifacts; the
ingest stage reads them. That is the same discover -> normalize -> validate -> ingest
rhythm the faculty, PYQ and policy pipelines already follow.
"""
