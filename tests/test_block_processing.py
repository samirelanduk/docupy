from unittest import TestCase
from django_samdown.block import process_block

class BasicParagraphTests(TestCase):

    def test_can_turn_block_into_paragraph(self):
        self.assertEqual(
         process_block("Text block.", {"inline": {}, "block": {}}),
         "<p>Text block.</p>"
        )


    def test_can_make_inline_replacements(self):
        self.assertEqual(
        "<p><u>Text</u> <u>block</u>.</p>",
         process_block(
          "_Text_ _block_.",
          {"inline": {r"_(.*?)_": r"<u>\1</u>"}, "block": {}}
         )
        )



class BlockTests(TestCase):

    def test_can_make_block_replacements(self):
        self.assertEqual(
        "<img src='/static/west'>",
         process_block(
          "<IMAGE>[west]",
          {"inline": {}, "block": {r"\<IMAGE\>\[(.*?)\]": r"<img src='/static/\1'>"}}
         )
        )


    def test_block_replacements_only_check_edges(self):
        self.assertEqual(
        "<p>s<IMAGE>[west]</p>",
         process_block(
          "s<IMAGE>[west]",
          {"inline": {}, "block": {r"\<IMAGE\>\[(.*?)\]": r"<img src='/static/\1'>"}}
         )
        )


    def test_inline_replacements_not_done_on_block_replacements(self):
        self.assertEqual(
        "<img src='/static/we_s_t'>",
         process_block(
          "<IMAGE>[we_s_t]",
          {
           "inline": {r"_(.*?)_": r"<u>\1</u>"},
           "block": {r"\<IMAGE\>\[(.*?)\]": r"<img src='/static/\1'>"}
          }
         )
        )


    def test_can_take_functions(self):
        f = lambda k: k.upper()
        self.assertEqual(
         "<IMAGE>[WEST]",
         process_block(
          "<IMAGE>[west]",
          {"inline": {}, "block": {r"\<IMAGE\>\[(.*?)\]": f}}
         )
        )
