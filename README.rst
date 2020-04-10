docupy
======

|travis| |coveralls| |pypi| |version| |commit|

.. |travis| image:: https://api.travis-ci.org/samirelanduk/docupy.svg?branch=0.3.2
  :target: https://travis-ci.org/samirelanduk/docupy/

.. |coveralls| image:: https://coveralls.io/repos/github/samirelanduk/docupy/badge.svg?branch=0.3.2
  :target: https://coveralls.io/github/samirelanduk/docupy/

.. |pypi| image:: https://img.shields.io/pypi/pyversions/docupy.svg
  :target: https://pypi.org/project/docupy/

.. |version| image:: https://img.shields.io/pypi/v/docupy.svg
  :target: https://pypi.org/project/docupy/

.. |commit| image:: https://img.shields.io/github/last-commit/samirelanduk/docupy/0.3.2.svg
  :target: https://github.com/samirelanduk/docupy/tree/0.3.2/


docupy is a Python markdown library.

Example
-------

  >>> import docupy
  >>> docupy.markdown_to_html("HTML is *easy*.")
  '<p>HTML is <em>easy</em>.</p>'





Installing
----------

pip
~~~

docupy can be installed using pip:

``$ pip3 install docupy``

docupy is written for Python 3, and does not support Python 2.

If you get permission errors, try using ``sudo``:

``$ sudo pip3 install docupy``


Development
~~~~~~~~~~~

The repository for docupy, containing the most recent iteration, can be
found `here <http://github.com/samirelanduk/docupy/>`_. To clone the
docupy repository directly from there, use:

``$ git clone git://github.com/samirelanduk/docupy.git``


Requirements
~~~~~~~~~~~~

docupy has no dependencies, compiled or otherwise, and is pure Python.


Overview
--------

Creating HTML
~~~~~~~~~~~~~

The ``markdown_to_html`` function takes Markdown text and returns the
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


Changelog
---------

Release 0.3.2
~~~~~~~~~~~~~

`10 April 2020`

* Line breaks in code blocks now preserved.
* Inline code blocks now supported.


Release 0.3.1
~~~~~~~~~~~~~

`8 January 2018`

* HTML tags in markdown now escaped.


Release 0.3.0
~~~~~~~~~~~~~

`10 November 2018`

* Added code block.

* Simplified markdown to HTML algorithm.


Release 0.2.0
~~~~~~~~~~~~~

`22 January 2018`

* Added figure captions.

* Added bullet point and numbered lists.


Release 0.1.0
~~~~~~~~~~~~~

`15 October 2017`

* Added basic Markdown to HTML:

  * Block identification.

  * Italics and bold.

  * Hyperlinks.

  * Images.

  * Videos.

  * YouTube.
