from unittest import TestCase
from django_samdown.block import process_block

class BasicParagraphTests(TestCase):

    def test_can_turn_block_into_paragraph(self):
        self.assertEqual(process_block("Text block.", {}), "<p>Text block.</p>")


    def test_can_make_inline_replacements(self):
        self.assertEqual(
         process_block("_Text_ _block_.", {r"_(.*?)_": r"<u>\1</u>"}),
         "<p><u>Text</u> <u>block</u>.</p>"
        )
