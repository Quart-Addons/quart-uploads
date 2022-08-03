"""
Tests saving files with Quart-Uploads.
"""
import os
import pytest
from quart_uploads import UploadConfiguration, UploadSet, TestingFileStorage, ALL

@pytest.mark.asyncio
async def test_saved(tmp_path):
    """
    Tests save file for Quart-Uploads.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs)
    assert res == 'foo.txt'
    assert tfs.saved == os.path.join(dir, "foo.txt")

@pytest.mark.asyncio
async def test_save_folders(tmp_path):
    """
    Tests save folders.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs, folder='someguy')
    assert res == 'someguy/foo.txt'
    assert tfs.saved == os.path.join(dir, 'someguy/foo.txt')

@pytest.mark.asyncio
async def test_save_named(tmp_path):
    """
    Tests saving a named file.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs, name='file_123.txt')
    assert res == 'file_123.txt'
    assert tfs.saved == os.path.join(dir, 'file_123.txt')

@pytest.mark.asyncio
async def test_save_named_ext(tmp_path):
    """
    Test renaming the file without the extension.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save(tfs, name='photo_123.')
    assert res == 'photo_123.jpg'
    assert tfs.saved == os.path.join(dir, "photo_123.jpg")

@pytest.mark.asyncio
async def test_folder_named_ext(tmp_path):
    """
    Tests renameing the file without the extension
    and with a custom folder.
    """
    dir = tmp_path / "uploads"
    dir.mkdir() 

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save(tfs, folder='someguy', name='photo_123.')
    assert res == 'someguy/photo_123.jpg'
    assert tfs.saved == os.path.join(dir, 'someguy/photo_123.jpg')

@pytest.mark.asyncio
async def test_implict_folder(tmp_path):
    """
    Tests an implict folder.
    """
    dir = tmp_path / "uploads"
    dir.mkdir() 

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save(tfs, name='someguy/photo_123.')
    assert res == 'someguy/photo_123.jpg'
    assert tfs.saved == os.path.join(dir, 'someguy/photo_123.jpg')

@pytest.mark.asyncio
async def test_secured_filename(tmp_path):
    """
    Tests a secure filename.
    """
    dir = tmp_path / "uploads"
    dir.mkdir() 

    uset = UploadSet('files', ALL)
    uset._config = UploadConfiguration(dir)

    tfs1 = TestingFileStorage(filename='/etc/passwd')
    tfs2 = TestingFileStorage(filename='../../myapp.wsgi')
    res1 = await uset.save(tfs1)
    assert res1 == 'etc_passwd'
    assert tfs1.saved == os.path.join(dir, 'etc_passwd')
    res2 = await uset.save(tfs2)
    assert res2 == 'myapp.wsgi'
    assert tfs2.saved == os.path.join(dir, 'myapp.wsgi')
