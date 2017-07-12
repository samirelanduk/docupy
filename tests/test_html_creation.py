from unittest import TestCase
from unittest.mock import patch, Mock
from django_samdown.raw import html_from_markdown

class Markdown2HtmlTests(TestCase):

    @patch("django_samdown.raw.get_lookup")
    @patch("django_samdown.raw.process_block")
    @patch("django_samdown.raw.split")
    def test_html_from_markdown_correct_functions(self, mock_split, mock_process, mock_lookup):
        mock_lookup.return_value = {"a": "b"}
        block1, block2, block3 = Mock(), Mock(), Mock()
        mock_split.return_value = [block1, block2, block3]
        mock_process.side_effect = ["<p>1</p>", "<p>2</p>", "<p>3</p>"]
        markdown = "markdown"
        html = html_from_markdown(markdown)
        mock_split.assert_called_with("markdown")
        mock_process.assert_any_call(block1, {"a": "b"})
        mock_process.assert_any_call(block2, {"a": "b"})
        mock_process.assert_any_call(block3, {"a": "b"})
        self.assertEqual(
         html,
         "\n".join(["<p>1</p>", "<p>2</p>", "<p>3</p>"])
        )
