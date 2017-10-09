from unittest import TestCase
import docupy

class MarkdownToHtmlTests(TestCase):

    def test_can_convert_markdown_to_html(self):
        with open("tests/integration/files/example.md") as f:
            markdown = f.read()
        with open("tests/integration/files/example.html") as f:
            html = f.read()
        self.assertEqual(docupy.markdown_to_html(markdown), html)
