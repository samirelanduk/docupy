from unittest import TestCase
import docupy

class MarkdownToHtmlTests(TestCase):

    def test_can_convert_markdown_to_html(self):
        with open("tests/integration/files/example.md") as f:
            markdown = f.read()
        with open("tests/integration/files/example.html") as f:
            html = [line.rstrip() for line in f.readlines()]
        self.assertEqual(docupy.markdown_to_html(markdown).split("\n"), html)


    def test_can_convert_markdown_to_html_path_substitution(self):
        lookup = {"logo": "/images/logo.png", "vid": "/videos/vid.mp4"}
        with open("tests/integration/files/example.md") as f:
            markdown = f.read()
        markdown = markdown.replace("/images/logo.png", "logo").replace(
         "/videos/vid.mp4)\n", "vid)\n"
        )
        with open("tests/integration/files/example.html") as f:
            html = [line.rstrip() for line in f.readlines()]
        self.assertEqual(
         docupy.markdown_to_html(markdown, paths=lookup).split("\n"), html
        )
