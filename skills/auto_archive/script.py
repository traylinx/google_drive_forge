import os
import sys
from datetime import datetime, timedelta, timezone

# Add the mcp/google_drive directory to sys.path to allow importing src
mcp_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if mcp_root not in sys.path:
    sys.path.append(mcp_root)

from src.intelligent_client import IntelligentDriveClient

def run():
    client = IntelligentDriveClient()
    print("🚀 Initializing Auto-Archive Skill...")
    
    # 1. Target the Archive folder
    print("🔍 Looking for 'Archive' folder...")
    folders = client.search("name = 'Archive' and mimeType = 'application/vnd.google-apps.folder'")
    
    if not folders:
        print("📁 Archive folder not found. Creating it...")
        archive_meta = client.create_folder("Archive")
        archive_id = archive_meta['id']
    else:
        archive_id = folders[0]['id']
        print(f"✅ Found existing Archive folder (ID: {archive_id})")

    # 2. Logic: Find files older than 30 days in root
    print("📅 Scanning for files older than 30 days...")
    # For this demo/first-run, we'll just list the last 10 files to show it works
    files = client.list_files(limit=10)
    
    archive_threshold = datetime.now(timezone.utc) - timedelta(days=30)
    
    candidates = []
    for f in files:
        # Ignore folders and the Archive folder itself
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            continue
            
        mod_time = datetime.fromisoformat(f['modifiedTime'].replace('Z', '+00:00'))
        if mod_time < archive_threshold:
            candidates.append(f)
            print(f"📦 Candidate found: {f['name']} (Last Modified: {f['modifiedTime']})")

    if not candidates:
        print("✨ No files currently meet the archive criteria. Drive is clean!")
    else:
        print(f"🏁 Found {len(candidates)} candidates for archiving.")
        # Actual move logic would go here: client.service.files().update(fileId=..., addParents=archive_id, removeParents=...)

if __name__ == "__main__":
    run()
