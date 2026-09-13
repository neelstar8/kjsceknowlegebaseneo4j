"""Owns the Google Drive connection. Read-only, and nothing Neo4j-related lives here.

Deliberately shaped like graph/neo4j_driver.py: a module-level singleton, a
verify_connection() that raises a human-readable error naming the exact missing
piece of config, and plain functions on top.

The credential is a service account scoped to drive.readonly, so this code
physically cannot modify the source Drive no matter what goes wrong.
"""
import os
import random
import time

from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "")
DRIVE_ROOT_FOLDER_ID = os.environ.get("PYQ_DRIVE_ROOT_FOLDER_ID", "")

FOLDER_MIME = "application/vnd.google-apps.folder"

# Everything we ask Drive for, in one place. Anything not listed here simply
# does not exist as far as the rest of the pipeline is concerned.
FILE_FIELDS = (
    "id, name, mimeType, size, webViewLink, parents, createdTime, modifiedTime"
)
LIST_FIELDS = f"nextPageToken, files({FILE_FIELDS})"

MAX_RETRIES = 5
RETRYABLE_STATUS = {403, 429, 500, 502, 503, 504}
# 403 is only retryable for these reasons -- a plain permission 403 must fail fast.
RETRYABLE_403_REASONS = {"rateLimitExceeded", "userRateLimitExceeded"}

_service = None


def get_service():
    global _service
    if _service is None:
        if not SERVICE_ACCOUNT_FILE:
            raise RuntimeError(
                "GOOGLE_SERVICE_ACCOUNT_FILE is not set. Add it to your .env file."
            )
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            raise RuntimeError(
                f"Service account key not found at {SERVICE_ACCOUNT_FILE}. "
                "Download the JSON key from the Google Cloud console and point "
                "GOOGLE_SERVICE_ACCOUNT_FILE at it."
            )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        _service = build("drive", "v3", credentials=credentials,
                         cache_discovery=False)
    return _service


def service_account_email() -> str | None:
    """The address the Drive folder has to be shared with. Used in error text."""
    if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
        return None
    import json

    with open(SERVICE_ACCOUNT_FILE, encoding="utf-8") as f:
        return json.load(f).get("client_email")


def _status_of(error) -> int | None:
    resp = getattr(error, "resp", None)
    status = getattr(resp, "status", None)
    return int(status) if status is not None else None


def _reasons_of(error) -> set[str]:
    """Drive puts the real cause in the JSON body, not the HTTP status."""
    import json

    try:
        body = json.loads(getattr(error, "content", b"") or b"{}")
    except (ValueError, TypeError):
        return set()
    errors = (body.get("error") or {}).get("errors") or []
    return {e.get("reason", "") for e in errors}


def _is_retryable(error) -> bool:
    status = _status_of(error)
    if status not in RETRYABLE_STATUS:
        return False
    if status == 403:
        return bool(_reasons_of(error) & RETRYABLE_403_REASONS)
    return True


def _execute(request):
    """Run a Drive request, backing off on rate limits and transient failures."""
    from googleapiclient.errors import HttpError

    for attempt in range(MAX_RETRIES):
        try:
            return request.execute()
        except HttpError as e:
            if not _is_retryable(e) or attempt == MAX_RETRIES - 1:
                raise
            # Exponential backoff with jitter, as Google's own guidance suggests.
            time.sleep((2 ** attempt) + random.uniform(0, 1))
    raise RuntimeError("unreachable")


def verify_connection(folder_id: str | None = None) -> bool:
    """Raises a clear error if Drive is unreachable or the folder isn't shared."""
    from googleapiclient.errors import HttpError

    folder_id = folder_id or DRIVE_ROOT_FOLDER_ID
    if not folder_id:
        raise RuntimeError(
            "PYQ_DRIVE_ROOT_FOLDER_ID is not set. Add it to your .env file."
        )
    try:
        get_service().files().get(
            fileId=folder_id, fields="id, name, mimeType",
            supportsAllDrives=True,
        ).execute()
        return True
    except HttpError as e:
        if _status_of(e) in (403, 404):
            email = service_account_email() or "the service account"
            raise RuntimeError(
                f"Drive folder {folder_id} is not readable by this credential. "
                f"Share the folder (Viewer is enough) with {email}."
            ) from e
        raise RuntimeError(f"Could not reach Google Drive: {e}") from e


def get_file(file_id: str) -> dict:
    return _execute(
        get_service().files().get(
            fileId=file_id, fields=FILE_FIELDS, supportsAllDrives=True
        )
    )


def list_children(folder_id: str) -> list[dict]:
    """Every non-trashed direct child of a folder, following all pages."""
    service = get_service()
    children, page_token = [], None
    while True:
        response = _execute(
            service.files().list(
                q=f"'{folder_id}' in parents and trashed = false",
                fields=LIST_FIELDS,
                pageSize=1000,
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
        )
        children.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return children


def walk_folder(root_id: str, root_name: str | None = None,
                exclude_ids: set[str] | None = None):
    """Breadth-first walk yielding every non-folder file under root_id.

    Each yielded record carries the folder chain it was found in, because for
    this corpus the path holds more reliable metadata than the file name does.

    Drive shortcuts can make the folder graph cyclic, so visited folder IDs are
    tracked -- without that this loops forever rather than failing.
    """
    if root_name is None:
        root_name = get_file(root_id).get("name", root_id)

    # The ESE collection lives in a subfolder of the ISE root, so an ISE re-walk
    # has to be told to leave it alone or it would sweep ESE files into the ISE
    # collection.
    visited: set[str] = set(exclude_ids or ())
    queue = [(root_id, [root_name], [root_id])]

    while queue:
        folder_id, path_names, path_ids = queue.pop(0)
        if folder_id in visited:
            continue
        visited.add(folder_id)

        for child in list_children(folder_id):
            if child.get("mimeType") == FOLDER_MIME:
                queue.append((
                    child["id"],
                    path_names + [child.get("name", child["id"])],
                    path_ids + [child["id"]],
                ))
                continue
            yield {
                "drive_file_id": child["id"],
                "file_name": child.get("name", ""),
                "mime_type": child.get("mimeType", ""),
                "file_size": int(child["size"]) if child.get("size") else None,
                "drive_url": child.get("webViewLink"),
                "parent_folder_id": folder_id,
                "parent_folder_name": path_names[-1],
                "folder_path": "/".join(path_names),
                "folder_path_ids": path_ids,
                "drive_created_time": child.get("createdTime"),
                "drive_modified_time": child.get("modifiedTime"),
            }


def download_file(file_id: str, max_bytes: int | None = None) -> bytes:
    """Fetch a file's bytes.

    Used only to LOOK INSIDE a semester bundle and find out which subjects it
    contains. The bytes are held in memory, read once, and dropped -- nothing
    downloaded here is ever written to disk or stored in Neo4j, which holds
    metadata and the Drive link only.
    """
    import io

    from googleapiclient.http import MediaIoBaseDownload

    buffer = io.BytesIO()
    request = get_service().files().get_media(fileId=file_id,
                                              supportsAllDrives=True)
    downloader = MediaIoBaseDownload(buffer, request, chunksize=1024 * 1024)
    done = False
    while not done:
        _, done = downloader.next_chunk()
        if max_bytes is not None and buffer.tell() > max_bytes:
            break
    return buffer.getvalue()


def close_service():
    global _service
    if _service is not None:
        _service.close()
        _service = None
