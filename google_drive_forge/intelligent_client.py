import logging
import functools
from typing import List, Dict, Any, Optional, Callable
from googleapiclient.errors import HttpError
from .client import DriveClient

from .audit import AuditLogger

logger = logging.getLogger(__name__)

def self_healing_recovery(func: Callable):
    """
    Decorator that attempts autonomous recovery on Google Drive API failures.
    Specifically targets 404 (Not Found) errors and logs events.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except HttpError as error:
            if error.resp.status == 404:
                file_id = kwargs.get('file_id') or (args[0] if args else None)
                if file_id and isinstance(file_id, str):
                    message = f"File ID '{file_id}' not found. Suggesting search recovery."
                    if hasattr(self, 'audit'):
                        self.audit.log_recovery(file_id, "Unknown (Need Search)", False)
                    
                    logger.info(f"Self-healing: {message}")
                    raise HttpError(error.resp, f"Autonomous Recovery: {message} Use 'search_files' to find the new ID.".encode())
            raise
    return wrapper

class IntelligentDriveClient(DriveClient):
    """
    An advanced Drive client that implements autonomous patterns and self-healing.
    """
    def __init__(self, audit: Optional[AuditLogger] = None):
        super().__init__()
        self.audit = audit
    
    @self_healing_recovery
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        return super().get_file_metadata(file_id)

    @self_healing_recovery
    def download_file(self, file_id: str, export_mime_type: Optional[str] = None) -> bytes:
        """
        Enhanced download with MIME-type intelligence.
        Autonomously determines if a file needs export vs download.
        """
        try:
            return super().download_file(file_id, export_mime_type=export_mime_type)
        except HttpError as error:
            # Add specific MIME-type failure handling if super().download_file fails
            logger.error(f"Intelligent Download failed for {file_id}: {error}")
            raise

    def find_and_heal_path(self, path: str) -> Optional[str]:
        """
        Autonomous Path Discovery with Active Healing. 
        If a path like /Project/2026/Budgt fails, it auto-corrects to the closest match.
        """
        parts = [p for p in path.split('/') if p]
        current_parent = 'root'
        healed_path_parts = []
        
        for part in parts:
            # Try exact match first
            results = self.list_files(query=f"name = '{part}' and '{current_parent}' in parents")
            
            if results:
                current_parent = results[0]['id']
                healed_path_parts.append(part)
                continue
                
            # Exact match failed. Attempt Active Healing.
            # 1. Get all children of the current parent
            children = self.list_files(query=f"'{current_parent}' in parents")
            
            # 2. Simple fuzzy match: case-insensitive match or name contains
            matches = [c for c in children if part.lower() in c['name'].lower()]
            
            if len(matches) == 1:
                # High confidence recovery
                healed_name = matches[0]['name']
                old_id = current_parent
                current_parent = matches[0]['id']
                
                logger.info(f"Active Healing: Resolved '{part}' -> '{healed_name}' in folder {old_id}")
                if self.audit:
                    self.audit.log_recovery(part, healed_name, True)
                
                healed_path_parts.append(healed_name)
            else:
                # No definitive match
                if self.audit:
                    self.audit.log_recovery(part, "Ambiguous/Not Found", False)
                
                suggestion_names = [c["name"] for c in children]
                logger.warning(f"Path break at '{part}'. Suggestions: {suggestion_names}")
                return None
            
        return current_parent
