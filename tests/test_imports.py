from unittest import TestCase
import samdown

class MainFunctionImportTests(TestCase):

    def test_main_function_imported(self):
        from samdown.raw import html_from_markdown
        self.assertIs(html_from_markdown, samdown.html_from_markdown)
