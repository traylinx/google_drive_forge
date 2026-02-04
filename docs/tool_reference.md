# MCP Tool Reference

These tools are exposed by the Google Drive MCP server for use by AI agents.

---

## File Management

### `list_files`
List recent files in Google Drive.
- **Args**: `limit: int = 20`
- **Returns**: JSON list of file objects.

### `search_files`
Search files by name.
- **Args**: `query: str`, `limit: int = 20`
- **Returns**: JSON list of matching files.

### `list_folder`
List children of a specific folder.
- **Args**: `folder_id: str`, `limit: int = 50`
- **Returns**: JSON list of children.

### `get_file_metadata`
Get detailed metadata for a file.
- **Args**: `file_id: str`
- **Returns**: JSON metadata object.

### `create_folder`
Create a new folder.
- **Args**: `name: str`, `parent_id: str = 'root'`
- **Returns**: JSON with new folder details.

### `upload_file`
Upload a text file.
- **Args**: `name: str`, `content: str`, `parent_id: str = 'root'`
- **Returns**: JSON with new file details.

### `trash_file`
Move a file to trash.
- **Args**: `file_id: str`
- **Returns**: JSON confirmation.

---

## Intelligent Tools

### `resolve_path`
Resolve a human-readable path (e.g., `/Projects/2026`) to a File ID.
- **Args**: `path: str`
- **Returns**: Resolved file ID or error message.

### `smart_read`
Read a file's content by path. Auto-converts Google Docs to text.
- **Args**: `path: str`
- **Returns**: File content as string, or `<Binary Content>` for non-text files.

### `download_to_local`
Download a file to the local filesystem.
- **Args**: `file_id: str`, `local_path: str`
- **Returns**: Success message with saved path.

---

## The Forge (Skills)

### `list_skills`
List all AI-forged skills.
- **Returns**: JSON list of skill names and descriptions.

### `create_skill`
Create a new Python skill.
- **Args**: `name: str`, `code: str`, `description: str`
- **Returns**: Success message.

### `update_skill`
Update an existing skill.
- **Args**: `name: str`, `code: str`, `description: str = None`
- **Returns**: Success message.

### `run_skill`
Execute a skill.
- **Args**: `name: str`, `args: List[str] = None`
- **Returns**: Script output.

### `get_skill_guide`
Get the full `SKILL.md` documentation.
- **Returns**: Markdown content.
