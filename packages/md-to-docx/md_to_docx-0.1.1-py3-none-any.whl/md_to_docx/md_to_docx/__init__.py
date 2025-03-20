"""
MD to DOCX converter with Mermaid diagram support.

This package provides tools for converting Markdown files to DOCX format,
with special handling for Mermaid diagrams and code blocks.
"""

__version__ = "0.1.1"

from .core import md_to_docx, render_mermaid_to_image

__all__ = ["md_to_docx", "render_mermaid_to_image"] 