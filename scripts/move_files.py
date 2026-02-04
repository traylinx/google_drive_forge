
import argparse
import logging
import sys
import os

# Add parent directory to sys.path to access src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google_drive_forge.intelligent_client import IntelligentDriveClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def move_files(source_name, dest_name, create_dest=False):
    client = IntelligentDriveClient()
    
    # 1. Find source files or folder
    print(f"Searching for source: '{source_name}'...")
    # Logic: If source is a folder, move its CONTENTS. If source is a file/pattern, move THE FILES.
    # For simplicity in this generic script, we'll assume source is a FOLDER and we move its contents.
    
    source_results = client.list_files(query=f"name = '{source_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
    
    if not source_results:
        print(f"Error: Source folder '{source_name}' not found. Cannot proceed.")
        return
    
    source_folder = source_results[0]
    source_id = source_folder['id']
    print(f"Found source folder: {source_folder['name']} (ID: {source_id})")
    
    # 2. Check for or create destination folder
    print(f"Searching for destination: '{dest_name}'...")
    
    # We look for destination folder ANYWHERE (or should we restrict?)
    # A generic move usually implies moving TO a specific target.
    dest_results = client.list_files(query=f"name = '{dest_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
    
    if dest_results:
        dest_folder = dest_results[0]
        dest_id = dest_folder['id']
        print(f"Found existing destination folder: {dest_folder['name']} (ID: {dest_id})")
    elif create_dest:
        print(f"Creating destination folder '{dest_name}' inside '{source_name}' (default behavior if parent not specified)...")
        # NOTE: If we want to create it elsewhere, we'd need a parent argument. 
        # For now, let's create it as a sibling of source? Or inside source?
        # If organizing, usually we want it INSIDE source (like 'archive').
        # Let's default to creating INSIDE source for safety, or asking user to be more specific.
        # Actually better: Create it in 'root' if not found? No, that's messy.
        # Let's create it inside the SOURCE folder as a subfolder.
        dest_folder = client.create_folder(name=dest_name, parent_id=source_id)
        dest_id = dest_folder['id']
        print(f"Created destination folder: {dest_folder['name']} (ID: {dest_id})")
    else:
        print(f"Error: Destination folder '{dest_name}' not found and --create-dest not specified.")
        return

    # 3. List files in source folder
    print(f"Listing files in '{source_folder['name']}'...")
    all_children = client.list_folder_children(source_id)
    
    # Filter out the destination folder if it is inside the source (to avoid recursion/errors)
    files_to_move = [f for f in all_children if f['id'] != dest_id]
    
    if not files_to_move:
        print("No files found to move.")
        return
        
    print(f"Found {len(files_to_move)} files to move.")
    
    # 4. Move files
    for file in files_to_move:
        file_id = file['id']
        file_name = file['name']
        print(f"Moving file: {file_name} ({file_id})")
        
        try:
            previous_parents = ",".join(file.get('parents', []))
            
            client.service.files().update(
                fileId=file_id,
                addParents=dest_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            print(f"Successfully moved: {file_name}")
        except Exception as e:
            print(f"Failed to move {file_name}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move all files from a source folder to a destination folder on Google Drive.")
    parser.add_argument("source", help="Name of the source folder")
    parser.add_argument("dest", help="Name of the destination folder")
    parser.add_argument("--create-dest", action="store_true", help="Create destination folder if it doesn't exist (created inside source)")
    
    args = parser.parse_args()
    
    move_files(args.source, args.dest, args.create_dest)
