"""
quart_uploads.config

Defines the configuration class and configuration
helper functions for the extension.

"""
import os

from dataclasses import dataclass, astuple
from typing import Optional, Union

from quart import Quart

from .utils import addslash
from .route import uploads_mod
from .set import UploadSet

__all__ = ['UploadConfiguration', 'config_for_set', 'configure_uploads']

@dataclass
class UploadConfiguration:
    """
    This holds the configuration for a single `UploadSet`. The constructor's
    arguments are also the attributes.

    :param destination: The directory to save files to.
    :param base_url: The URL (ending with a /) that files can be downloaded
        from. If this is `None`, Quart-Uploads will serve the files itself.
    :param allow: A tuple of extensions to allow, even if they're not in the
        `UploadSet` extensions list.
    :param deny: A tuple of extensions to deny, even if they are in the
        `UploadSet` extensions list.
    """

    destination: str
    base_url: Optional[str] = None
    allow: tuple = ()
    deny: tuple  = ()

    @property
    def tuple(self) -> tuple:
        """
        Returns the configuration as a tuple.
        """
        return astuple(self)

    def __eq__(self, other) -> bool:
        return self.tuple == other.tuple

def config_for_set(
    uset: UploadSet,
    app: Quart,
    defaults: Optional[dict]=None
    ) -> UploadConfiguration:
    """
    This is a helper function for `configure_uploads` that extracts the
    configuration for a single set.

    :param uset: The upload set.
    :param app: The app to load the configuration from.
    :param defaults: A dict with keys `url` and `dest` from the
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
            # use the "default_dest" callable
            destination = uset.default_dest(app)
        if destination is None: # still
            # use the default dest from the config
            if defaults['dest'] is not None:
                using_defaults = True
                destination = os.path.join(defaults['dest'], uset.name)
            else:
                raise RuntimeError(f"no destination for set {uset.name}")

    if base_url is None and using_defaults and defaults['url']:
        base_url = addslash(defaults['url']) + uset.name + '/'

    return UploadConfiguration(destination, base_url, allow_extns, deny_extns)

def configure_uploads(app: Quart, upload_sets: Union[UploadSet, tuple[UploadSet, ...]]) -> None:
    """
    Call this after the app has been configured. It will go through all the
    upload sets, get their configuration, and store the configuration on the
    app. It will also register the uploads module if it hasn't been set. This
    can be called multiple times with different upload sets. The uploads
    module/blueprint will only be registered if it is needed to serve the
    upload sets.

    :param app: The `~quart.Quart` instance to get the configuration from.
    :param upload_sets: The `UploadSet` instances to configure.
    """

    if isinstance(upload_sets, UploadSet):
        upload_sets = (upload_sets,)

    if not hasattr(app, 'upload_set_config'):
        app.upload_set_config = {}
    set_config = app.upload_set_config
    defaults = dict(dest=app.config.get('UPLOADS_DEFAULT_DEST'),
                    url=app.config.get('UPLOADS_DEFAULT_URL'))

    for uset in upload_sets:
        config = config_for_set(uset, app, defaults)
        set_config[uset.name] = config

    should_serve = any(s.base_url is None for s in set_config.values())
    if '_uploads' not in app.blueprints and should_serve:
        app.register_blueprint(uploads_mod)
