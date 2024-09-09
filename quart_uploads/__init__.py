"""
quart_uploads
"""
from __future__ import absolute_import
from __future__ import print_function

from .config import UploadConfig, Uploads, configure_uploads
from .exceptions import UploadNotAllowed, AllExcept
from .file_ext import FILE_EXTENSIONS as FE, ALL
from .set import UploadSet
from .utils import TestingFileStorage

__all__ = [
    'UploadConfig',
    'configure_uploads',
    'Uploads',
    'UploadNotAllowed',
    'FE',
    'ALL',
    'AllExcept',
    'UploadSet',
    'TestingFileStorage'
    ]

"""
__version_info__ = (0, 0, 1)
__version__ = '.'.join(__version_info__)
__author__ = 'Chris Rood'
__license__ = 'MIT'
__copyright__ = '(c) 2022 by Chris Rood'
"""
