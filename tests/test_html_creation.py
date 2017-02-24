from unittest import TestCase
from unittest.mock import patch, Mock
from samdown.raw import html_from_markdown

class Markdown2HtmlTests(TestCase):

    @patch("samdown.raw.process_block")
    @patch("samdown.raw.split")
    def test_html_from_markdown_correct_functions(self, mock_splitter, mock_processer):
        mock_splitter.return_value = [Mock(), Mock(), Mock()]
        mock_processer.side_effect = ["<p>1</p>", "<p>2</p>", "<p>3</p>"]
        markdown = "markdown"
        html = html_from_markdown(markdown)
        self.assertEqual(
         html,
         "\n".join(["<p>1</p>", "<p>2</p>", "<p>3</p>"])
        )
