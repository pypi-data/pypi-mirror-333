# md_to_docx

A Python tool to convert Markdown documents to DOCX format with special support for Mermaid diagrams.

## Features

- Convert Markdown to DOCX while preserving formatting
- Render Mermaid diagrams as images in the resulting DOCX file
- Support for common Markdown elements:
  - Headers
  - Lists (ordered and unordered)
  - Tables
  - Bold and italic text
  - Code blocks
  - And more!

## Installation

```bash
pip install md_to_docx
```

## Usage

### Command Line

```bash
md-to-docx input.md output.docx
```

### Python API

```python
from md_to_docx import md_to_docx

# Convert markdown to docx
md_to_docx("path/to/input.md", "path/to/output.docx")

# Or with string content
markdown_content = "# Hello World\n\nThis is a test."
md_to_docx(markdown_content, "output.docx")
```

### MCP Server

This tool can also be used as an MCP server:

```python
from mcp.client import Client

client = Client()
result = client.md_to_docx(md_content="# Hello World", output_file="output.docx")
```

## Mermaid Support

The tool automatically renders Mermaid diagrams found in the Markdown. Example:

````markdown
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Do Something]
    B -->|No| D[Do Nothing]
```
````

## Requirements

- Python 3.8+
- Dependencies are automatically installed with the package

## License

MIT
