# Agentic App Integration Guide

This guide explains how to use `google_drive_forge` as a library in your own Python applications and agents.

---

## Installation

```bash
# From source
pip install -e /path/to/mcp/google_drive/

# From git
pip install git+https://github.com/your-org/google-drive-forge.git
```

---

## Example: Simple File Lister

```python
from google_drive_forge import ForgeClient

def main():
    client = ForgeClient()
    
    print("Recent files:")
    for f in client.list_files(limit=5):
        print(f"  - {f['name']} ({f['id']})")

if __name__ == "__main__":
    main()
```

---

## Example: Downloading Docs to Local

```python
from google_drive_forge import IntelligentDriveClient
import os

def download_folder_as_markdown(folder_path: str, local_dir: str):
    """
    Downloads all Google Docs from a Drive folder to a local directory as Markdown.
    """
    client = IntelligentDriveClient()
    os.makedirs(local_dir, exist_ok=True)
    
    # Resolve the folder path to an ID
    folder_id = client.find_and_heal_path(folder_path)
    if not folder_id:
        print(f"Error: Could not find folder '{folder_path}'")
        return
    
    # List files in the folder
    files = client.list_folder_children(folder_id)
    
    for f in files:
        if f['mimeType'] == 'application/vnd.google-apps.document':
            content = client.download_file(f['id'], export_mime_type='text/plain')
            local_path = os.path.join(local_dir, f['name'] + ".md")
            with open(local_path, 'wb') as out:
                out.write(content)
            print(f"Saved: {local_path}")

if __name__ == "__main__":
    download_folder_as_markdown("/socialMedia/skills", "./local_skills")
```

---

## Example: Running a Forged Skill

```python
from google_drive_forge import ScriptExecutor

def main():
    executor = ScriptExecutor(
        python_path="/path/to/venv/bin/python",
        skills_dir="/path/to/mcp/google_drive/skills"
    )
    
    # Run an existing skill
    output = executor.run_skill("auto_archive", args=["--days", "30"])
    print(output)

if __name__ == "__main__":
    main()
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Your Agentic App                       │
│  (e.g., chatbot, automation script, AI workflow)            │
└───────────────────────────┬─────────────────────────────────┘
                            │ imports
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    google_drive_forge                         │
│  ┌───────────────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │ IntelligentClient │  │ ScriptExecutor│  │ SkillLoader │  │
│  │ (Drive API)       │  │ (The Forge)   │  │ (Discovery) │  │
│  └─────────┬─────────┘  └───────┬───────┘  └──────┬──────┘  │
│            │                    │                 │         │
│            └───────────────────┼─────────────────┘         │
│                               ▼                             │
│                        Google Drive API                     │
└─────────────────────────────────────────────────────────────┘
```
