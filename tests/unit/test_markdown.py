from unittest import TestCase
from unittest.mock import patch, Mock, PropertyMock
from collections import OrderedDict
from docupy.markdown import *
import docupy

class MarkdownToHtmlTests(TestCase):

    @patch("docupy.markdown.escape_characters")
    @patch("docupy.markdown.add_p_tags")
    @patch("docupy.markdown.add_list_tags")
    def test_can_convert_markdown_to_html(self, mock_list, mock_p, mock_esc):
        docupy.markdown.PATTERNS = OrderedDict((("20", "30"), ("H", "P")))
        mock_esc.return_value = ["H\x1A\x1AL\r\n20", "TM"]
        mock_p.return_value = ["HTML", "20"]
        mock_list.return_value = ["1", "2", "3"]
        html = "HTML\n20"
        markdown = markdown_to_html(html)
        mock_esc.assert_called_with("HTML\n20")
        mock_p.assert_called_with(["", "PTML", "30"])
        mock_list.assert_called_with(["HTML", "20"])
        self.assertEqual(markdown, "1\n2\n3")


    @patch("docupy.markdown.escape_characters")
    @patch("docupy.markdown.add_p_tags")
    @patch("docupy.markdown.add_list_tags")
    def test_can_convert_markdown_to_html_with_paths(self, mock_list, mock_p, mock_esc):
        docupy.markdown.PATTERNS = OrderedDict((("20", "src=\"3\""), ("H", "P")))
        mock_esc.return_value = ["H\x1A\x1AL\n20", "TM"]
        mock_p.return_value = ["HTML", "20"]
        mock_list.return_value = ["1", "2", "3"]
        html = "HTML\n20"
        markdown = markdown_to_html(html, paths={"3": "4/5"})
        mock_esc.assert_called_with("HTML\n20")
        mock_p.assert_called_with(["", "PTML", "src=\"4/5\""])
        mock_list.assert_called_with(["HTML", "20"])
        self.assertEqual(markdown, "1\n2\n3")



class CharacterEscapingTests(TestCase):

    def test_can_escape_no_characters(self):
        self.assertEqual(
         escape_characters("line1\nline2"), ("line1\nline2", [])
        )


    def test_can_escape_characters(self):
        self.assertEqual(
         escape_characters("li\\ne1\nli\\*ne2"),
         ("li\x1ae1\nli\x1ane2", ["n", "*"])
        )


    def test_cant_escape_line_breaks(self):
        self.assertEqual(
         escape_characters("li\\ne1\\\nli\\*ne2"),
         ("li\x1ae1\nli\x1ane2", ["n", "*"])
        )


    def test_slashes_can_be_at_end(self):
        self.assertEqual(
         escape_characters("li\\ne1\nli\\*ne2\\"),
         ("li\x1ae1\nli\x1ane2\\", ["n", "*"])
        )



class PTagAddingTests(TestCase):

    def test_can_add_p_tags(self):
        lines = ["<h1>A</h1>", "B", "<a>C</a>", "", "<code>", "D", "E", "</code>"]
        self.assertEqual(add_p_tags(lines), [
         "<h1>A</h1>", "<p>B</p>", "<p><a>C</a></p>", "<code>", "D", "E", "</code>"
        ])



class ListTagAddingTests(TestCase):

    def test_can_add_list_tags(self):
        lines = ["A", "<li>B</li>u", "<li>C</li>u", "D", "<li>E</li>o"]
        self.assertEqual(add_list_tags(lines), [
         "A", "<ul>", "<li>B</li>", "<li>C</li>", "</ul>", "D", "<ol>", "<li>E</li>", "</ol>"
        ])
