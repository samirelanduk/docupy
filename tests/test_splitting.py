from unittest import TestCase
from samdown.raw import split

class NoSplitTests(TestCase):

    def test_single_line_doesnt_split(self):
        self.assertEqual(split("A single line"), ["A single line"])



class CanSplitTests(TestCase):

    def test_can_split_on_double_line(self):
        self.assertEqual(
         split("A single line\n\nSecond line"),
         ["A single line", "Second line"]
        )
