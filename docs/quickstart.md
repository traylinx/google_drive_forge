# Google Drive Forge - Quick Start

## Overview

**Google Drive Forge** provides two integration modes:

1.  **MCP Server**: For AI IDEs like Cursor and Claude Desktop.
2.  **Agentic Library**: For embedding into your own Python apps.

---

## 1. MCP Server Setup

Add the following to your MCP configuration file:

```json
{
  "mcpServers": {
    "google-drive-forge": {
      "command": "/path/to/venv/bin/python3",
      "args": [
        "-m",
        "google_drive_forge"
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

| Variable                     | Description                           |
| ---------------------------- | ------------------------------------- |
| `GOOGLE_DRIVE_CREDENTIALS`   | Path to `credentials.json`.           |
| `GOOGLE_DRIVE_HEADLESS_AUTH` | Set to `"true"` for headless servers. |

---

## 2. Python Library Setup

Install the package:

```bash
pip install git+https://github.com/your-org/google-drive-forge.git
```

### Basic Usage

```python
from google_drive_forge import ForgeClient

# Initialize
client = ForgeClient()

# List files
files = client.list_files(limit=10)
```

See [api_reference.md](api_reference.md) for full API details.
