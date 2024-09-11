"""
quart_uploads.utils
"""
import asyncio
import os
from typing import Any, IO

from quart.datastructures import FileStorage
from werkzeug.datastructures import Headers


def extension(filename: str) -> str:
    """
    Returns the extension used for a file.

    Arguments:
        filename: The filename to get the extension.
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

    Arguments:
        filename: The filename to ensure has a lowercase extension.
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

    argument:
        url: The url to add an end slash to.
    """
    if url.endswith('/'):
        return url
    return url + '/'


class TestingFileStorage(FileStorage):
    """
    This is a helper for testing upload behavior in your application. You
    can manually create it, and its save method is overloaded to set `saved`
    to the name of the file it was saved to. All of these parameters are
    optional, so only bother setting the ones relevant to your application.

    Arguments:
        stream: A stream. The default is an empty stream.
        filename: The filename uploaded from the client. The default is the
            stream's name.
        name: The name of the form field it was loaded from. The default is
            `None`.
        content_type: The content type it was uploaded as. The default is
            ``application/octet-stream``.
        content_length: How long it is. The default is -1.
        headers: Multipart headers as a `werkzeug.Headers`. The default is
        `None`.
    """
    def __init__(
            self, stream: IO[bytes] | None = None,
            filename: str | None = None,
            name: str | None = None,
            content_type: str | None = None,
            content_length: int | None = None,
            headers: Headers | None = None
    ) -> None:
        super().__init__(
            stream, filename, name, content_type, content_length, headers
        )
        self.saved: Any | None = None

    async def save(
            self, destination: Any, buffer_size: int = 16384
    ) -> None:
        """
        This marks the file as saved by setting the `saved` attribute to the
        name of the file it was saved to.

        Arguments:
            :destination: The file to save to.
            :buffer_size: Ignored.
        """
        await asyncio.sleep(0.2)

        if isinstance(destination, str):
            self.saved = destination
        else:
            self.saved = destination.name
