import io
import logging
import functools
from typing import List, Dict, Any, Optional, Union
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .auth import get_credentials

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DriveClient:
    def __init__(self):
        self.creds = get_credentials()
        self.service = build('drive', 'v3', credentials=self.creds)

    @functools.lru_cache(maxsize=128)
    def _cached_list_files(self, q: str, limit: int) -> List[Dict[str, Any]]:
        """Internal cached method for listing files."""
        results = self.service.files().list(
            q=q,
            pageSize=limit,
            fields="nextPageToken, files(id, name, mimeType, parents, owners, modifiedTime, webViewLink, size)"
        ).execute()
        return results.get('files', [])

    @retry(
        retry=retry_if_exception_type(HttpError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def list_files(self, query: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Lists files with retry logic.
        """
        try:
            # Default query to not show trashed files if no query provided
            if not query:
                q = "trashed = false"
            else:
                q = f"({query}) and trashed = false"

            return self._cached_list_files(q, limit)
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            raise

    @functools.lru_cache(maxsize=256)
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """Get detailed metadata for a file."""
        return self.service.files().get(
            fileId=file_id,
            fields="id, name, mimeType, parents, owners, modifiedTime, webViewLink, size, exportLinks"
        ).execute()

    def download_file(self, file_id: str, export_mime_type: Optional[str] = None) -> bytes:
        """
        Downloads a file's content.
        Handles binary downloads and Google Workspace document exports.
        """
        try:
            meta = self.get_file_metadata(file_id)
            mime_type = meta.get('mimeType')

            # Handle Google Workspace documents (Docs, Sheets, Slides)
            if mime_type == 'application/vnd.google-apps.document':
                # Default to text/plain if requested or for general text-based use
                target_mime = export_mime_type or 'application/pdf'
                request = self.service.files().export_media(fileId=file_id, mimeType=target_mime)
            elif mime_type == 'application/vnd.google-apps.spreadsheet':
                target_mime = export_mime_type or 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                request = self.service.files().export_media(fileId=file_id, mimeType=target_mime)
            elif mime_type == 'application/vnd.google-apps.presentation':
                target_mime = export_mime_type or 'application/pdf'
                request = self.service.files().export_media(fileId=file_id, mimeType=target_mime)
            else:
                # Standard binary download
                request = self.service.files().get_media(fileId=file_id)

            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            return file_io.getvalue()
        except HttpError as error:
            logger.error(f"Error downloading file {file_id}: {error}")
            raise

    def create_folder(self, name: str, parent_id: str = 'root') -> Dict[str, Any]:
        """Create a new folder."""
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        return self.service.files().create(body=file_metadata, fields='id, name, webViewLink').execute()

    def upload_file(self, name: str, content: Union[str, bytes], parent_id: str = 'root', mime_type: str = 'text/plain') -> Dict[str, Any]:
        """Upload a file."""
        file_metadata = {
            'name': name,
            'parents': [parent_id]
        }
        
        if isinstance(content, str):
            content_bytes = io.BytesIO(content.encode('utf-8'))
        else:
            content_bytes = io.BytesIO(content)

        # Use MediaIoBaseUpload for in-memory bytes
        from googleapiclient.http import MediaIoBaseUpload
        media = MediaIoBaseUpload(content_bytes, mimetype=mime_type, resumable=True)

        return self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()

    def trash_file(self, file_id: str) -> Dict[str, Any]:
        """Move a file to trash."""
        body = {'trashed': True}
        return self.service.files().update(fileId=file_id, body=body).execute()

    def list_folder_children(self, folder_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """List all children of a specific folder."""
        query = f"'{folder_id}' in parents"
        return self.list_files(query=query, limit=limit)

    def search(self, text: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Perform a semantic/name search."""
        # Simple name contains search for now, can be expanded
        query = f"name contains '{text}'"
        return self.list_files(query=query, limit=limit)
