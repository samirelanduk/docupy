"""This module contains for functions for parsing markdown."""

def markdown_to_html(markdown):
    blocks = text_to_blocks(markdown)
    return "\n".join(blocks)


def text_to_blocks(text):
    blocks = text.replace("\r\n", "\n").split("\n\n")
    blocks = [block.strip().replace("\n", " ") for block in blocks]
    blocks = list(filter(bool, blocks))
    return blocks


def block_to_html(block):
    if block[0] == "!" or block [0] == "#":
        return create_special_html(block)
    return create_paragraph_html(block)


def create_special_html(block):
    pass


def create_paragraph_html(block):
    pass
