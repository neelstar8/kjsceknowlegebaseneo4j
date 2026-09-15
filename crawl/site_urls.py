"""URL canonicalisation, identity and host policy for the KJSCE crawl.

The repo had no URL canonicaliser at all before this -- every earlier scraper
compared raw URL strings -- which is why the same PDF could enter the graph twice
under two spellings. Everything downstream keys off `canonical_url()`.

Two traps this module exists to handle, both measured on the real site:

  1. `<loc>` values in sitemap.xml are XML-escaped: the file literally contains
     `...?type=research&amp;id=160120`. Fetching that verbatim asks the server for a
     parameter named `amp;id`, which is not the parameter the page wants. Anything
     entering this module is unescaped first.

  2. Query strings here are load-bearing. 149 of the 366 sitemap URLs carry one, and
     stripping them would merge 8 distinct `/admission/btech?vthmstablink=...` tabs
     into a single page. So params are KEPT and ordered, not dropped -- with a narrow
     deny-list for the handful that are provably tracking noise.
"""
from __future__ import annotations

import hashlib
import html
import re
import urllib.parse as up

# ---------------------------------------------------------------- host policy

# Downloaded and read in full.
KJ_DOWNLOAD_HOSTS = {
    "kjsce-files.somaiya.edu",
    "kjsse-files.somaiya.edu",
    "kjsce-old.somaiya.edu",
}

# Crawled as HTML: the college site itself.
KJ_SITE_HOSTS = {"kjsce.somaiya.edu"}

# Official Somaiya, but university-wide rather than engineering-college specific.
# Recorded with title and exact URL; never downloaded, never extracted.
REFERENCE_HOSTS = {
    "svu-files.somaiya.edu",
    "svv-files.somaiya.edu.in",
    "svu-admissions.somaiya.edu",
    "www.somaiya.edu",
    "somaiya.edu",
}

# Never fetched.
IGNORED_HOSTS = {
    "alumni.kjsim.somaiya.edu",
    "www.facebook.com", "facebook.com", "twitter.com", "x.com",
    "www.instagram.com", "instagram.com", "www.linkedin.com", "linkedin.com",
    "www.youtube.com", "youtube.com", "youtu.be",
}

IGNORED_SCHEMES = {"mailto", "tel", "javascript", "data", "ftp"}

# robots.txt Disallow entries, honoured even though the crawl scope would otherwise
# reach them.
ROBOTS_DISALLOW = ("/500245", "/710853", "/alumni.kjsim.somaiya.edu")

# Params that never change what a page returns. Everything else is preserved --
# see the module docstring for why that direction is the safe one here.
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid", "_ga", "phpsessid",
}

DOCUMENT_EXT_RE = re.compile(r"\.(pdf|docx?|xlsx?|pptx?)$", re.I)


class HostClass:
    SITE = "site"            # crawl as HTML
    DOWNLOAD = "download"    # fetch and read the document
    REFERENCE = "reference"  # record title + URL only
    IGNORE = "ignore"


def unescape(url: str) -> str:
    """Undo XML/HTML entity escaping.

    `&amp;` inside a sitemap `<loc>` is correct XML, not a typo -- but requesting it
    verbatim sends a parameter literally named `amp;id`.
    """
    return html.unescape((url or "").strip())


def canonical_url(url: str, base: str | None = None) -> str:
    """The comparison key for a URL. Stable, order-independent, entity-free.

    Resolves against `base` when relative, lowercases scheme and host, drops the
    fragment and any tracking parameter, sorts the remaining parameters, and
    normalises percent-encoding so `A+B` and `A%2BB` compare equal.

    Returns "" for anything that is not a fetchable http(s) URL.
    """
    raw = unescape(url)
    if not raw:
        return ""
    if base:
        raw = up.urljoin(unescape(base), raw)

    parts = up.urlsplit(raw)
    if parts.scheme.lower() in IGNORED_SCHEMES:
        return ""
    if parts.scheme.lower() not in ("http", "https"):
        return ""

    host = parts.netloc.lower()
    # Drop a default port so :443 and bare compare equal.
    if host.endswith(":80") or host.endswith(":443"):
        host = host.rsplit(":", 1)[0]

    # The Somaiya hosts serve the same bytes over http and https, and the site links
    # to both spellings of the same file. Left alone, one PDF becomes two resources
    # with two ids and two nodes -- which is exactly what happened to the NIRF 2025
    # Engineering report before this line existed.
    scheme = parts.scheme.lower()
    if scheme == "http" and host.endswith("somaiya.edu"):
        scheme = "https"

    # Re-encode the path consistently: unquote first so an already-encoded path is
    # not double-encoded, then quote the characters that must be escaped. `+` in a
    # path is a literal plus on these CDN hosts, so it is left intact.
    path = up.quote(up.unquote(parts.path), safe="/%+()&,'~!$*@=:;")

    keep = [(k, v) for k, v in up.parse_qsl(parts.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS]
    query = up.urlencode(sorted(keep), safe="+()")

    return up.urlunsplit((scheme, host, path, query, ""))


def resource_id(url: str, kind: str = "res") -> str:
    """Short, stable id derived from the canonical URL. The manifest's primary key."""
    canon = canonical_url(url) or unescape(url)
    digest = hashlib.sha1(canon.encode("utf-8")).hexdigest()[:16]
    return f"{kind}_{digest}"


def host_of(url: str) -> str:
    return up.urlsplit(canonical_url(url) or unescape(url)).netloc.lower()


def classify_host(url: str) -> str:
    """Decide what this crawl is allowed to do with a URL."""
    canon = canonical_url(url)
    if not canon:
        return HostClass.IGNORE
    parts = up.urlsplit(canon)
    host = parts.netloc.lower()

    if host in IGNORED_HOSTS:
        return HostClass.IGNORE
    if host in KJ_SITE_HOSTS:
        if any(parts.path.startswith(p) for p in ROBOTS_DISALLOW):
            return HostClass.IGNORE
        return HostClass.SITE
    if host in KJ_DOWNLOAD_HOSTS:
        return HostClass.DOWNLOAD
    if host in REFERENCE_HOSTS:
        return HostClass.REFERENCE
    # Unknown host: record the link, never fetch it.
    return HostClass.REFERENCE


def is_document(url: str) -> bool:
    """True when the URL points at a file rather than a page."""
    return bool(DOCUMENT_EXT_RE.search(up.urlsplit(canonical_url(url) or url).path))


def filename_of(url: str) -> str:
    """Human-readable filename from a URL, with `+` restored to spaces."""
    path = up.urlsplit(canonical_url(url) or unescape(url)).path
    return up.unquote(path.rsplit("/", 1)[-1]).replace("+", " ")


def section_of(url: str) -> str:
    """First meaningful path segment of a site page, e.g. 'documents', 'programme'."""
    parts = [p for p in up.urlsplit(canonical_url(url) or url).path.split("/") if p]
    if parts and parts[0] in ("en", "hi"):
        parts = parts[1:]
    return parts[0] if parts else "(root)"
