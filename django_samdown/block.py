"""Functions for turning markdown blocks into HTML elements."""

import re

def process_block(block, lookup):
    """Takes a block of Markdown and returns the correct HTML for that
    block, based on its contents."""

    for pattern in lookup:
        block = re.sub(pattern, lookup[pattern], block)

    return "<p>%s</p>" % block
