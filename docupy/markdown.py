"""This module contains for functions for parsing markdown."""

import re

def markdown_to_html(markdown):
    blocks = text_to_blocks(markdown)
    html_blocks = [block_to_html(block) for block in blocks]
    return "\n".join(html_blocks)


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
    if block[0] == "#":
        start = re.search(r"[^#]", block).start()
        level = block[:start].count("#")
        return "<h{}>{}</h{}>".format(level, block[start:].strip(), level)
    else:
        if re.compile(r"\[(.*?)\]\((.*?)\)").match(block[1:]):
            return re.sub(
             r"\[(.*?)\]\((.*?)\)",
             r'<figure><img src="\2" title="\1"></figure>',
             block[1:]
            )
    return ""


def create_paragraph_html(block):
    block = re.sub(
     r"\[(.*?)\]\(\{(.*?)\}\)", r'<a href="\2" target="_blank">\1</a>', block
    )
    block = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', block)
    block = re.sub(r"\~\~(.*?)\~\~", r"<del>\1</del>", block)
    block = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", block)
    block = re.sub(r"\*(.*?)\*", r"<em>\1</em>", block)
    return "<p>{}</p>".format(block)
