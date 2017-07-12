from unittest import TestCase
import django_samdown

class MainFunctionImportTests(TestCase):

    def test_main_function_imported(self):
        from django_samdown.raw import html_from_markdown
        self.assertIs(html_from_markdown, django_samdown.html_from_markdown)
