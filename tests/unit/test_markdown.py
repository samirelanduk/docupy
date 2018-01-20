from unittest import TestCase
from unittest.mock import patch, Mock
from docupy.markdown import *

class MarkdownToHtmlTests(TestCase):

    @patch("docupy.markdown.text_to_blocks")
    @patch("docupy.markdown.block_to_html")
    def test_can_convert_markdown_to_html(self, mock_html, mock_blocks):
        mock_blocks.return_value = ["block1", "block2"]
        mock_html.side_effect = ["html1", "html2"]
        markdown = "markdown"
        html = markdown_to_html(markdown, paths="PATHS")
        mock_blocks.assert_called_with("markdown")
        mock_html.assert_any_call("block1", paths="PATHS")
        mock_html.assert_any_call("block2", paths="PATHS")
        self.assertEqual(html, "html1\nhtml2")



class BlockSplittingTests(TestCase):

    def test_single_line_returns_single_block(self):
        blocks = text_to_blocks("A line.")
        self.assertEqual(blocks, ["A line."])


    def test_one_line_break_not_enough(self):
        blocks = text_to_blocks("A line.\nA second line?")
        self.assertEqual(blocks, ["A line. A second line?"])


    def test_can_break_into_blocks(self):
        blocks = text_to_blocks("A line.\n\nA second line\n\nThird line")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_empty_lines_ignored(self):
        blocks = text_to_blocks("A line.\n\n\n\nA second line\n\n\nThird line\n")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_windows_line_breaks(self):
        blocks = text_to_blocks("A line.\r\n\r\nA second line")
        self.assertEqual(blocks, ["A line.", "A second line"])



class BlockToHtmlTests(TestCase):

    @patch("docupy.markdown.create_special_html")
    def test_can_get_special_html(self, mock_html):
        mock_html.return_value = "<X>...</X>"
        html = block_to_html("!block", paths="PATHS")
        mock_html.assert_called_with("!block", paths="PATHS")
        self.assertEqual(html, "<X>...</X>")
        html = block_to_html("#block", paths="PAHS")
        mock_html.assert_called_with("#block", paths="PAHS")
        self.assertEqual(html, "<X>...</X>")


    @patch("docupy.markdown.create_paragraph_html")
    def test_can_get_para_html(self, mock_html):
        mock_html.return_value = "<X>...</X>"
        html = block_to_html("block", paths="PATHS")
        mock_html.assert_called_with("block")
        self.assertEqual(html, "<X>...</X>")


    @patch("docupy.markdown.create_paragraph_html")
    def test_can_escape_characters(self, mock_html):
        mock_html.return_value = "<X>\x1A..\x1A.</X>"
        html = block_to_html("\!bl\*ck\\")
        mock_html.assert_called_with("\x1Abl\x1Ack")
        self.assertEqual(html, "<X>!..*.</X>")



class SpecialHtmlTests(TestCase):

    def test_can_create_heading_html(self):
        html = create_special_html("##     head")
        self.assertEqual(html, "<h2>head</h2>")
        html = create_special_html("########HHH")
        self.assertEqual(html, "<h8>HHH</h8>")


    def test_can_get_image(self):
        html = create_special_html("![image1](path/to/image)")
        self.assertEqual(
         html, "<figure><img src=\"path/to/image\" title=\"image1\"></figure>"
        )


    def test_can_get_image_with_lookup(self):
        html = create_special_html("![pp](pp)", paths={"pp": "1", "gg": "2"})
        self.assertEqual(
         html, "<figure><img src=\"1\" title=\"pp\"></figure>"
        )


    def test_can_get_image_no_lookup(self):
        html = create_special_html("![gg](ll)", paths={"pp": "1", "gg": "2"})
        self.assertEqual(
         html, "<figure><img src=\"\" title=\"gg\"></figure>"
        )


    def test_can_get_video(self):
        html = create_special_html("!(path/to/video)")
        self.assertEqual(html, "<video src=\"path/to/video\" controls></video>")


    def test_can_get_video_with_lookup(self):
        html = create_special_html("!(pp)", paths={"pp": "1", "gg": "2"})
        self.assertEqual(html, "<video src=\"1\" controls></video>")


    def test_can_get_video_no_lookup(self):
        html = create_special_html("!(ll)", paths={"pp": "1", "gg": "2"})
        self.assertEqual(html, "<video src=\"\" controls></video>")


    def test_can_get_youtube(self):
        html = create_special_html("!{xxxyyyzzz}")
        self.assertEqual(
         html,
         "<div class=\"youtube\"><iframe src=\"//www.youtube.com/embed"
         "/xxxyyyzzz/\" frameborder=\"0\" allowfullscreen></iframe></div>"
        )



class ParagraphHtmlTests(TestCase):

    def test_can_create_paragraph_html(self):
        html = create_paragraph_html("text")
        self.assertEqual(html, "<p>text</p>")


    def test_can_get_italics_text(self):
        html = create_paragraph_html("text *italic*.")
        self.assertEqual(html, "<p>text <em>italic</em>.</p>")


    def test_can_get_italics_text(self):
        html = create_paragraph_html("text **bold**.")
        self.assertEqual(html, "<p>text <strong>bold</strong>.</p>")


    def test_can_get_struckthrough_text(self):
        html = create_paragraph_html("text ~~deleted~~.")
        self.assertEqual(html, "<p>text <del>deleted</del>.</p>")


    def test_can_get_link_text(self):
        html = create_paragraph_html("text [link](path).")
        self.assertEqual(html, "<p>text <a href=\"path\">link</a>.</p>")


    def test_can_get_link_title_text(self):
        html = create_paragraph_html("text [link](path \"title\").")
        self.assertEqual(
         html, "<p>text <a href=\"path\" title=\"title\">link</a>.</p>"
        )


    def test_can_get_external_link_text(self):
        html = create_paragraph_html("text {link}(path).")
        self.assertEqual(
         html, "<p>text <a href=\"path\" target=\"_blank\">link</a>.</p>"
        )


    def test_can_get_external_link_title_text(self):
        html = create_paragraph_html("text {link}(path \"title\").")
        self.assertEqual(
         html, "<p>text <a href=\"path\" target=\"_blank\" title=\"title\">link</a>.</p>"
        )


    def test_two_links(self):
        html = create_paragraph_html("[link](path) text {link}(path).")
        self.assertEqual(
         html, "<p><a href=\"path\">link</a> text <a href=\"path\" target=\"_blank\">link</a>.</p>"
        )
