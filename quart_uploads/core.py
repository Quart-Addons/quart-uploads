"""
quart_uploads.core
"""
from __future__ import annotations
from collections import UserDict
from typing import Any, TYPE_CHECKING

from quart import Quart

if TYPE_CHECKING:
    from .config import UploadConfig

MUST_BE_STRING = 'The key must be a string value.'
MUST_BE_CONFIG = 'The item must be an `UploadConfig` object.'


class Uploads(UserDict):
    """
    Custom dictionary for storing `UploadConfig` objects on the
    `Quart` application.
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
