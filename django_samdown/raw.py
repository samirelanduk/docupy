from .block import process_block
from django.conf import settings

"""Functions for processing raw markdown."""

def split(raw_text):
    """Takes a chunk of raw markdown and splits it into blocks.

    :param str raw_text: The raw markdown.
    :rtype: ``list``"""

    return raw_text.replace("\r\n", "\n").split("\n\n")


def get_lookup():
    lookup = {
     r"_(.*?)_": r"<u>\1</u>",
     r"\*\*(.*?)\*\*": r"<b>\1</b>",
     r"\*(.*?)\*": r"<em>\1</em>",
    }
    extra = getattr(settings, "SAMDOWN_LOOKUP", {})
    lookup.update(extra)
    return lookup


def html_from_markdown(samdown):
    """Converts markdown text into HTML.

    :param str markdown: The markdown text to convert to HTML.
    :rtype: ``str``"""

    lookup = get_lookup()

    return "\n".join([process_block(block, lookup) for block in split(samdown)])
