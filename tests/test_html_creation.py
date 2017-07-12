from unittest import TestCase
from unittest.mock import patch, Mock
from django_samdown.raw import html_from_markdown

class Markdown2HtmlTests(TestCase):

    @patch("django_samdown.raw.process_block")
    @patch("django_samdown.raw.split")
    def test_html_from_markdown_correct_functions(self, mock_splitter, mock_processer):
        mock_splitter.return_value = [Mock(), Mock(), Mock()]
        mock_processer.side_effect = ["<p>1</p>", "<p>2</p>", "<p>3</p>"]
        markdown = "markdown"
        html = html_from_markdown(markdown)
        self.assertEqual(
         html,
         "\n".join(["<p>1</p>", "<p>2</p>", "<p>3</p>"])
        )
