import os
import tempfile
import unittest
from md_to_docx import md_to_docx


class TestMdToDocx(unittest.TestCase):
    def test_basic_conversion(self):
        """Test basic conversion of Markdown to DOCX."""
        # Create a simple Markdown content
        md_content = """# Test Heading

This is a test paragraph.

## Subheading

* List item 1
* List item 2

```python
def hello():
    print("Hello, world!")
```

"""
        # Create a temporary file for the output
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            output_path = temp_file.name

        try:
            # Convert the Markdown to DOCX
            result = md_to_docx(md_content, output_path)
            
            # Check that the file exists and has content
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 0)
            
        finally:
            # Clean up temporary file
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == '__main__':
    unittest.main() 