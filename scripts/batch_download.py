
import argparse
import os
import sys

# Add the mcp/google_drive directory to sys.path to import internal modules
mcp_dir = "/Users/sebastian/Projects/clis/antigravity/mcp/google_drive"
if mcp_dir not in sys.path:
    sys.path.append(mcp_dir)

from google_drive_mcp.intelligent_client import IntelligentDriveClient

def batch_download(folder_name, dest_path):
    client = IntelligentDriveClient()
    os.makedirs(dest_path, exist_ok=True)
    
    print(f"Searching for folder: {folder_name}...")
    results = client.list_files(query=f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'")
    
    if not results:
        print(f"Error: Folder '{folder_name}' not found.")
        return
    
    folder_id = results[0]['id']
    print(f"Found folder '{folder_name}' with ID: {folder_id}")
    
    print(f"Listing files in folder...")
    files = client.list_folder_children(folder_id)
    
    for f in files:
        file_name = f['name']
        file_id = f['id']
        mime_type = f['mimeType']
        
        if mime_type == 'application/vnd.google-apps.folder':
            print(f"Skipping subfolder: {file_name}")
            continue
            
        print(f"Processing: {file_name} ({mime_type})...")
        
        try:
            if mime_type == 'application/vnd.google-apps.document':
                # Export to plain text for MD
                content = client.download_file(file_id, export_mime_type='text/plain')
                file_extension = ".md"
            else:
                # Standard download
                content = client.download_file(file_id)
                # Keep original extension or use .bin if unknown
                _, ext = os.path.splitext(file_name)
                file_extension = ext or ".bin"
            
            # Ensure name doesn't have duplicate extension if we changed it
            base_name, _ = os.path.splitext(file_name)
            local_name = f"{base_name}{file_extension}"
            local_path = os.path.join(dest_path, local_name)
            
            with open(local_path, "wb") as out:
                out.write(content)
            print(f"  Saved to: {local_path}")
            
        except Exception as e:
            print(f"  Error processing {file_name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch download files from a Google Drive folder.")
    parser.add_argument("folder", help="Name of the Google Drive folder to download from")
    parser.add_argument("dest", help="Local destination directory")
    
    args = parser.parse_args()
    
    batch_download(args.folder, args.dest)
