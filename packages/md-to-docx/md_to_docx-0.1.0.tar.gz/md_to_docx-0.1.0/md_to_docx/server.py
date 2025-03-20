"""
MCP server implementation for md_to_docx.
"""

from mcp.server.fastmcp import FastMCP
from .converter import md_to_docx as convert_md_to_docx

# Initialize FastMCP server
mcp = FastMCP("md_to_docx")


@mcp.tool()
async def md_to_docx(md_content: str, output_file: str = None):
    """Convert Markdown content to DOCX, rendering Mermaid diagrams as images.
    
    Args:
        md_content: Markdown content to convert
        output_file: Optional output file path, defaults to 'output.docx'
    
    Returns:
        Path to the generated DOCX file
    """
    return convert_md_to_docx(md_content, output_file)


def run_server():
    """Run the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    run_server() 