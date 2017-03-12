Overview
--------

Creating HTML
~~~~~~~~~~~~~

The :py:func:`.html_from_markdown` function takes Markdown text and returns the
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
