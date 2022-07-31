"""
quart_uploads
"""
from .config import UploadConfiguration, config_for_set, configure_uploads
from .exceptions import UploadNotAllowed, AllExcept
from .file_ext import (TEXT, DOCUMENTS, IMAGES, AUDIO, DATA, SCRIPTS,
                       ARCHIVES, SOURCE, EXECUTABLES, DEFAULTS, ALL)
from .set import UploadSet
from .utils import (extension, lowercase_ext, addslash,
                   patch_request_class, TestingFileStorage)

__all__ = [
    'config_for_set',
    'configure_uploads',
    'TEXT',
    'DOCUMENTS',
    'IMAGES',
    'AUDIO',
    'DATA',
    'SCRIPTS',
    'ARCHIVES',
    'SOURCE',
    'EXECUTABLES',
    'DEFAULTS',
    'ALL',
    'UploadSet',
    'extension',
    'lowercase_ext',
    'addslash',
    'patch_request_class',
    'TestingFileStorage'
    ]

__version__ = '0.0.1'
