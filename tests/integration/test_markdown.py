from unittest import TestCase
import docupy

class MarkdownToHtmlTests(TestCase):

    def check_markdown_to_html(self, markdown, html, lookup=None):
        with open(markdown) as f: markdown = f.read()
        with open(html) as f: html = f.read()
        lookup = lookup or {}
        for key, value in lookup.items():
            markdown = markdown.replace("\n" + value, "\n" + key)
        converted = docupy.markdown_to_html(markdown, paths=lookup)
        for line1, line2 in zip(converted.splitlines(), html.splitlines()):
            self.assertEqual(line1, line2)
        self.assertEqual(len(converted.splitlines()), len(html.splitlines()))



    def test_can_convert_markdown_to_html(self):
        self.check_markdown_to_html(
         "tests/integration/files/example.md",
         "tests/integration/files/example.html"
        )


    def test_can_convert_markdown_to_html_path_substitution(self):
        self.check_markdown_to_html(
         "tests/integration/files/example.md",
         "tests/integration/files/example.html",
         lookup={"logo": "/images/logo.png", "vid": "/videos/vid.mp4"}
        )
