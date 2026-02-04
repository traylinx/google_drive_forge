from typing import Optional, List
from mcp.server.fastmcp import Context, FastMCP
from .client import DriveClient
from .executor import ScriptExecutor
from .skill_loader import SkillLoader
from .audit import AuditLogger

def register_tools(mcp: FastMCP, client: DriveClient):
    """Registers tool handlers to the MCP server."""

    @mcp.tool()
    def list_files(limit: int = 20) -> str:
        """
        List the most recent files in Google Drive.
        
        Args:
            limit: Number of files to return (default 20, max 100).
        """
        import json
        files = client.list_files(limit=limit)
        return json.dumps(files, indent=2)

    @mcp.tool()
    def search_files(query: str, limit: int = 20) -> str:
        """
        Search for files in Google Drive by name.
        
        Args:
            query: The search text (e.g. project name).
            limit: Max results.
        """
        import json
        files = client.search(query, limit=limit)
        return json.dumps(files, indent=2)

    @mcp.tool()
    def list_folder(folder_id: str, limit: int = 50) -> str:
        """
        List all children (files and subfolders) of a specific folder.
        
        Args:
            folder_id: The ID of the folder to list. Use 'root' for top level.
            limit: Limit results.
        """
        import json
        files = client.list_folder_children(folder_id, limit=limit)
        return json.dumps(files, indent=2)

    @mcp.tool()
    def get_file_metadata(file_id: str) -> str:
        """
        Get detailed metadata for a file.
        
        Args:
            file_id: The ID of the file.
        """
        import json
        meta = client.get_file_metadata(file_id)
        return json.dumps(meta, indent=2)

    @mcp.tool()
    def create_folder(name: str, parent_id: str = 'root') -> str:
        """
        Create a new folder.
        
        Args:
            name: Name of the new folder.
            parent_id: ID of the parent folder (default 'root').
        """
        import json
        res = client.create_folder(name, parent_id)
        return json.dumps(res, indent=2)

    @mcp.tool()
    def upload_file(name: str, content: str, parent_id: str = 'root') -> str:
        """
        Upload a text file to Google Drive.
        
        Args:
            name: Name of the file.
            content: Text content of the file.
            parent_id: ID of the parent folder.
        """
        import json
        res = client.upload_file(name, content, parent_id=parent_id)
        return json.dumps(res, indent=2)

    @mcp.tool()
    def trash_file(file_id: str) -> str:
        """
        Move a file to the trash.
        
        Args:
            file_id: ID of the file to trash.
        """
        import json
        res = client.trash_file(file_id)
        return json.dumps(res, indent=2)

def register_intelligent_tools(mcp: FastMCP, client: DriveClient, executor: ScriptExecutor, loader: SkillLoader, audit: AuditLogger):
    """Registers the 'Forge' and 'Autonomy' tools to the MCP server."""

    @mcp.tool()
    def create_skill(name: str, code: str, description: str) -> str:
        """
        Forges a new capability (Skill) by writing a Python script.
        
        Args:
            name: Technical name of the skill (e.g., 'archive_old_files'). No spaces.
            code: The Python code for the script.
            description: What this skill does (will be saved in SKILL.md).
        """
        import os
        import re
        
        # Sanitize name
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
        
        skill_dir = os.path.join(loader.skills_dir, safe_name)
        os.makedirs(skill_dir, exist_ok=True)
        
        # Write script.py
        with open(os.path.join(skill_dir, "script.py"), "w") as f:
            f.write(code)
            
        # Write SKILL.md
        skill_md_content = f"""---
name: {safe_name}
description: {description}
---

{description}
"""
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write(skill_md_content)
            
        # Log to Audit
        audit.log_skill_creation(safe_name)
            
        return f"Skill '{safe_name}' forged successfully in {skill_dir}"

    @mcp.tool()
    def list_skills() -> str:
        """
        Lists all available AI-forged skills in the library.
        """
        import json
        skills = loader.discover_skills()
        return json.dumps([{"name": s.name, "description": s.description} for s in skills], indent=2)

    @mcp.tool()
    def update_skill(name: str, code: str, description: Optional[str] = None) -> str:
        """
        Updates an existing skill with new code or description.
        
        Args:
            name: Technical name of the skill to update.
            code: The new Python code.
            description: Optional updated description.
        """
        import os
        import re
        
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
        skill_dir = os.path.join(loader.skills_dir, safe_name)
        
        if not os.path.exists(skill_dir):
            return f"Error: Skill '{safe_name}' does not exist. Use create_skill first."
        
        # Update script.py
        with open(os.path.join(skill_dir, "script.py"), "w") as f:
            f.write(code)
            
        # Update SKILL.md if description provided
        if description:
            skill_md_content = f"""---
name: {safe_name}
description: {description}
---

{description}
"""
            with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
                f.write(skill_md_content)
        
        audit.log_event("SKILL_UPDATE", f"Capability updated: {safe_name}")
        return f"Skill '{safe_name}' updated successfully."

    @mcp.tool()
    def run_skill(name: str, args: Optional[List[str]] = None) -> str:
        """
        Executes an AI-forged skill from the library.
        
        Args:
            name: The name of the skill to run.
            args: Optional list of command-line arguments for the script.
        """
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
        return executor.run_skill(safe_name, args)

    @mcp.tool()
    def resolve_path(path: str) -> str:
        """
        Intelligently resolves a human-readable path (e.g., '/Projects/2026') to a File ID.
        Includes autonomous healing if the path is broken.
        
        Args:
            path: The full path to resolve.
        """
        file_id = client.find_and_heal_path(path)
        if file_id:
            return f"Resolved '{path}' to ID: {file_id}"
        return f"Error: Could not resolve path '{path}'. Check logs for suggestions."


    @mcp.tool()
    def get_skill_guide() -> str:
        """
        Returns the detailed manual (SKILL.md) for this Google Drive MCP.
        Read this to understand how to use autonomous features, The Forge, and script templates.
        """
        import os
        
        # Locate SKILL.md in the root of the MCP installation
        # Helper: tools.py is in src/, so root is ../
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        skill_md_path = os.path.join(base_dir, "SKILL.md")
        
        if not os.path.exists(skill_md_path):
            return "Error: SKILL.md not found in the MCP root directory."
            
        with open(skill_md_path, "r", encoding="utf-8") as f:
            return f.read()

    @mcp.tool()
    def download_to_local(file_id: str, local_path: str) -> str:
        """
        Downloads a file from Drive to the local filesystem.
        Automatically converts Google Docs/Sheets to meaningful text/markdown formats.
        
        Args:
            file_id: The ID of the file to download.
            local_path: Absolute path on the local machine to save the file.
        """
        import os
        try:
            # 1. Get Metadata to check type
            meta = client.get_file_metadata(file_id)
            name = meta.get('name')
            mime_type = meta.get('mimeType')
            
            # 2. Determine conversion (if needed)
            content = None
            final_path = local_path
            
            # Normalize path: if directory, append filename
            if os.path.isdir(local_path) or local_path.endswith(os.sep):
                os.makedirs(local_path, exist_ok=True)
                final_path = os.path.join(local_path, name)
            
            # Ensure parent dir exists
            os.makedirs(os.path.dirname(final_path), exist_ok=True)

            if mime_type == 'application/vnd.google-apps.document':
                # Export as text for Docs
                content = client.download_file(file_id, export_mime_type='text/plain')
                if not final_path.endswith(('.txt', '.md')):
                    final_path += '.md'
            elif mime_type == 'application/vnd.google-apps.spreadsheet':
                # Export as CSV for Sheets (easy to read) or Excel
                 content = client.download_file(file_id, export_mime_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                 if not final_path.endswith('.xlsx'):
                    final_path += '.xlsx'
            else:
                # Binary / Default
                content = client.download_file(file_id)
            
            # 3. Write to Disk
            with open(final_path, 'wb') as f:
                if isinstance(content, str):
                    f.write(content.encode('utf-8'))
                else:
                    f.write(content)
                    
            return f"Successfully downloaded '{name}' to '{final_path}'"
            
        except Exception as e:
            return f"Error downloading file: {str(e)}"

    @mcp.tool()
    def smart_read(path: str) -> str:
        """
        Resolves a path and reads its content in one step.
        Autonomously handles path healing and MIME-type conversion.
        
        Args:
            path: Path to the file.
        """
        file_id = client.find_and_heal_path(path)
        if not file_id:
            return f"Error: Could not resolve path '{path}'"
        
        try:
            # Check if it's a Google Doc that needs text export
            meta = client.get_file_metadata(file_id)
            mime_type = meta.get('mimeType')
            
            if mime_type == 'application/vnd.google-apps.document':
                # Force text export for reading
                content_bytes = client.download_file(file_id, export_mime_type='text/plain')
            else:
                content_bytes = client.download_file(file_id)

            # Try to decode
            if isinstance(content_bytes, str):
                return content_bytes
            
            try:
                return content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return f"<Binary Content: {len(content_bytes)} bytes> (MIME: {mime_type})"
        except Exception as e:
            return f"Error reading file at '{path}': {str(e)}"
