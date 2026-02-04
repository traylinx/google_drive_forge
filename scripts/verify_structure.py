import logging
import sys
import os

# Add parent directory to sys.path to access src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.intelligent_client import IntelligentDriveClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_and_fix():
    client = IntelligentDriveClient()
    
    print("Verifying 'socialMedia' structure...")
    
    # Find socialMedia
    social_cols = client.list_files(query="name = 'socialMedia' and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
    if not social_cols:
        print("ERROR: socialMedia not found")
        return
    social_id = social_cols[0]['id']
    print(f"socialMedia ID: {social_id}")
    
    # Find skills inside socialMedia
    skills_cols = client.list_files(query=f"name = 'skills' and mimeType = 'application/vnd.google-apps.folder' and '{social_id}' in parents and trashed = false")
    if not skills_cols:
        print("ERROR: skills folder not found in socialMedia")
        return
    skills_id = skills_cols[0]['id']
    print(f"skills ID: {skills_id}")
    
    # Check contents of skills
    print("Checking contents of 'skills'...")
    children = client.list_folder_children(skills_id)
    
    clawdbot_in_skills = None
    for c in children:
        print(f"- {c['name']} ({c['mimeType']})")
        if c['name'] == 'clawdbot' and c['mimeType'] == 'application/vnd.google-apps.folder':
            clawdbot_in_skills = c
            
    if clawdbot_in_skills:
        print("\nFound 'clawdbot' folder inside 'skills'. Moving it back to 'socialMedia'...")
        # Move back
        client.service.files().update(
            fileId=clawdbot_in_skills['id'],
            addParents=social_id,
            removeParents=skills_id,
            fields='id, parents'
        ).execute()
        print("Moved 'clawdbot' back to 'socialMedia'.")
    else:
        print("\n'clawdbot' is not in 'skills'. Verification passed.")

if __name__ == "__main__":
    verify_and_fix()
