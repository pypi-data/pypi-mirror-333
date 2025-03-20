from typing import Any
import os
from mcp.server.fastmcp import FastMCP
from .core import md_to_docx

# Initialize FastMCP server
mcp = FastMCP("md_to_docx")


@mcp.tool()
async def md_to_docx_tool(md_content: str, output_file: str = None, debug_mode: bool = False) -> str:
    """Convert Markdown file to DOCX, rendering Mermaid diagrams as images.
    
    Args:
        md_content: Markdown content to convert
        output_file: Optional output file path, defaults to 'output.docx'
        debug_mode: Whether to enable debug mode
        
    Returns:
        The path to the saved DOCX file
    """
    return md_to_docx(md_content, output_file, debug_mode)


def run_server():
    """Run the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    run_server() 