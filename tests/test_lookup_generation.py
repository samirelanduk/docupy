from unittest import TestCase
from unittest.mock import patch
from django_samdown.raw import get_lookup

class LookupGenerationTests(TestCase):

    @patch("django_samdown.raw.settings")
    def test_default_lookup_is_basic_formatting(self, mock_settings):
        self.assertEqual(get_lookup(), {
         "inline": {
          r"_(.*?)_": r"<u>\1</u>",
          r"\*\*(.*?)\*\*": r"<b>\1</b>",
          r"\*(.*?)\*": r"<em>\1</em>",
         }, "block": {}
        })


    @patch("django_samdown.raw.settings")
    def test_can_get_extra_formatting(self, mock_settings):
        mock_settings.SAMDOWN_LOOKUP = {
         "inline": {
          r"aaa": r"bbb",
          r"ccc": r"ddd",
         }, "block": {}
        }
        self.assertEqual(get_lookup(), {
         "inline": {
          r"_(.*?)_": r"<u>\1</u>",
          r"\*\*(.*?)\*\*": r"<b>\1</b>",
          r"\*(.*?)\*": r"<em>\1</em>",
          r"aaa": r"bbb",
          r"ccc": r"ddd",
         }, "block": {}
        })


    @patch("django_samdown.raw.settings")
    def test_can_extra_formatting_takes_priority(self, mock_settings):
        mock_settings.SAMDOWN_LOOKUP = {
         "inline": {
          r"aaa": r"bbb",
          r"ccc": r"ddd",
          r"_(.*?)_": r"<D>\1</D>",
         }, "block": {}
        }
        self.assertEqual(get_lookup(), {
         "inline": {
          r"_(.*?)_": r"<D>\1</D>",
          r"\*\*(.*?)\*\*": r"<b>\1</b>",
          r"\*(.*?)\*": r"<em>\1</em>",
          r"aaa": r"bbb",
          r"ccc": r"ddd",
         }, "block": {}
        })


    @patch("django_samdown.raw.settings")
    def test_can_get_block_formatting(self, mock_settings):
        mock_settings.SAMDOWN_LOOKUP = {
         "inline": {
          r"aaa": r"bbb",
          r"ccc": r"ddd",
         }, "block": {
          r"eee": r"fff"
         }
        }
        self.assertEqual(get_lookup(), {
         "inline": {
          r"_(.*?)_": r"<u>\1</u>",
          r"\*\*(.*?)\*\*": r"<b>\1</b>",
          r"\*(.*?)\*": r"<em>\1</em>",
          r"aaa": r"bbb",
          r"ccc": r"ddd",
         }, "block": {
          r"eee": r"fff"
         }
        })


    @patch("django_samdown.raw.settings")
    def test_can_get_handle_missing_dict(self, mock_settings):
        mock_settings.SAMDOWN_LOOKUP = {
         "block": {
          r"eee": r"fff"
         }
        }
        self.assertEqual(get_lookup(), {
         "inline": {
          r"_(.*?)_": r"<u>\1</u>",
          r"\*\*(.*?)\*\*": r"<b>\1</b>",
          r"\*(.*?)\*": r"<em>\1</em>",
         }, "block": {
          r"eee": r"fff"
         }
        })
        mock_settings.SAMDOWN_LOOKUP = {
         "inline": {
          r"eee": r"fff"
         }
        }
        self.assertEqual(get_lookup(), {
         "inline": {
          r"_(.*?)_": r"<u>\1</u>",
          r"\*\*(.*?)\*\*": r"<b>\1</b>",
          r"\*(.*?)\*": r"<em>\1</em>",
          r"eee": r"fff"
         }, "block": {}
        })
