from unittest import TestCase
from docupy.markdown import text_to_blocks

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
