"""
quart_uploads.utils
"""
import asyncio
import os

from quart import Quart
from werkzeug.datastructures import FileStorage

__all__ = ['extension', 'lowercase_ext', 'addslash', 'patch_request_class',
          'TestingFileStorage']

def extension(filename: str) -> str:
    """
    Returns the extension used for a file.
    """
    ext = os.path.splitext(filename)[1]
    if ext == '':
        # add non-ascii filename support
        ext = os.path.splitext(filename)[0]
    if ext.startswith('.'):
        # os.path.splitext retains . separator
        ext = ext[1:]
    return ext


def lowercase_ext(filename: str) -> str:
    """
    This is a helper used by UploadSet.save to provide lowercase extensions for
    all processed files, to compare with configured extensions in the same
    case.
    :param filename: The filename to ensure has a lowercase extension.
    """
    if '.' in filename:
        main, ext = os.path.splitext(filename)
        return main + ext.lower()
    # For consistency with os.path.splitext,
    # do not treat a filename without an extension as an extension.
    # That is, do not return filename.lower().
    return filename


def addslash(url: str) -> str:
    """
    Adds an end slash to a url.
    """
    if url.endswith('/'):
        return url
    return url + '/'

def patch_request_class(app: Quart, size=64 * 1024 * 1024) -> None:
    """
    By default, Flask will accept uploads to an arbitrary size. While Werkzeug
    switches uploads from memory to a temporary file when they hit 500 KiB,
    it's still possible for someone to overload your disk space with a
    gigantic file.
    This patches the app's request class's
    `~werkzeug.BaseRequest.max_content_length` attribute so that any upload
    larger than the given size is rejected with an HTTP error.
    .. note::
       In Flask 0.6, you can do this by setting the `MAX_CONTENT_LENGTH`
       setting, without patching the request class. To emulate this behavior,
       you can pass `None` as the size (you must pass it explicitly). That is
       the best way to call this function, as it won't break the Flask 0.6
       functionality if it exists.
    .. versionchanged:: 0.1.1
    :param app: The app to patch the request class of.
    :param size: The maximum size to accept, in bytes. The default is 64 MiB.
                 If it is `None`, the app's `MAX_CONTENT_LENGTH` configuration
                 setting will be used to patch.
    """
    if size is None:
        if isinstance(app.request_class.__dict__['max_content_length'],
                      property):
            return
        size = app.config.get('MAX_CONTENT_LENGTH')
    reqclass = app.request_class
    patched = type(reqclass.__name__, (reqclass,),
                   {'max_content_length': size})
    app.request_class = patched

class TestingFileStorage(FileStorage):
    """
    This is a helper for testing upload behavior in your application. You
    can manually create it, and its save method is overloaded to set `saved`
    to the name of the file it was saved to. All of these parameters are
    optional, so only bother setting the ones relevant to your application.
    :param stream: A stream. The default is an empty stream.
    :param filename: The filename uploaded from the client. The default is the
                     stream's name.
    :param name: The name of the form field it was loaded from. The default is
                 `None`.
    :param content_type: The content type it was uploaded as. The default is
                         ``application/octet-stream``.
    :param content_length: How long it is. The default is -1.
    :param headers: Multipart headers as a `werkzeug.Headers`. The default is
                    `None`.
    """
    def __init__(self, stream=None, filename=None, name=None,
                 content_type='application/octet-stream', content_length=-1,
                 headers=None):
        FileStorage.__init__(self, stream, filename, name=name,
            content_type=content_type, content_length=content_length,
            headers=None)
        self.saved = None

    async def save(self, dst, buffer_size=16384):
        """
        This marks the file as saved by setting the `saved` attribute to the
        name of the file it was saved to.
        :param dst: The file to save to.
        :param buffer_size: Ignored.
        """
        await asyncio.sleep(0.2)

        if isinstance(dst, str):
            self.saved = dst
        else:
            self.saved = dst.name
