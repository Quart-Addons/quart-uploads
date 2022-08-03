"""
photolog.py
===========
This is a simple example app for Quart-Uploads. It is a
simple photolog app that lets you submit blog posts that
are photos.
"""
from quart import (Quart, request, url_for, redirect, render_template,
                  flash, session, g)

from quart_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed

DEBUG = False
SECRET_KEY = ('\xa3\xb6\x15\xe3E\xc4\x8c\xbaT\x14\xd1:'
              '\xafc\x9c|.\xc0H\x8d\xf2\xe5\xbd\xd5')

UPLOADED_PHOTOS_DEST = '/tmp/photolog'

