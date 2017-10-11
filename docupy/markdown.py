"""This module contains for functions for parsing markdown."""

import re

def markdown_to_html(markdown, paths=None):
    blocks = text_to_blocks(markdown)
    html_blocks = [block_to_html(block, paths=paths) for block in blocks]
    return "\n".join(html_blocks)


def text_to_blocks(text):
    blocks = text.replace("\r\n", "\n").split("\n\n")
    blocks = [block.strip().replace("\n", " ") for block in blocks]
    blocks = list(filter(bool, blocks))
    return blocks


def block_to_html(block, paths=None):
    substituted_characters = []
    html = ""
    while "\\" in block:
        location = block.find("\\")
        if location != len(block) - 1:
            substituted_characters.append(block[location + 1])
            block = block[:location] + "\x1A" + block[location + 2:]
        else:
            block = block[:-1]
    if block[0] == "!" or block[0] == "#":
        html = create_special_html(block, paths=paths)
    else:
        html = create_paragraph_html(block)
    for char in substituted_characters:
        html = html.replace("\x1A", char, 1)
    return html


def create_special_html(block, paths=None):
    if block[0] == "#":
        start = re.search(r"[^#]", block).start()
        level = block[:start].count("#")
        return "<h{}>{}</h{}>".format(level, block[start:].strip(), level)
    else:
        if re.compile(r"\[(.*?)\]\((.*?)\)").match(block[1:]):
            path = re.compile(r"\[(.*?)\]\((.*?)\)").findall(block[1:])[0][1]
            if paths: path = paths.get(path, "")
            return re.sub(
             r"\[(.*?)\]\((.*?)\)",
             r'<figure><img src="{}" title="\1"></figure>'.format(path),
             block[1:]
            )
        elif re.compile(r"\((.*?)\)").match(block[1:]):
            path = re.compile(r"\((.*?)\)").findall(block[1:])[0]
            if paths: path = paths.get(path, "")
            return '<video src="{}" controls></video>'.format(path)
        elif re.compile(r"\{(.*?)\}").match(block[1:]):
            return re.sub(
             r"\{(.*?)\}",
             r'<iframe class="youtube" src="//www.youtube.com/embed'
             r'/\1/" frameborder="0" allowfullscreen></iframe>',
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
