import os
import json
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Configure logger for this module
logger = logging.getLogger(__name__)

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/drive']

# Base directory for relative paths (assumes this file is in src/, so go up one level)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')

def get_credentials() -> Credentials:
    """
    Retrieves OAuth2 credentials.
    Refreshes expired tokens if possible, or triggers a new login flow.
    """
    creds = None
    
    # 1. Try to load existing token
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            logger.warning(f"Error loading token.json: {e}")
            # Invalid token file, ignore it

    # 2. If no valid credentials, login or refresh
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing access token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                 logger.warning(f"Error refreshing token: {e}. Initiating new login.")
                 creds = _login_flow()
        else:
            logger.info("No valid token found. Initiating login flow...")
            creds = _login_flow()

        # 3. Save the new/refreshed token
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            logger.info(f"Token saved to {TOKEN_PATH}")

    return creds

def _login_flow() -> Credentials:
    """Helper to run the interactive OAuth flow."""
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"Credentials file not found at {CREDENTIALS_PATH}. "
            "Please download it from Google Cloud Console and place it there."
        )

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    
    # Check for headless environment
    is_headless = os.getenv("GOOGLE_DRIVE_HEADLESS_AUTH", "false").lower() == "true"
    
    if is_headless:
        logger.info("Headless mode detected. Please follow the URL to authenticate.")
        # run_local_server with open_browser=False is the modern replacement for run_console
        creds = flow.run_local_server(port=0, open_browser=False)
    else:
        # Standard flow with browser
        creds = flow.run_local_server(port=0)
        
    return creds
