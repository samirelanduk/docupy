Overview
--------

Creating HTML
~~~~~~~~~~~~~

The :py:func:`.markdown_to_html` function takes Markdown text and returns the
equivalent HTML.

  >>> import docupy
  >>> docupy.markdown_to_html("HTML is easy.")
  '<p>HTML is easy.</p>'
  >>> docupy.markdown_to_html("HTML is easy.\n\nNew paragraph.\r\n\r\nThird.")
  '<p>HTML is easy.</p>\n<p>New paragraph.</p>\n<p>Third.</p>'

Formatting
~~~~~~~~~~

Basic formatting is applied as follows:

* `Italics` text is created by \*surrounding with asterisks\*.

* **Bold** text is created by \*\*surrounding with double asterisks\*\*.

* `Links <https://samireland.com/>`_ are created like: \[text\]\(path).

* External links use curly braces: \{text\}\(path).

* Strikethrough text uses tildes: ~~deleted text~~.


Special Blocks
~~~~~~~~~~~~~~

Headings begin with ``#`` characters. One is a ``<h1>``, two is a ``<h2>``, and
so on.

Images use ``![alt text](link/to/image)`` notation.

Videos use ``!(link/to/video)`` notation.

YouTube embeds use ``!{youtube_id}`` notation.

Code can be embedded in ` characters.

You can provide a lookup dictionary to substitute words for paths when rendered.
For example the block ``![alt text](seaside-2)`` when rendered with
``{"seaside-2": "path/to/image"}`` will point in the right place.

Group blocks
~~~~~~~~~~~~

Bullet pointed lists (``-``) and numbered lists will be detected automatically.

Security
~~~~~~~~

Any HTML tags in the markdown will be escaped, preventing (among other things)
the arbitrary injection of JavaScript via submitted markdown.


Example
~~~~~~~

.. code-block:: html

  # An example document

  This is the *first* paragraph.

  This is the **second** paragraph.

  This is the ~~second~~ third paragraph.

  ## Some Links

  Here is [a link](https://example.com/).

  [This whole paragraph is a link.](https://example2.com/)

  ### Special Example...

  {This link}(https://example3.com/) opens in a new tab.

  You [can](https://example.com/) have {multiple}(https://example3.com/) links!

  ## Media

  ![Image here!](/images/logo.png)

  !(/videos/vid.mp4)

  !{zhbnwPAlKxs}

  ### Inline Media

  \!As a side note, incorporating !{blocks} in paragraphs has no
  effect. See - !(/videos/vid.mp4).

  ## Escaping

  You can escape characters like \*this\* and \[this](see!).

  <script>Evil Javascript</script>

...becomes...

.. code-block:: html

  <h1>An example document</h1>
  <p>This is the <em>first</em> paragraph.</p>
  <p>This is the <strong>second</strong> paragraph.</p>
  <p>This is the <del>second</del> third paragraph.</p>
  <h2>Some Links</h2>
  <p>Here is <a href="https://example.com/">a link</a>.</p>
  <p><a href="https://example2.com/">This whole paragraph is a link.</a></p>
  <h3>Special Example...</h3>
  <p><a href="https://example3.com/" target="_blank">This link</a> opens in a new tab.</p>
  <p>You <a href="https://example.com/">can</a> have <a href="https://example3.com/" target="_blank">multiple</a> links!</p>
  <h2>Media</h2>
  <figure><img src="/images/logo.png" title="Image here!"></figure>
  <video src="/videos/vid.mp4" controls></video>
  <div class="youtube"><iframe src="//www.youtube.com/embed/zhbnwPAlKxs/" frameborder="0" allowfullscreen></iframe></div>
  <h3>Inline Media</h3>
  <p>!As a side note, incorporating !{blocks} in paragraphs has no effect. See - !(/videos/vid.mp4).</p>
  <h2>Escaping</h2>
  <p>You can escape characters like *this* and [this](see!).</p>
  <p>&#60;script&#62;Evil Javascript&#60;/script&#62;</p>
