
import sys
import os

# Add the current directory to sys.path so we can import the package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_drive_mcp.__main__ import main

if __name__ == "__main__":
    main()
