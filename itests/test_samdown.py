from unittest import TestCase
import django_samdown

class Tests(TestCase):

    def test_process_samdown(self):
        raw = "\n\n".join([
         "This *is* some _formatted_ text.",
         "**Isn't it great?**"
        ])

        html = django_samdown.html_from_samdown(raw)

        self.assertEqual("\n".join([
         "<p>This <em>is</em> some <u>formatted</u> text.</p>",
         "<p><b>Isn't it great?</b></p>"
        ]), html)
