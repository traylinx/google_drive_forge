# Google Drive Forge - Complete Setup Guide

This guide walks you through everything needed to get Google Drive Forge working from scratch.

---

## Prerequisites

- **Python 3.10+** installed on your system
- A **Google Account** (personal or Workspace)
- **5-10 minutes** for initial setup

---

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Enter a project name (e.g., `drive-forge-mcp`)
4. Click **Create**
5. Wait for the project to be created, then select it

---

## Step 2: Enable the Google Drive API

1. In your new project, go to **APIs & Services** → **Library**
2. Search for **"Google Drive API"**
3. Click on **Google Drive API**
4. Click **Enable**

---

## Step 3: Configure OAuth Consent Screen

Before creating credentials, you must configure the OAuth consent screen:

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have a Workspace account and want internal-only)
3. Click **Create**
4. Fill in the required fields:
   - **App name**: `Drive Forge MCP`
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click **Save and Continue**
6. On the **Scopes** page, click **Add or Remove Scopes**
7. Find and select:
   - `https://www.googleapis.com/auth/drive` (full Drive access)
8. Click **Update** → **Save and Continue**
9. On the **Test users** page, click **Add Users**
10. Add your Google email address
11. Click **Save and Continue** → **Back to Dashboard**

> **Note**: For personal use, your app will remain in "Testing" mode. This is fine — it just means only the test users you added can authorize it.

---

## Step 4: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. For **Application type**, select **Desktop app**
4. Enter a name (e.g., `Drive Forge Desktop`)
5. Click **Create**
6. A dialog will appear with your Client ID and Client Secret
7. Click **Download JSON**
8. Rename the downloaded file to `credentials.json`
9. Move it to a secure location (e.g., `~/.config/google-drive-forge/credentials.json`)

---

## Step 5: Install Google Drive Forge

```bash
pip install google-drive-forge
```

---

## Step 6: First-Time Authentication

The first time you run Google Drive Forge, it will open a browser for OAuth authorization:

### Option A: Interactive Mode (Recommended for Desktop)

```bash
# Set the path to your credentials
export GOOGLE_DRIVE_CREDENTIALS=~/.config/google-drive-forge/credentials.json

# Run the MCP server (it will open your browser)
google-drive-forge
```

1. A browser window will open
2. Sign in with the Google account you added as a test user
3. Click **Continue** (past the "unverified app" warning)
4. Click **Allow** to grant Drive access
5. A `token.json` file will be created in the same directory as `credentials.json`

### Option B: Headless Mode (For Servers)

If you're running on a headless server:

```bash
export GOOGLE_DRIVE_CREDENTIALS=/path/to/credentials.json
export GOOGLE_DRIVE_HEADLESS_AUTH=true

google-drive-forge
```

This will print a URL to the console. Copy it, open it in any browser, complete the authorization, and paste the resulting code back into the terminal.

---

## Step 7: Configure Your MCP Client

Add Google Drive Forge to your MCP client configuration:

```json
{
  "mcpServers": {
    "google-drive-forge": {
      "command": "google-drive-forge",
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

---

## Environment Variables Reference

| Variable                     | Description                 | Default              |
| ---------------------------- | --------------------------- | -------------------- |
| `GOOGLE_DRIVE_CREDENTIALS`   | Path to `credentials.json`  | `./credentials.json` |
| `GOOGLE_DRIVE_HEADLESS_AUTH` | Enable console-based OAuth  | `false`              |
| `GOOGLE_DRIVE_PYTHON_PATH`   | Custom Python executable    | System default       |
| `GOOGLE_DRIVE_SKILLS_DIR`    | Directory for forged skills | `./skills`           |

---

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you added your email as a **test user** in the OAuth consent screen

### "Token has expired"
- Delete `token.json` and run the authentication flow again

### "The OAuth client was not found"
- Verify `credentials.json` is the correct file from Google Cloud Console

### "Permission denied" errors
- Ensure you selected the `drive` scope during OAuth consent screen setup

---

## Security Notes

- **Keep `credentials.json` and `token.json` private** — they grant access to your Google Drive
- **Don't commit them to git** — add them to `.gitignore`
- **Revoke access anytime** at [Google Account Permissions](https://myaccount.google.com/permissions)

---

## Next Steps

Once setup is complete, see:
- [Quick Start Guide](quickstart.md) — Basic usage examples
- [Tool Reference](tool_reference.md) — All available MCP tools
- [Agentic Integration](agentic_integration.md) — Advanced autonomous features
