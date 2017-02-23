"""Functions for processing raw markdown."""

def split(raw_text):
    """Takes a chunk of raw markdown and splits it into blocks.

    :param str raw_text: The raw markdown.
    :rtype: ``list``"""

    return raw_text.replace("\r\n", "\n").split("\n\n")
