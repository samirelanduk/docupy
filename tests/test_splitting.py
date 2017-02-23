from unittest import TestCase
from samdown.raw import split

class NoSplitTests(TestCase):

    def test_single_line_doesnt_split(self):
        self.assertEqual(split("A single line"), ["A single line"])
