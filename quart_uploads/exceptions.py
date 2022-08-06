"""
quart_uploads.exceptions

Provides exceptions for the app.
"""

__all__ = ['UploadNotAllowed', 'AllExcept']

class UploadNotAllowed(Exception):
    """
    This exception is raised if the upload was not allowed. You should catch
    it in your view code and display an appropriate message to the user.
    """

class AllExcept(object):
    """
    This can be used to allow all file types except certain ones. For example,
    to ban .exe and .iso files, pass::

        AllExcept(('exe', 'iso'))

    to the `UploadSet` constructor as `extensions`. You can use any container,
    for example::

        AllExcept(SCRIPTS + EXECUTABLES)
    """
    def __init__(self, items):
        self.items = items

    def __contains__(self, item):
        return item not in self.items
