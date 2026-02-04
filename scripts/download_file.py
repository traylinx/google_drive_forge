
import argparse
import logging
import sys
import os

# Add parent directory to sys.path to access src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google_drive_mcp.intelligent_client import IntelligentDriveClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(file_id, dest_path):
    client = IntelligentDriveClient()
    
    print(f"Resolving file ID: {file_id}...")
    try:
        # Check metadata for name and mimeType
        meta = client.service.files().get(fileId=file_id, fields="name, mimeType").execute()
        file_name = meta.get('name')
        mime_type = meta.get('mimeType')
        print(f"Found: {file_name} ({mime_type})")
        
        # Determine output filename
        if os.path.isdir(dest_path):
            # If dest is a dir, save with original name inside it
            output_file = os.path.join(dest_path, file_name)
        else:
            # If dest is a file path (or doesn't exist yet/ends in extension), use it
            output_file = dest_path
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Download logic
        if mime_type == 'application/vnd.google-apps.document':
            print("Detected Google Doc. Exporting as plain text...")
            content = client.download_file(file_id, export_mime_type='text/plain')
            # If output filename doesn't have extension, add .md or .txt?
            # Let's trust the user's dest path or append .md if it was auto-generated from name
            if os.path.isdir(dest_path) and not output_file.lower().endswith(('.md', '.txt')):
                 output_file += ".md"
        else:
            print("Downloading binary content...")
            content = client.download_file(file_id)

        # Write to file
        with open(output_file, "wb") as f:
            if isinstance(content, str):
                f.write(content.encode('utf-8'))
            else:
                f.write(content)
                
        print(f"Successfully saved to: {output_file}")
        
    except Exception as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a specific file from Google Drive by ID.")
    parser.add_argument("file_id", help="The Google Drive File ID")
    parser.add_argument("dest", help="Local destination path (directory or filename)")
    
    args = parser.parse_args()
    
    download_file(args.file_id, args.dest)
