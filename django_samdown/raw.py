from .block import process_block
from django.conf import settings

"""Functions for processing raw samdown."""

def split(raw_text):
    """Takes a chunk of raw samdown and splits it into blocks.

    :param str raw_text: The raw samdown.
    :rtype: ``list``"""

    return raw_text.replace("\r\n", "\n").split("\n\n")


def get_lookup():
    """Creates a lookup dictionary, using pre-defined rules and the samdown
    settings in your Django application's settings.py file.

    :rtype: ``dict``"""

    lookup = {
     "inline": {
      r"_(.*?)_": r"<u>\1</u>",
      r"\*\*(.*?)\*\*": r"<b>\1</b>",
      r"\*(.*?)\*": r"<em>\1</em>",
     }, "block": {}
    }
    extra = getattr(settings, "SAMDOWN_LOOKUP", {})
    lookup["inline"].update(extra.get("inline", {}))
    lookup["block"].update(extra.get("block", {}))
    return lookup


def html_from_markdown(samdown):
    """Converts samdown text into HTML.

    :param str samdown: The samdown text to convert to HTML.
    :rtype: ``str``"""

    lookup = get_lookup()
    return "\n".join([process_block(block, lookup) for block in split(samdown)])
