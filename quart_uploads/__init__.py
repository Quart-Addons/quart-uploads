"""
quart_uploads
"""
from __future__ import absolute_import
from __future__ import print_function


from .config import UploadConfig, configure_uploads
from .core import Uploads
from .exceptions import UploadNotAllowed, AllExcept
from .file_ext import FileExtensions, ALL
from .set import UploadSet
from .utils import TestingFileStorage

__all__ = [
    'UploadConfig',
    'configure_uploads',
    'Uploads',
    'UploadNotAllowed',
    'FileExtensions',
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
