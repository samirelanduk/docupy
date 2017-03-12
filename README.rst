samdown
=======

samdown is yet another Python markdown engine.

Example
-------

  >>> import samdown
  >>> samdown.html_from_markdown("HTML is *easy*.")
  '<p>HTML is <em>easy</em>.</p>'



Installing
----------

pip
~~~

samdown can be installed using pip:

``$ pip install samdown``

samdown is written for Python 3. If the above installation fails, it may be
that your system uses ``pip`` for the Python 2 version - if so, try:

``$ pip3 install samdown``

Requirements
~~~~~~~~~~~~

samdown currently has no dependencies.


Overview
--------

Creating HTML
~~~~~~~~~~~~~

The ``html_from_markdown`` function takes Markdown text and returns the
equivalent HTML.

  >>> import samdown
  >>> samdown.html_from_markdown("HTML is easy.")
  '<p>HTML is easy.</p>'

Two line breaks are considered a new paragraph - windows line breaks will be
converted to UNIX ones before processing:

>>> samdown.html_from_markdown("HTML is easy.\n\nNew paragraph.\r\n\r\nThird.")
'<p>HTML is easy.</p>\n<p>New paragraph.</p>\n<p>Third.</p>'

Formatting
~~~~~~~~~~

Basic formatting is applied as follows:

* `Italics` text is created by \*surrounding with asterisks\*.

* **Bold** text is created by \*\*surrounding with double asterisks\*\*.

* Underlined text is created by \_surrounding with underscores\_.


Changelog
---------

Release 0.2.0
~~~~~~~~~~~~~

`12 March 2017`

* Added formatting for bold, italics, and underlined text.


Release 0.1.0
~~~~~~~~~~~~~

`24 February 2017`

* Added basic markdown processing, and paragraph creation.
* Added suport for Windows line breaks.
