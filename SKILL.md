---
name: google-drive-mcp
description: "Autonomous Google Drive management with intelligent path resolution, auto-recovery, and custom skill forging. Use when Claude needs to work with cloud storage for tasks like: (1) Navigating complex folder structures with human-like paths (/Work/Projects/2026), (2) Reading and converting content from Docs, Sheets, and PDFs, (3) Automating multi-step Drive operations by creating and running custom Python 'Skills', (4) Managing files (upload, search, trash)."
---

# Google Drive MCP

## Overview

This skill transforms Claude into an **Autonomous Power-User** for Google Drive. It goes beyond basic file listing by providing a cognitive layer that handles path resolution, autonomous recovery from errors, and the ability to extend itself by "forging" new capabilities on the fly.

## Core Capabilities

### 1. Intelligent Navigation & Reading

Forget opaque File IDs. Use human-readable paths and automatic content conversion.

- **`resolve_path`**: Converts a path like `/Marketing/Drafts/2026_Strategy` into a File ID. If parts of the path are missing or misspelled, it attempts "Self-Healing" to find the closest match.
- **`smart_read`**: A high-level tool that resolves a path, downloads the content, and converts it to text (Decodes Google Docs, Sheets, and PDFs automatically) in one step.

### 2. Standard File Management

Comprehensive control over the Drive filesystem.

- **`list_files` / `list_folder`**: Discover recent files or explore specific directories.
- **`search_files`**: Finds files by name or content properties.
- **`create_folder` / `upload_file` / `trash_file`**: Manage the lifecycle of your storage.

### 3. The Forge (Autonomous Skills)

Empower Claude to expand its own capabilities by writing and executing Python logic directly on the Drive API.

- **`create_skill`**: Design a custom script for complex tasks (e.g., "Archive all files older than 30 days").
- **`run_skill`**: Execute a forged capability with parameters.
- **`list_skills`**: View the library of existing capabilities Claude has learned.

## Common Workflows

### Organizing Files

When a user asks to "Organize the social media folder", use `list_folder` to find the content, `create_folder` for new categories, and `run_skill` (or basic `update`) to move them.

### Reading Complex Documents

For Google Docs or PDFs, always prefer `smart_read`. It handles the export MIME-types automatically so you get clean markdown/text. If `smart_read` returns binary content for a PDF, you may need to download it to process it locally.

### Downloading Files to Project

To save a file from Drive to the user's local project (e.g., to `jevelabsblog/drafts/skills`), use **`download_to_local`**.
- It automatically converts Google Docs to Markdown/Text.
- It accepts an absolute path (e.g., `/Users/sebastian/Projects/...`).
- **Usage**: `download_to_local(file_id="...", local_path="/absolute/path/to/blog_post.md")`

### Creating Automations

If a task is repetitive (like "Sync all new PDFs to a specific folder"), use `create_skill` to write a Python script that uses the `IntelligentDriveClient`. This is more token-efficient than doing it step-by-step for every file.

## Resources

### scripts/

The `scripts/` directory contains utility examples that can be used as templates for "The Forge". They are now dynamic and can be adapted for any workflow:

- **`move_files.py`**: Generic bulk mover.
  - Usage: `python scripts/move_files.py <source_folder> <dest_folder> [--create-dest]`
  - Example: `python scripts/move_files.py "Downloads" "Archive/2025" --create-dest`

- **`batch_download.py`**: Generic folder syncer.
  - Usage: `python scripts/batch_download.py <drive_folder_name> <local_dest_path>`
  - Example: `python scripts/batch_download.py "Project Assets" "./assets"`

- **`download_file.py`**: Single file downloader (Auto-converts Docs to Markdown).
  - Usage: `python scripts/download_file.py <file_id> <dest_path>`
  - Example: `python scripts/download_file.py "12345abcde" "./docs/spec.md"`

### references/

- `api_reference.md`: Detailed documentation of the internal `IntelligentDriveClient` used by the AI-forged skills.
