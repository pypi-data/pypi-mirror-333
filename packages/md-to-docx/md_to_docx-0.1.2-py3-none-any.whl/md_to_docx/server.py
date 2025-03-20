"""Server module for md_to_docx.

This module re-exports server functionality from the package's __init__ for backward compatibility.
"""

from md_to_docx import serve

if __name__ == "__main__":
    serve() 