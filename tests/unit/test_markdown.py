from unittest import TestCase
from unittest.mock import patch, Mock
from docupy.markdown import *

class ParagraphHtmlTests(TestCase):

    def test_can_create_paragraph_html(self):
        html = create_paragraph_html("text")
        self.assertEqual(html, "<p>text</p>")


    def test_can_get_italics_text(self):
        html = create_paragraph_html("text *italic*.")
        self.assertEqual(html, "<p>text <em>italic</em>.</p>")


    def test_can_get_bold_text(self):
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


    def test_can_omit_p_tags(self):
        html = create_paragraph_html("[link](path) text {link}(path).", p=False)
        self.assertEqual(
         html, "<a href=\"path\">link</a> text <a href=\"path\" target=\"_blank\">link</a>."
        )



class HeadingHtmlTests(TestCase):

    def test_can_create_heading_html_no_spaces(self):
        html = create_heading_html("##head")
        self.assertEqual(html, "<h2>head</h2>")
        html = create_heading_html("########HH#H")
        self.assertEqual(html, "<h8>HH#H</h8>")


    def test_can_create_heading_html_with_spaces(self):
        html = create_heading_html("## head")
        self.assertEqual(html, "<h2>head</h2>")
        html = create_heading_html("########          HH#H")
        self.assertEqual(html, "<h8>HH#H</h8>")



class ImageHtmlTests(TestCase):

    def test_basic_image_markdown(self):
        html = create_image_html("![t](image.jpg)")
        self.assertEqual(
         html, '<figure><img src="image.jpg" title="t"></figure>'
        )


    def test_basic_image_markdown_with_paths(self):
        html = create_image_html("![t](p)", paths={"s": "A", "p": "B"})
        self.assertEqual(
         html, '<figure><img src="B" title="t"></figure>'
        )


    def test_basic_image_markdown_with_failed_paths(self):
        html = create_image_html("![t](x)", paths={"s": "A", "p": "B"})
        self.assertEqual(
         html, '<figure><img src="x" title="t"></figure>'
        )


    @patch("docupy.markdown.create_paragraph_html")
    def test_basic_image_markdown_with_caption(self, mock_p):
        mock_p.return_value = "cap"
        html = create_image_html("![t][c](image.p)")
        self.assertEqual(
         html,
         '<figure><img src="image.p" title="t"><figcaption>cap</figcaption></figure>'
        )
        mock_p.assert_called_with("c", p=False)


    @patch("docupy.markdown.create_paragraph_html")
    def test_basic_image_markdown_with_paths_and_caption(self, mock_p):
        mock_p.return_value = "cap"
        html = create_image_html("![t][c](p)", paths={"s": "A", "p": "B"})
        self.assertEqual(
         html,
         '<figure><img src="B" title="t"><figcaption>cap</figcaption></figure>'
        )
        mock_p.assert_called_with("c", p=False)



class VideoHtmlTests(TestCase):

    def test_basic_video_markdown(self):
        html = create_video_html("!(/videos/vid.mp4)")
        self.assertEqual(html, '<video src="/videos/vid.mp4" controls></video>')


    def test_basic_video_markdown_with_paths(self):
        html = create_video_html("!(v)", paths={"s": "A", "v": "B"})
        self.assertEqual(html, '<video src="B" controls></video>')


    def test_basic_video_markdown_with_failed_paths(self):
        html = create_video_html("!(x)", paths={"s": "A", "v": "B"})
        self.assertEqual(html, '<video src="x" controls></video>')



class YouTubeHtmlTests(TestCase):

    def test_youtube_markdown(self):
        html = create_youtube_html("!{zhbnwPAlKxs}")
        self.assertEqual(
         html,
         '<div class="youtube"><iframe src="//www.youtube.com/embed/zhbnwPAlKxs/"'
         ' frameborder="0" allowfullscreen></iframe></div>'
        )



class CharacterEscaping(TestCase):

    def test_can_escape_no_characters(self):
        self.assertEqual(escape_characters("abcde"), ("abcde", []))


    def test_can_escape_characters(self):
        self.assertEqual(escape_characters("\\abc\\de"), ("\x1abc\x1ae", ["a", "d"]))



class BlockHtmlTests(TestCase):

    def setUp(self):
        self.patcher1 = patch("docupy.markdown.create_paragraph_html")
        self.patcher2 = patch("docupy.markdown.create_heading_html")
        self.patcher3 = patch("docupy.markdown.create_image_html")
        self.patcher4 = patch("docupy.markdown.create_video_html")
        self.patcher5 = patch("docupy.markdown.create_youtube_html")
        self.patcher6 = patch("docupy.markdown.escape_characters")
        self.mock_p = self.patcher1.start()
        self.mock_head = self.patcher2.start()
        self.mock_img = self.patcher3.start()
        self.mock_vid = self.patcher4.start()
        self.mock_tube = self.patcher5.start()
        self.mock_escape = self.patcher6.start()
        self.mock_escape.side_effect = lambda b: (b, [])


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        self.patcher5.stop()
        self.patcher6.stop()


    def test_can_pass_to_paragraph_converter(self):
        self.mock_p.return_value = "P"
        self.assertEqual(create_block_html("This is just a ![paragraph](th)."), "P")
        self.mock_p.assert_called_with("This is just a ![paragraph](th).")


    def test_can_pass_to_heading_converter(self):
        self.mock_head.return_value = "H"
        self.assertEqual(create_block_html("###   Heading"), "H")
        self.mock_head.assert_called_with("###   Heading")


    def test_can_pass_to_image_converter(self):
        self.mock_img.return_value = "I"
        self.assertEqual(create_block_html("![title](file)"), "I")
        self.mock_img.assert_called_with("![title](file)", paths=None)
        self.assertEqual(create_block_html("![title][cap](file)", paths="P"), "I")
        self.mock_img.assert_called_with("![title][cap](file)", paths="P")


    def test_can_pass_to_video_converter(self):
        self.mock_vid.return_value = "V"
        self.assertEqual(create_block_html("!(file)", paths=None), "V")
        self.mock_vid.assert_called_with("!(file)", paths=None)
        self.assertEqual(create_block_html("!(file)", paths="P"), "V")
        self.mock_vid.assert_called_with("!(file)", paths="P")


    def test_can_pass_to_youtube_converter(self):
        self.mock_tube.return_value = "Y"
        self.assertEqual(create_block_html("!{code}"), "Y")
        self.mock_tube.assert_called_with("!{code}")


    def test_can_escape_characters(self):
        self.mock_escape.side_effect = lambda b: (b, ["1", "2"])
        self.mock_p.return_value = "\x1aP\x1a"
        self.assertEqual(create_block_html("This is a paragraph."), "1P2")
        self.mock_p.assert_called_with("This is a paragraph.")



class MarkdownSplittingTests(TestCase):

    def test_single_line_returns_single_block(self):
        blocks = markdown_to_blocks("A line.")
        self.assertEqual(blocks, ["A line."])


    def test_one_line_break_not_enough(self):
        blocks = markdown_to_blocks("A line.\nA second line?")
        self.assertEqual(blocks, ["A line. A second line?"])


    def test_can_break_into_blocks(self):
        blocks = markdown_to_blocks("A line.\n\nA second line\n\nThird line")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_empty_lines_ignored(self):
        blocks = markdown_to_blocks("A line.\n\n\n\nA second line\n\n\nThird line\n")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_windows_line_breaks(self):
        blocks = markdown_to_blocks("A line.\r\n\r\nA second line")
        self.assertEqual(blocks, ["A line.", "A second line"])



class MarkdownToHtmlTests(TestCase):

    @patch("docupy.markdown.markdown_to_blocks")
    @patch("docupy.markdown.create_block_html")
    def test_can_convert_markdown_to_html(self, mock_html, mock_blocks):
        mock_blocks.return_value = ["block1", "block2"]
        mock_html.side_effect = ["html1", "html2"]
        html = markdown_to_html("markdown")
        mock_blocks.assert_called_with("markdown")
        mock_html.assert_any_call("block1", paths=None)
        mock_html.assert_any_call("block2", paths=None)
        self.assertEqual(html, "html1\nhtml2")


    @patch("docupy.markdown.markdown_to_blocks")
    @patch("docupy.markdown.create_block_html")
    def test_can_convert_markdown_to_html_with_paths(self, mock_html, mock_blocks):
        mock_blocks.return_value = ["block1", "block2"]
        mock_html.side_effect = ["html1", "html2"]
        html = markdown_to_html("markdown", paths="P")
        mock_blocks.assert_called_with("markdown")
        mock_html.assert_any_call("block1", paths="P")
        mock_html.assert_any_call("block2", paths="P")
        self.assertEqual(html, "html1\nhtml2")
