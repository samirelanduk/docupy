from unittest import TestCase
from unittest.mock import patch
from django_samdown.raw import get_lookup

class LookupGenerationTests(TestCase):

    @patch("django_samdown.raw.settings")
    def test_default_lookup_is_basic_formatting(self, mock_settings):
        self.assertEqual(get_lookup(), {
         r"_(.*?)_": r"<u>\1</u>",
         r"\*\*(.*?)\*\*": r"<b>\1</b>",
         r"\*(.*?)\*": r"<em>\1</em>",
        })


    @patch("django_samdown.raw.settings")
    def test_can_get_extra_formatting(self, mock_settings):
        mock_settings.SAMDOWN_LOOKUP = {
         r"aaa": r"bbb",
         r"ccc": r"ddd",
        }
        self.assertEqual(get_lookup(), {
         r"_(.*?)_": r"<u>\1</u>",
         r"\*\*(.*?)\*\*": r"<b>\1</b>",
         r"\*(.*?)\*": r"<em>\1</em>",
         r"aaa": r"bbb",
         r"ccc": r"ddd",
        })


    @patch("django_samdown.raw.settings")
    def test_can_extra_formatting_takes_priority(self, mock_settings):
        mock_settings.SAMDOWN_LOOKUP = {
         r"aaa": r"bbb",
         r"ccc": r"ddd",
         r"_(.*?)_": r"<D>\1</D>",
        }
        self.assertEqual(get_lookup(), {
         r"_(.*?)_": r"<D>\1</D>",
         r"\*\*(.*?)\*\*": r"<b>\1</b>",
         r"\*(.*?)\*": r"<em>\1</em>",
         r"aaa": r"bbb",
         r"ccc": r"ddd",
        })
