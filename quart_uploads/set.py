"""
quart_uploads.set

Defines the upload set class.
"""
from __future__ import annotations
import os
import pathlib
import posixpath
from typing import Callable, Optional, Tuple, Union, TYPE_CHECKING

import aiofiles.os
from quart import Quart, current_app, url_for
from quart.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .exceptions import UploadNotAllowed
from .file_ext import FILE_EXTENSIONS as FE, All
from .utils import extension, lowercase_ext

if TYPE_CHECKING:
    from .core import Uploads
    from .config import UploadConfig


class UploadSet(object):
    """
    This represents a single set of uploaded files. Each upload set is
    independent of the others. This can be reused across multiple application
    instances, as all configuration is stored on the application object itself
    and found with `quart.current_app`.

    Arguments:
        name: The name of this upload set. It defaults to ``files``, but
              you can pick any alphanumeric name you want. (For simplicity,
              it's best to use a plural noun.)
        extensions: The extensions to allow uploading in this set. The
                    easiest way to do this is to add together the extension
                    presets (for example, ``TEXT + DOCUMENTS + IMAGES``).
                    It can be overridden by the configuration with the
                    `UPLOADED_X_ALLOW` and `UPLOADED_X_DENY` configuration
                    parameters. The default is `DEFAULTS`.
        default_dest: If given, this should be a callable. If you call it
                      with the app, it should return the default upload
                      destination path for that app.
    """

    def __init__(
        self,
        name: str = 'files',
        extensions: Union[Tuple[str], All] = FE.Defaults,
        default_dest: Optional[Union[str, Callable[[Quart], str]]] = None
    ) -> None:
        if not name.isalnum():
            raise ValueError("Name must be alphanumeric (no underscores)")

        self.name = name
        self.extensions = extensions
        self.default_dest = default_dest

        self._config: UploadConfig | None = None

    @property
    def config(self) -> UploadConfig:
        """
        This gets the current configuration. By default, it looks up the
        current application and gets the configuration from there. But if you
        don't want to go to the full effort of setting an application, or it's
        otherwise outside of a request context, set the `_config` attribute to
        an `UploadConfiguration` instance, then set it back to `None` when
        you're done.
        """
        if self._config is None:
            uploads: Uploads = current_app.extensions['uploads']
            self._config = uploads.get(self.name)

        return self._config

    def url(self, filename: str) -> str:
        """
        This function gets the URL a file uploaded to this set would be
        accessed at. It doesn't check whether said file exists.

        :param filename: The filename to return the URL for.
        """
        base = self.config.base_url
        if base is None:
            return url_for('_uploads.uploaded_file', setname=self.name,
                           filename=filename, _external=True)
        else:
            return base + filename

    def path(self, filename: str, folder: Optional[str] = None) -> str:
        """
        This returns the absolute path of a file uploaded to this set. It
        doesn't actually check whether said file exists.

        :param filename: The filename to return the path for.
        :param folder: The subfolder within the upload set previously
                       used to save to.
        """

        if folder is not None:
            target_folder = os.path.join(self.config.destination, folder)
        else:
            target_folder = self.config.destination
        return os.path.join(target_folder, filename)

    def file_allowed(self, basename: str) -> bool:
        """
        This tells whether a file is allowed. It should return `True` if the
        given `werkzeug.FileStorage` object can be saved with the given
        basename, and `False` if it can't. The default implementation just
        checks the extension, so you can override this if you want.

        :param storage: The `werkzeug.FileStorage` to check.
        :param basename: The basename it will be saved under.
        """
        return self.extension_allowed(extension(basename))

    def extension_allowed(self, ext: str) -> bool:
        """
        This determines whether a specific extension is allowed. It is called
        by `file_allowed`, so if you override that but still want to check
        extensions, call back into this.

        :param ext: The extension to check, without the dot.
        """
        return ((ext in self.config.allow) or
                (ext in self.extensions and ext not in self.config.deny))

    def get_basename(self, filename: str) -> str:
        """
        Returns the file basename.
        """
        return lowercase_ext(secure_filename(filename))

    async def save(
        self,
        storage: FileStorage,
        folder: Optional[str] = None,
        name: Optional[str] = None
    ) -> str:
        """
        This coroutine saves a `werkzeug.FileStorage` into this upload set.
        If the upload is not allowed, an `UploadNotAllowed` error will be
        raised. Otherwise, the file will be saved and its name (including
        the folder) will be returned.

        :param storage: The uploaded file to save.
        :param folder: The subfolder within the upload set to save to.
        :param name: The name to save the file as. If it ends with a dot, the
            file's extension will be appended to the end. (If you
            are using `name`, you can include the folder in the
            `name` instead of explicitly using `folder`, i.e.
            ``uset.save(file, name="someguy/photo_123.")``
        """

        if not isinstance(storage, FileStorage):
            raise TypeError("Storage must be a werkzeug.FileStorage")

        if folder is None and name is not None and "/" in name:
            folder, name = os.path.split(name)

        basename = self.get_basename(storage.filename)

        if not self.file_allowed(basename):
            raise UploadNotAllowed()

        if name:
            if name.endswith('.'):
                basename = name + extension(basename)
            else:
                basename = name

        if folder:
            target_folder = os.path.join(self.config.destination, folder)
        else:
            target_folder = self.config.destination

        if not await aiofiles.os.path.exists(target_folder):
            await aiofiles.os.makedirs(target_folder)

        if await aiofiles.os.path.exists(
            os.path.join(target_folder, basename)
        ):
            basename = await self.resolve_conflict(target_folder, basename)

        target = os.path.join(target_folder, basename)
        target = pathlib.Path(target)

        await storage.save(target)

        if folder:
            return posixpath.join(folder, basename)
        else:
            return basename

    async def resolve_conflict(self, target_folder: str, basename: str) -> str:
        """
        If a file with the selected name already exists in the target folder,
        this method is called to resolve the conflict. It should return a new
        basename for the file.

        The default implementation splits the name and extension and adds a
        suffix to the name consisting of an underscore and a number, and tries
        that until it finds one that doesn't exist.

        :param target_folder: The absolute path to the target.
        :param basename: The file's original basename.
        """
        name, ext = os.path.splitext(basename)
        count = 0
        while True:
            count = count + 1
            newname = f'{name}_{count}{ext}'
            if not await aiofiles.os.path.exists(
                os.path.join(target_folder, newname)
            ):
                return newname
