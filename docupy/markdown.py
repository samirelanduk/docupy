"""This module contains for functions for parsing markdown."""

import re

def create_paragraph_html(block, p=True):
    """Converts a paragraph markdown block to its HTML equivalent.

    :param str block: The block to convert.
    :param bool p: If ``false``, the enclosing <p> tags will be omitted.
    :rtype: ``str``"""

    block = re.sub(
     r"\{(.*?)\}\((.*?) \"(.*?)\"\)",
     r'<a href="\2" target="_blank" title="\3">\1</a>', block
    )
    block = re.sub(
     r"\{(.*?)\}\((.*?)\)", r'<a href="\2" target="_blank">\1</a>', block
    )
    block = re.sub(
     r"\[(.*?)\]\((.*?) \"(.*?)\"\)", r'<a href="\2" title="\3">\1</a>', block
    )
    block = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', block)
    block = re.sub(r"\~\~(.*?)\~\~", r"<del>\1</del>", block)
    block = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", block)
    block = re.sub(r"\*(.*?)\*", r"<em>\1</em>", block)
    return "<p>{}</p>".format(block) if p else block


def create_heading_html(block):
    """Converts a heading markdown block to HTML. The heading level will depend
    on the number of # characters, and there is no upper limit.

    :param str block: The block to convert."""

    start = re.search(r"[^#]", block).start()
    level = block[:start].count("#")
    return "<h{}>{}</h{}>".format(level, block[start:].strip(), level)


def create_image_html(block, paths=None):
    """Converts an image markdown block to HTML. It accepts blocks with or
    without figcaption sections.

    :param str block: The block to convert.
    :param dict paths: If given, these will be used to translate any paths.
    :rtype: ``str``"""

    title, *mid, path = re.compile(
     r"\!\[(.*?)\](\[.*?\])?\((.*?)\)"
    ).findall(block)[0]
    if paths: path = paths.get(path, path)
    caption = ""
    if mid and mid[0]:
        caption = "<figcaption>{}</figcaption>".format(
         create_paragraph_html(mid[0][1:-1], p=False)
        )
    return '<figure><img src="{}" title="{}">{}</figure>'.format(
     path, title, caption
    )


def create_video_html(block, paths=None):
    """Converts a video markdown block to HTML.

    :param str block: The block to convert.
    :param dict paths: If given, these will be used to translate any paths.
    :rtype: ``str``"""

    path = re.compile(r"\!\((.*?)\)").findall(block)[0]
    if paths: path = paths.get(path, path)
    return '<video src="{}" controls></video>'.format(path)


def create_youtube_html(block):
    """Converts a youtube markdown block to HTML.

    :param str block: The block to convert."""

    v = re.compile(r"\!\{(.*?)\}").findall(block)[0]
    return ('<div class="youtube"><iframe src="//www.youtube.com/embed/{}/"' +
    ' frameborder="0" allowfullscreen></iframe></div>').format(v)


def escape_characters(block):
    """Takes a block and replaces escaped characters with the substition
    character. This is returned along with a list of escaped characters.

    :param str text: The string to break up.
    :rtype: ``str``, ``list``"""

    characters = []
    while "\\" in block:
        location = block.find("\\")
        if location != len(block) - 1:
            characters.append(block[location + 1])
            block = block[:location] + "\x1A" + block[location + 2:]
        else:
            block = block[:-1]
    return block, characters


def create_block_html(block, paths=None):
    """Converts a Markdown block to the relevant HTML.

    :param str text: The string to break up.
    :rtype: ``list``"""

    block, characters = escape_characters(block)
    html = ""
    if block[0] == "#":
        html = create_heading_html(block)
    elif re.compile(r"\!\[(.*?)\](\[.*?\])?\((.*?)\)").match(block):
        html =  create_image_html(block, paths=paths)
    elif re.compile(r"\!\((.*?)\)").match(block):
        html =  create_video_html(block, paths=paths)
    elif re.compile(r"\!\{(.*?)\}").match(block):
        html =  create_youtube_html(block)
    else:
        html = create_paragraph_html(block)
    for char in characters:
        html = html.replace("\x1A", char, 1)
    return html


def markdown_to_blocks(text):
    """Breaks a string into a list of blocks, using double line breaks.
    Windows line breaks (``\\r\\n``) are supported.

    :param str text: The string to break up.
    :rtype: ``list``"""

    blocks = text.replace("\r\n", "\n").split("\n\n")
    blocks = [block.strip().replace("\n", " ") for block in blocks]
    blocks = list(filter(bool, blocks))
    return blocks


def markdown_to_html(markdown, paths=None):
    """Takes a string in markdown, and converts it to HTML. There must be two
    line breaks between separate blocks.

    :param str markdown: The maekdown to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    blocks = markdown_to_blocks(markdown)
    html_blocks = [create_block_html(block, paths=paths) for block in blocks]
    return "\n".join(html_blocks)
