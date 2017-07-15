"""Functions for turning samdown blocks into HTML elements."""

import re

def process_block(block, lookup):
    """Takes a block of samdown and returns the correct HTML for that
    block, based on its contents.

    This function requires a lookup dictionary that tells it what regex patterns
    to look for and what to replace those patterns with. This dictionary needs
    a 'inline' subdictionary and a 'block' subdictionary. That is:

    ``{
     'inline': {
      ...
     }, 'block': {
      ...
     }
    }``

    These two sub-dictionaries should have regex expressions as keys, and regex
    replacement expressions as values (although blocks can have functions also).

    :param str block: The block of samdown to turn into HTML.
    :param dict lookup: The lookup dictionary to translate the block with."""

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
