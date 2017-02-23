from unittest import TestCase
from samdown.block import process_block

class BasicParagraphTests(TestCase):

    def test_can_turn_block_into_paragraph(self):
        self.assertEqual(process_block("Text block."), "<p>Text block.</p>")
