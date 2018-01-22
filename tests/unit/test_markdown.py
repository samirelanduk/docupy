from unittest import TestCase
from unittest.mock import patch, Mock
from docupy.markdown import *

class MarkdownToHtmlTests(TestCase):

    def setUp(self):
        self.patcher1 = patch("docupy.markdown.escape_characters")
        self.patcher2 = patch("docupy.markdown.markdown_to_blocks")
        self.patcher3 = patch("docupy.markdown.group_blocks")
        self.patcher4 = patch("docupy.markdown.block_to_html")
        self.patcher5 = patch("docupy.markdown.group_block_to_html")
        self.mock_escape = self.patcher1.start()
        self.mock_blocks = self.patcher2.start()
        self.mock_group = self.patcher3.start()
        self.mock_block2html = self.patcher4.start()
        self.mock_multi2html = self.patcher5.start()


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        self.patcher5.stop()


    def test_can_convert_markdown_to_html(self):
        self.mock_escape.return_value = ("markdown_esc", [])
        self.mock_blocks.return_value = ["block1", "block2"]
        self.mock_group.return_value = ["block1g", "block2g"]
        self.mock_block2html.side_effect = ["html1", "html2"]
        html = markdown_to_html("markdown")
        self.mock_escape.assert_called_with("markdown")
        self.mock_blocks.assert_called_with("markdown_esc")
        self.mock_group.assert_called_with(["block1", "block2"])
        self.mock_block2html.assert_any_call("block1g", paths=None)
        self.mock_block2html.assert_any_call("block2g", paths=None)
        self.assertEqual(html, "html1\nhtml2")


    def test_can_convert_markdown_to_html_with_groups(self):
        self.mock_escape.return_value = ("markdown_esc", [])
        self.mock_blocks.return_value = ["b1", "b2", "b3", "b4", "b5", "b6"]
        self.mock_group.return_value = ["b1", ["b2", "b3", "b4"], ["b5", "b6"]]
        self.mock_block2html.return_value = "h1"
        self.mock_multi2html.side_effect = ["h2\nh3", "h4h5h6"]
        html = markdown_to_html("markdown")
        self.mock_escape.assert_called_with("markdown")
        self.mock_blocks.assert_called_with("markdown_esc")
        self.mock_group.assert_called_with(["b1", "b2", "b3", "b4", "b5", "b6"])
        self.mock_block2html.assert_called_with("b1", paths=None)
        self.mock_multi2html.assert_any_call(["b2", "b3", "b4"])
        self.mock_multi2html.assert_any_call(["b5", "b6"])
        self.assertEqual(html, "h1\nh2\nh3\nh4h5h6")


    def test_can_convert_markdown_to_html_with_escaped_chars(self):
        self.mock_escape.return_value = ("mark\x1adown\x1a\x1a", ["1", "3", "9"])
        self.mock_blocks.return_value = ["block1", "block2"]
        self.mock_group.return_value = ["block1g", "block2g"]
        self.mock_block2html.side_effect = ["html\x1a1", "html2\x1a\x1a"]
        html = markdown_to_html("markdown")
        self.mock_escape.assert_called_with("markdown")
        self.mock_blocks.assert_called_with("mark\x1adown\x1a\x1a")
        self.mock_group.assert_called_with(["block1", "block2"])
        self.mock_block2html.assert_any_call("block1g", paths=None)
        self.mock_block2html.assert_any_call("block2g", paths=None)
        self.assertEqual(html, "html11\nhtml239")


    def test_can_convert_markdown_to_html_with_paths(self):
        self.mock_escape.return_value = ("markdown_esc", [])
        self.mock_blocks.return_value = ["block1", "block2"]
        self.mock_group.return_value = ["block1g", "block2g"]
        self.mock_block2html.side_effect = ["html1", "html2"]
        html = markdown_to_html("markdown", paths="P")
        self.mock_escape.assert_called_with("markdown")
        self.mock_blocks.assert_called_with("markdown_esc")
        self.mock_group.assert_called_with(["block1", "block2"])
        self.mock_block2html.assert_any_call("block1g", paths="P")
        self.mock_block2html.assert_any_call("block2g", paths="P")
        self.assertEqual(html, "html1\nhtml2")



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



class MarkdownToBlockSplittingTests(TestCase):

    def test_single_line_returns_single_block(self):
        blocks = markdown_to_blocks("A line.")
        self.assertEqual(blocks, ["A line."])


    def test_can_break_into_blocks(self):
        blocks = markdown_to_blocks("A line.\nA second line\nThird line")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_empty_lines_ignored(self):
        blocks = markdown_to_blocks("A line.\n\n\nA second line\n\nThird line\n")
        self.assertEqual(blocks, ["A line.", "A second line", "Third line"])


    def test_windows_line_breaks(self):
        blocks = markdown_to_blocks("A line.\r\nA second line")
        self.assertEqual(blocks, ["A line.", "A second line"])



class GroupBlockTests(TestCase):

    def setUp(self):
        self.patcher1 = patch("docupy.markdown.is_multi_block")
        self.check = self.patcher1.start()
        self.blocks = ["1", "2", "3", "4", "5", "6", "7"]


    def tearDown(self):
        self.patcher1.stop()


    def test_can_return_ungrouped_blocks(self):
        self.check.return_value = False
        self.assertEqual(group_blocks(self.blocks[:]), self.blocks)
        for i in range(1, 8):
            self.check.assert_any_call(str(i))


    def test_can_group_blocks(self):
        self.check.side_effect = [False, False, True, True, False, False, False]
        self.assertEqual(group_blocks(self.blocks), ["1", "2", ["3", "4"], "5", "6", "7"])
        for i in range(1, 8):
            self.check.assert_any_call(str(i))


    def test_can_group_multiple_blocks(self):
        self.check.side_effect = [False, True, False, True, True, True, False]
        self.assertEqual(group_blocks(self.blocks), ["1", ["2"], "3", ["4", "5", "6"], "7"])
        for i in range(1, 8):
            self.check.assert_any_call(str(i))


    def test_groups_can_be_at_end(self):
        self.check.side_effect = [True, True, False, False, True, True, True]
        self.assertEqual(group_blocks(self.blocks), [["1", "2"], "3", "4", ["5", "6", "7"]])
        for i in range(1, 8):
            self.check.assert_any_call(str(i))



class BlockHtmlTests(TestCase):

    def setUp(self):
        self.patcher1 = patch("docupy.markdown.create_paragraph_html")
        self.patcher2 = patch("docupy.markdown.create_heading_html")
        self.patcher3 = patch("docupy.markdown.create_image_html")
        self.patcher4 = patch("docupy.markdown.create_video_html")
        self.patcher5 = patch("docupy.markdown.create_youtube_html")
        self.mock_p = self.patcher1.start()
        self.mock_head = self.patcher2.start()
        self.mock_img = self.patcher3.start()
        self.mock_vid = self.patcher4.start()
        self.mock_tube = self.patcher5.start()


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        self.patcher5.stop()


    def test_can_pass_to_paragraph_converter(self):
        self.mock_p.return_value = "P"
        self.assertEqual(block_to_html("This is just a ![paragraph](th)."), "P")
        self.mock_p.assert_called_with("This is just a ![paragraph](th).")


    def test_can_pass_to_heading_converter(self):
        self.mock_head.return_value = "H"
        self.assertEqual(block_to_html("###   Heading"), "H")
        self.mock_head.assert_called_with("###   Heading")


    def test_can_pass_to_image_converter(self):
        self.mock_img.return_value = "I"
        self.assertEqual(block_to_html("![title](file)"), "I")
        self.mock_img.assert_called_with("![title](file)", paths=None)
        self.assertEqual(block_to_html("![title][cap](file)", paths="P"), "I")
        self.mock_img.assert_called_with("![title][cap](file)", paths="P")


    def test_can_pass_to_video_converter(self):
        self.mock_vid.return_value = "V"
        self.assertEqual(block_to_html("!(file)", paths=None), "V")
        self.mock_vid.assert_called_with("!(file)", paths=None)
        self.assertEqual(block_to_html("!(file)", paths="P"), "V")
        self.mock_vid.assert_called_with("!(file)", paths="P")


    def test_can_pass_to_youtube_converter(self):
        self.mock_tube.return_value = "Y"
        self.assertEqual(block_to_html("!{code}"), "Y")
        self.mock_tube.assert_called_with("!{code}")



class GroupBlockHtmlTests(TestCase):

    def setUp(self):
        self.patcher1 = patch("docupy.markdown.create_list_html")
        self.mock_list = self.patcher1.start()


    def tearDown(self):
        self.patcher1.stop()


    def test_can_pass_to_list_converter(self):
        self.mock_list.return_value = "L"
        self.assertEqual(group_block_to_html(["- Item 1", "- Item 2"]), "L")
        self.mock_list.assert_called_with(["- Item 1", "- Item 2"])



class MultiBlockCheckTests(TestCase):

    def test_can_return_false(self):
        self.assertFalse(is_multi_block("just a line"))


    def test_can_return_true_for_bullet(self):
        self.assertTrue(is_multi_block("-a line"))
        self.assertTrue(is_multi_block("- a line"))
        self.assertTrue(is_multi_block("-  a line"))


    def test_can_return_true_for_number(self):
        self.assertTrue(is_multi_block("1.a line"))
        self.assertTrue(is_multi_block("2. a line"))
        self.assertTrue(is_multi_block("309.  a line"))



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



class ListHtmlTests(TestCase):

    def test_can_create_bullet_html(self):
        html = create_list_html(["-item1", "- item2", "-  item3"])
        self.assertEqual(
         html, "<ul>\n<li>item1</li>\n<li>item2</li>\n<li>item3</li>\n</ul>"
        )


    def test_can_create_number_html(self):
        html = create_list_html(["1. item1", "2.item2", "345.    item3"])
        self.assertEqual(
         html, "<ol>\n<li>item1</li>\n<li>item2</li>\n<li>item3</li>\n</ol>"
        )
