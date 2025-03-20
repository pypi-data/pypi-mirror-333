"""
Command-line interface for md_to_docx.
"""

import argparse
import sys
from pathlib import Path
from .converter import md_to_docx


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown to DOCX with Mermaid diagram support"
    )
    parser.add_argument(
        "input_file",
        help="Input Markdown file path"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="Output DOCX file path (default: input filename with .docx extension)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Set default output file if not provided
    if args.output_file is None:
        output_file = input_path.with_suffix(".docx")
    else:
        output_file = args.output_file
    
    try:
        result = md_to_docx(str(input_path), str(output_file))
        print(f"Successfully converted '{input_path}' to '{result}'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 