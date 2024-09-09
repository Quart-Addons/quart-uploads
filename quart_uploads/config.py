"""
quart_uploads.config

Defines the configuration class and configuration
helper functions for the extension.

"""
from __future__ import annotations
import os
from collections import UserDict
from dataclasses import dataclass, astuple
from typing import Any, Dict, Optional, Union

from quart import Quart

from .route import uploads_mod
from .set import UploadSet
from .utils import addslash


@dataclass
class UploadConfig:
    """
    This holds the configuration for a single `UploadSet`. The constructor's
    arguments are also the attributes.

    Arguments:
        destination: The directory to save files to.
        base_url: The URL (ending with a /) that files can be downloaded from.
        If this is `None`, Quart-Uploads will serve the files itself.
        allow: A tuple of extensions to allow, even if they're not in the
        `UploadSet` extensions list.
        deny: A tuple of extensions to deny, even if they are in the
        `UploadSet` extensions list.
    """

    destination: str
    base_url: Optional[str] = None
    allow: tuple = ()
    deny: tuple = ()

    @property
    def tuple(self) -> tuple:
        """
        Returns the configuration as a tuple.
        """
        return astuple(self)

    def __eq__(self, other: Any) -> bool:
        return self.tuple == other.tuple


MUST_BE_STRING = 'The key must be a string value.'
MUST_BE_CONFIG = 'The item must be an `UploadConfig` object.'


class Uploads(UserDict):
    """
    Custom dictionary for storing `UploadConfig` objects on the
    `Quart` application.

    This will be stored at `Quart.extensions`.
    """
    def __init__(self, app: Quart) -> None:
        super().__init__()
        app.extensions['uploads'] = self

    def __getitem__(self, key: str) -> UploadConfig:
        if not isinstance(key, str):
            raise TypeError(MUST_BE_STRING)
        return super().__getitem__(key)

    def __setitem__(self, key: str, item: UploadConfig) -> None:
        if not isinstance(key, str):
            raise TypeError(MUST_BE_STRING)
        if not isinstance(item, UploadConfig):
            raise TypeError(MUST_BE_CONFIG)
        super().__setitem__(key, item)

    def __delitem__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError(MUST_BE_STRING)
        return super().__delitem__(key)

    def get(self, key: str, default: Any | None = None) -> UploadConfig | None:
        if key in self:
            return self[key]
        return default


def config_for_set(
    uset: UploadSet,
    app: Quart,
    defaults: Optional[Dict[str, str]] = None
) -> UploadConfig:
    """
    This is a helper function for `configure_uploads` that extracts the
    configuration for a single set.

    Arguments:
        uset: The upload set.
        app: The app to load the configuration from.
        defaults: A dict with keys `url` and `dest` from the
                  `UPLOADS_DEFAULT_DEST` and `DEFAULT_UPLOADS_URL`
                   settings.
    """

    config = app.config
    prefix = f'UPLOADED_{uset.name.upper()}_'
    using_defaults = False
    if defaults is None:
        defaults = dict(dest=None, url=None)

    allow_extns = tuple(config.get(prefix + 'ALLOW', ()))
    deny_extns = tuple(config.get(prefix + 'DENY', ()))
    destination = config.get(prefix + 'DEST')
    base_url = config.get(prefix + 'URL')

    if destination is None:
        # the upload set's destination wasn't given
        if uset.default_dest:
            if callable(uset.default_dest):
                # default destination is a callable.
                destination = uset.default_dest(app)
            else:
                destination = uset.default_dest
        if destination is None:  # still
            # use the default dest from the config
            if defaults['dest'] is not None:
                using_defaults = True
                destination = os.path.join(defaults['dest'], uset.name)
            else:
                raise RuntimeError(f"no destination for set {uset.name}")

    if base_url is None and using_defaults and defaults['url']:
        base_url = addslash(defaults['url']) + uset.name + '/'

    return UploadConfig(destination, base_url, allow_extns, deny_extns)


def configure_uploads(
        app: Quart, upload_sets: Union[UploadSet, tuple[UploadSet, ...]]
) -> None:
    """
    Call this after the app has been configured. It will go through all the
    upload sets, get their configuration, and store the configuration on the
    app. It will also register the uploads module if it hasn't been set. This
    can be called multiple times with different upload sets. The uploads
    module/blueprint will only be registered if it is needed to serve the
    upload sets.

    Arguments:
        app: The `~quart.Quart` instance to get the configuration from.
        upload_sets: The `UploadSet` instances to configure.
    """

    if isinstance(upload_sets, UploadSet):
        upload_sets = (upload_sets,)

    if 'uploads' not in app.extensions:
        Uploads(app)

    uploads: Uploads = app.extensions['uploads']

    defaults = {
        "dest": app.config.get('UPLOADS_DEFAULT_DEST'),
        "url": app.config.get('UPLOADS_DEFAULT_URL')
    }

    for uset in upload_sets:
        config = config_for_set(uset, app, defaults)
        uploads[uset.name] = config

    should_serve = any(s.base_url is None for s in uploads.values())
    if '_uploads' not in app.blueprints and should_serve:
        app.register_blueprint(uploads_mod)
