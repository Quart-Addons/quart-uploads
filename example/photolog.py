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