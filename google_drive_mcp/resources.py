from mcp.server.fastmcp import Context, FastMCP
from .client import DriveClient

def register_resources(mcp: FastMCP, client: DriveClient):
    """Registers resource handlers to the MCP server."""

    @mcp.resource("gdrive://{file_id}/content")
    def get_file_content(file_id: str) -> str:
        """
        Reads the content of a file from Google Drive.
        Automatic export for Google Docs/Sheets/Slides (to PDF/Excel).
        """
        try:
            content_bytes = client.download_file(file_id)
            
            # Try to decode as text first
            try:
                return content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # If binary, return a representation or base64? 
                # MCP text resources expect string. For binary, we might need a different approach 
                # or just indicate it's binary.
                # For now, let's return a clear message or a hex representation if small?
                # A better pattern for binary files in MCP is usually not raw text resource 
                # unless using the 'blob' resource type (which FastMCP might wrap differently).
                # FastMCP resource decorators typically return text.
                return f"<Binary Content: {len(content_bytes)} bytes>"
        except Exception as e:
            return f"Error reading file {file_id}: {str(e)}"
