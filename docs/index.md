# Google Drive Forge Documentation

Welcome to the documentation for **Google Drive Forge** (formerly Google Drive MCP).

## Contents

| Document                                      | Description                                    |
| --------------------------------------------- | ---------------------------------------------- |
| [Quick Start](quickstart.md)                  | Setup guide for MCP Server and Python library. |
| [API Reference](api_reference.md)             | Python classes and methods for library usage.  |
| [Tool Reference](tool_reference.md)           | MCP tools exposed to AI agents.                |
| [Agentic Integration](agentic_integration.md) | Examples for embedding in your own apps.       |

## Overview

This project provides two ways to interact with Google Drive:

1.  **MCP Server**: Exposes tools for AI IDEs like Cursor and Claude Desktop.
2.  **Agentic Library**: Embed `google_drive_forge` into your own agentic workflows.

## Quick Links

-   **Main Entry Point (MCP)**: `server.py` or `python -m google_drive_forge`
-   **Package Name**: `google_drive_forge`
-   **Key Classes**: `ForgeClient`, `ScriptExecutor`, `SkillLoader`
