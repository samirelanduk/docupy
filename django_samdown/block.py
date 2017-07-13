"""Functions for turning markdown blocks into HTML elements."""

import re

def process_block(block, lookup):
    """Takes a block of Markdown and returns the correct HTML for that
    block, based on its contents."""

    for pattern in lookup["block"]:
        compiled = re.compile(pattern)
        if compiled.match(block):
            if isinstance(lookup["block"][pattern], str):
                block = re.sub(pattern, lookup["block"][pattern], block)
            else:
                block = lookup["block"][pattern](block)
            return block
    for pattern in lookup["inline"]:
        block = re.sub(pattern, lookup["inline"][pattern], block)

    return "<p>%s</p>" % block
