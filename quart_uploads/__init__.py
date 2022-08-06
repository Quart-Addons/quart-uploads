"""
quart_uploads
"""
from __future__ import absolute_import
from __future__ import print_function

from .config import UploadConfiguration, config_for_set, configure_uploads
from .exceptions import UploadNotAllowed, AllExcept
from .file_ext import (TEXT, DOCUMENTS, IMAGES, AUDIO, DATA, SCRIPTS,
                       ARCHIVES, SOURCE, EXECUTABLES, DEFAULTS, All, ALL)
from .set import UploadSet
from .utils import extension, lowercase_ext, addslash, TestingFileStorage

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
    'All',
    'ALL',
    'UploadSet',
    'extension',
    'lowercase_ext',
    'addslash',
    'TestingFileStorage'
    ]
"""
__version_info__ = (0, 0, 1)
__version__ = '.'.join(__version_info__)
__author__ = 'Chris Rood'
__license__ = 'MIT'
__copyright__ = '(c) 2022 by Chris Rood'
"""
