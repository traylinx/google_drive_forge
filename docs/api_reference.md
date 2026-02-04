# API Reference

This document describes the public Python API for the `google_drive_mcp` package.

---

## `IntelligentDriveClient`

The primary client for interacting with Google Drive. Extends `DriveClient` with autonomous features.

```python
from google_drive_mcp import IntelligentDriveClient

client = IntelligentDriveClient(audit=None)  # audit: Optional[AuditLogger]
```

### Methods

| Method                                          | Description                                                                               |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `list_files(query=None, limit=10)`              | List files. Returns `List[Dict]`.                                                         |
| `search(text, limit=20)`                        | Search files by name. Returns `List[Dict]`.                                               |
| `get_file_metadata(file_id)`                    | Get detailed metadata. Returns `Dict`.                                                    |
| `download_file(file_id, export_mime_type=None)` | Download file content. Returns `bytes`.                                                   |
| `create_folder(name, parent_id='root')`         | Create a folder. Returns `Dict`.                                                          |
| `upload_file(name, content, parent_id='root')`  | Upload a file. Returns `Dict`.                                                            |
| `trash_file(file_id)`                           | Move file to trash. Returns `Dict`.                                                       |
| `list_folder_children(folder_id, limit=100)`    | List children of a folder. Returns `List[Dict]`.                                          |
| `find_and_heal_path(path)`                      | Resolve a human-readable path to a file ID with auto-correction. Returns `str` or `None`. |

---

## `ScriptExecutor`

Runs Python scripts (skills) in a subprocess.

```python
from google_drive_mcp import ScriptExecutor

executor = ScriptExecutor(python_path="/path/to/python", skills_dir="/path/to/skills")
```

### Methods

| Method                             | Description                                     |
| ---------------------------------- | ----------------------------------------------- |
| `run_skill(skill_name, args=None)` | Execute a skill script. Returns `str` (stdout). |

---

## `SkillLoader`

Discovers and manages AI-forged skills.

```python
from google_drive_mcp import SkillLoader

loader = SkillLoader(skills_dir="/path/to/skills")
```

### Methods

| Method              | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `discover_skills()` | Returns a `List[SkillMeta]` of all available skills. |

---

## `DriveClient`

The base client without autonomous features. Use `IntelligentDriveClient` for most cases.
