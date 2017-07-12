from unittest import TestCase
from django_samdown.raw import split

class NoSplitTests(TestCase):

    def test_single_line_doesnt_split(self):
        self.assertEqual(split("A single line"), ["A single line"])


    def test_single_line_break_doesnt_split(self):
        self.assertEqual(split("Single line\nSecond"), ["Single line\nSecond"])



class CanSplitTests(TestCase):

    def test_can_split_on_double_line(self):
        self.assertEqual(
         split("A single line\n\nSecond line"),
         ["A single line", "Second line"]
        )


    def test_can_split_on_windows_line_breaks(self):
        self.assertEqual(
         split("A single line\r\n\r\nSecond line"),
         ["A single line", "Second line"]
        )
