.. _ascii:

==========================
Non-ASCII Filename Support
==========================

Quart-Uplaods use Werkzeug's ``secure_filename()`` to check filename, it will omit
Non-ASCII string. When the filename is completely consist of Non-ASCII string, 
such as Chinese or Japanese, it will return empty filename like ``.jpg``. If your 
files may encounter a situation like this, you have to set it's name or generate 
random filename:

.. code-block:: python 
    uset.save(file, name='photo_123.')
    # If name ends with a dot, the file's extension will be appended to the end.