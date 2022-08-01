"""
Tests saving files with Quart-Uploads.
"""
import pytest
from quart_uploads import UploadConfiguration, UploadSet, TestingFileStorage, ALL

@pytest.mark.asyncio
async def test_saved():
    """
    Tests save file for Quart-Uploads.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save_testing(tfs)
    assert res == 'foo.txt'
    assert tfs.saved == '/uploads/foo.txt'

@pytest.mark.asyncio
async def test_save_folders():
    """
    Tests save folders.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save_testing(tfs, folder='someguy')
    assert res == 'someguy/foo.txt'
    assert tfs.saved == '/uploads/someguy/foo.txt'

@pytest.mark.asyncio
async def test_save_named():
    """
    Tests saving a named file.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save_testing(tfs, name='file_123.txt')
    assert res == 'file_123.txt'
    assert tfs.saved == '/uploads/file_123.txt'

@pytest.mark.asyncio
async def test_save_named_ext():
    """
    Test renaming the file without the extension.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save_testing(tfs, name='photo_123.')
    assert res == 'photo_123.jpg'
    assert tfs.saved == '/uploads/photo_123.jpg'

@pytest.mark.asyncio
async def test_folder_named_ext():
    """
    Tests renameing the file without the extension
    and with a custom folder.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save_testing(tfs, folder='someguy', name='photo_123.')
    assert res == 'someguy/photo_123.jpg'
    assert tfs.saved == '/uploads/someguy/photo_123.jpg'

@pytest.mark.asyncio
async def test_implict_folder():
    """
    Tests an implict folder.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save_testing(tfs, name='someguy/photo_123.')
    assert res == 'someguy/photo_123.jpg'
    assert tfs.saved == '/uploads/someguy/photo_123.jpg'

@pytest.mark.asyncio
async def test_secured_filename():
    """
    Tests a secure filename.
    """
    uset = UploadSet('files', ALL)
    uset._config = UploadConfiguration('/uploads')

    tfs1 = TestingFileStorage(filename='/etc/passwd')
    tfs2 = TestingFileStorage(filename='../../myapp.wsgi')
    res1 = await uset.save_testing(tfs1)
    assert res1 == 'etc_passwd'
    assert tfs1.saved == '/uploads/etc_passwd'
    res2 = await uset.save_testing(tfs2)
    assert res2 == 'myapp.wsgi'
    assert tfs2.saved == '/uploads/myapp.wsgi'
