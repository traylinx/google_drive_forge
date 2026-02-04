# Google Drive MCP - Quick Start

## Overview

Google Drive MCP provides two integration modes:
1.  **MCP Server**: For AI IDEs like Cursor and Claude Desktop.
2.  **Python Library**: For embedding into your own agentic apps.

---

## 1. MCP Server Setup (Cursor / Claude Desktop)

Add the following to your MCP configuration file (e.g., `mcp_config.json` or `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "/path/to/venv/bin/python3",
      "args": [
        "/path/to/google_drive/server.py"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "/path/to/credentials.json",
        "GOOGLE_DRIVE_HEADLESS_AUTH": "true"
      }
    }
  }
}
```

### Environment Variables

| Variable                     | Description                                                               |
| ---------------------------- | ------------------------------------------------------------------------- |
| `GOOGLE_DRIVE_CREDENTIALS`   | Path to your `credentials.json` from Google Cloud Console.                |
| `GOOGLE_DRIVE_HEADLESS_AUTH` | Set to `"true"` for servers without a browser (auth URL printed to logs). |
| `GOOGLE_DRIVE_PYTHON_PATH`   | (Optional) Python executable for running forged skills.                   |
| `GOOGLE_DRIVE_SKILLS_DIR`    | (Optional) Directory to store AI-forged skills.                           |

### First Run Authentication

On first run, the server will prompt you to authenticate with Google.
1.  A URL will appear in the server logs.
2.  Open the URL in a browser.
3.  Authenticate and grant permissions.
4.  The server will save a `token.json` and start.

---

## 2. Python Library Setup (Agentic Apps)

Install the package:

```bash
# From source (local development)
pip install -e /path/to/google_drive/

# Or from git (when published)
pip install git+https://github.com/your-org/google-drive-mcp.git
```

### Basic Usage

```python
from google_drive_mcp import IntelligentDriveClient

# Initialize the client (triggers auth on first run)
client = IntelligentDriveClient()

# List files
files = client.list_files(limit=10)
print(files)

# Download a Google Doc as text
content = client.download_file("YOUR_FILE_ID", export_mime_type="text/plain")
print(content.decode('utf-8'))

# Self-healing path resolution
file_id = client.find_and_heal_path("/Projects/MyDoc")
```

See [api_reference.md](api_reference.md) for full API details.
