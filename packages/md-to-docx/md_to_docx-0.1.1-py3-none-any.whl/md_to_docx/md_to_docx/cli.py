#!/usr/bin/env python
import argparse
import os
import sys
from pathlib import Path

from .core import md_to_docx as convert_md_to_docx


def main():
    """Command line interface for the md_to_docx package."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown file to DOCX file with Mermaid diagram support'
    )
    
    parser.add_argument(
        'input_file', 
        type=str, 
        help='Path to the Markdown file to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Path to the output DOCX file (default: input_file_name.docx)'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    # Determine output file path
    if args.output:
        output_path = args.output
    else:
        # Replace .md extension with .docx, or add .docx if no extension
        if input_path.suffix.lower() == '.md':
            output_path = str(input_path.with_suffix('.docx'))
        else:
            output_path = f"{args.input_file}.docx"
    
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        print(f"Converting {args.input_file} to {output_path}...")
        
        # Convert to DOCX
        result = convert_md_to_docx(md_content, output_path, args.debug)
        
        print(f"Conversion completed successfully! Output file: {result}")
        return 0
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 