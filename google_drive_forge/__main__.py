import logging
import os
import sys
from mcp.server.fastmcp import FastMCP
from .intelligent_client import IntelligentDriveClient
from .tools import register_tools, register_intelligent_tools
from .resources import register_resources
from .executor import ScriptExecutor
from .skill_loader import SkillLoader
from .audit import AuditLogger

# Configure logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize FastMCP Server
mcp = FastMCP("google-drive-forge")

# Setup Paths from Environment or Defaults
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

SKILLS_DIR = os.getenv("GOOGLE_DRIVE_SKILLS_DIR", os.path.join(BASE_DIR, "skills"))
# Default to current python if no specific venv provided or found
DEFAULT_VENV = os.path.join(os.path.dirname(BASE_DIR), "antigravity-env")
PYTHON_EXE = os.getenv("GOOGLE_DRIVE_PYTHON_PATH")

if not PYTHON_EXE:
    if os.path.exists(DEFAULT_VENV):
        PYTHON_EXE = DEFAULT_VENV
    else:
        PYTHON_EXE = sys.executable

AUDIT_LOG = os.getenv("GOOGLE_DRIVE_AUDIT_LOG", os.path.join(PROJECT_ROOT, "docs/research/intelligent_audit.log"))

try:
    # Initialize Core Components
    audit = AuditLogger(AUDIT_LOG)
    client = IntelligentDriveClient(audit=audit)
    executor = ScriptExecutor(PYTHON_EXE, SKILLS_DIR)
    loader = SkillLoader(SKILLS_DIR)
    
    # Register Components
    register_tools(mcp, client)
    register_resources(mcp, client)
    register_intelligent_tools(mcp, client, executor, loader, audit)
    
except Exception as e:
    logger.error(f"Failed to initialize server components: {e}")
    @mcp.tool()
    def status() -> str:
        return f"Server failed to initialize: {str(e)}. Please check setup."

def main():
    mcp.run()

if __name__ == "__main__":
    main()
