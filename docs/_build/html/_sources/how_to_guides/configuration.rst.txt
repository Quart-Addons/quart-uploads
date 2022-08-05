.. _configuration:

=============
Configuration  
=============

If you're just deploying an application that uses Quarts-Uploads, you can
customize its behavior extensively from the application's configuration.
Check the application's documentation or source code to see how it loads its
configuration.

The settings below apply for a single set of uploads, replacing `FILES` with
the name of the set (i.e. `PHOTOS`, `ATTACHMENTS`):

`UPLOADED_FILES_DEST`
    This indicates the directory uploaded files will be saved to.

`UPLOADED_FILES_URL`
    If you have a server set up to serve the files in this set, this should be
    the URL they are publicly accessible from. Include the trailing slash.

`UPLOADED_FILES_ALLOW`
    This lets you allow file extensions not allowed by the upload set in the
    code.

`UPLOADED_FILES_DENY`
    This lets you deny file extensions allowed by the upload set in the code.

To save on configuration time, there are two settings you can provide
that apply as "defaults" if you don't provide the proper settings otherwise.

`UPLOADS_DEFAULT_DEST`
    If you set this, then if an upload set's destination isn't otherwise
    declared, then its uploads will be stored in a subdirectory of this
    directory. For example, if you set this to ``/var/uploads``, then a set
    named photos will store its uploads in ``/var/uploads/photos``.

`UPLOADS_DEFAULT_URL`
    If you have a server set up to serve from `UPLOADS_DEFAULT_DEST`, then
    set the server's base URL here. Continuing the example above, if
    ``/var/uploads`` is accessible from ``http://localhost:5001``, then you
    would set this to ``http://localhost:5001/`` and URLs for the photos set
    would start with ``http://localhost:5001/photos``. Include the trailing
    slash.

However, you don't have to set any of the ``_URL`` settings - if you don't,
then they will be served internally by Quart. They are just there so if you
have heavy upload traffic, you can have a faster production server.

In order to have the application limit the size of uploaded files set the
Quart defulat configuration variable `MAX_CONTENT_LENGTH`.
