"""This module contains for functions for parsing markdown."""

def markdown_to_html(markdown):
    blocks = text_to_blocks(markdown)
    return "\n".join(blocks)


def text_to_blocks(text):
    blocks = text.replace("\r\n", "\n").split("\n\n")
    blocks = [block.strip().replace("\n", " ") for block in blocks]
    blocks = list(filter(bool, blocks))
    return blocks
