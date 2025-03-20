"""
MD to DOCX converter with Mermaid diagram support.

This package provides tools for converting Markdown files to DOCX format,
with special handling for Mermaid diagrams and code blocks.
"""

__version__ = "0.1.1"

import click
import sys
import asyncio
import logging
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from .core import md_to_docx, render_mermaid_to_image

__all__ = ["md_to_docx", "render_mermaid_to_image"]

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


def serve():
    """Run the MCP server."""
    mcp.run(transport='stdio')


@click.group()
def cli():
    """MD to DOCX converter with Mermaid diagram support."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=str, help='Path to the output DOCX file (default: input_file_name.docx)')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
def convert(input_file, output, debug):
    """Convert Markdown file to DOCX file with Mermaid diagram support."""
    # Process input file path
    input_path = Path(input_file)
    
    # Determine output file path
    if output:
        output_path = output
    else:
        # Replace .md extension with .docx, or add .docx if no extension
        if input_path.suffix.lower() == '.md':
            output_path = str(input_path.with_suffix('.docx'))
        else:
            output_path = f"{input_file}.docx"
    
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        click.echo(f"Converting {input_file} to {output_path}...")
        
        # Convert to DOCX
        result = md_to_docx(md_content, output_path, debug)
        
        click.echo(f"Conversion completed successfully! Output file: {result}")
        return 0
    
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)
        import traceback
        traceback.print_exc()
        return 1


@cli.command()
@click.option("-v", "--verbose", count=True, help="Increase verbosity (can be used multiple times)")
def server(verbose):
    """Run as an MCP server."""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    # Don't use asyncio.run() here as mcp.run() handles the event loop itself
    serve()


def main():
    """Entry point for the application."""
    return cli()


if __name__ == "__main__":
    sys.exit(main()) 