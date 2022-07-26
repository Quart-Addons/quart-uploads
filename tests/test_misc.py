"""
Tests Quart-Uploads Utilities.
"""
from __future__ import with_statement
import pytest
from quart_uploads import (addslash, extension, lowercase_ext,
                           TestingFileStorage, ALL, AllExcept)

@pytest.mark.asyncio
async def test_tfs():
    """
    File Storage Testing.
    """
    tfs = TestingFileStorage(filename='foo.bar')
    assert tfs.filename == 'foo.bar'
    assert tfs.name is None
    assert tfs.saved is None
    await tfs.save('foo_bar.txt')
    assert tfs.saved == 'foo_bar.txt'

def test_extension():
    """
    Test extension utility function.
    """
    assert extension('foo.txt') == 'txt'
    assert extension('foo') is not ''
    assert extension('archive.tar.gz') == 'gz'
    assert extension('audio.m4a') == 'm4a'

def test_lowercast_ext():
    """
    Test lowercase extension utility.
    """
    assert lowercase_ext('foo.txt') == 'foo.txt'
    assert lowercase_ext('FOO.TXT') == 'FOO.txt'
    assert lowercase_ext('foo') == 'foo'
    assert lowercase_ext('FOO') == 'FOO'
    assert lowercase_ext('archive.tar.gz') == 'archive.tar.gz'
    assert lowercase_ext('ARCHIVE.TAR.GZ') == 'ARCHIVE.TAR.gz'
    assert lowercase_ext('audio.m4a') == 'audio.m4a'
    assert lowercase_ext('AUDIO.M4A') == 'AUDIO.m4a'

def test_add_slash():
    """
    Test add slash utility.
    """
    assert (addslash('http://localhost:4000') ==
            'http://localhost:4000/')
    assert (addslash('http://localhost/uploads') ==
            'http://localhost/uploads/')
    assert (addslash('http://localhost:4000/') ==
            'http://localhost:4000/')
    assert (addslash('http://localhost/uploads/') ==
            'http://localhost/uploads/')

def test_custom_iterables():
    """
    Test `ALL` and `AllExcept`.
    """
    assert 'txt' in ALL
    assert 'exe' in ALL
    all_except = AllExcept(['exe'])
    assert 'txt' in all_except
    assert 'exe' not in all_except
