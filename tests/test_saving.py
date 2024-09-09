"""
testing.test_saving
"""
import os
from pathlib import Path
import pytest
from quart_uploads import UploadConfig, UploadSet, TestingFileStorage, ALL


@pytest.mark.asyncio
async def test_saved(tmp_path: Path) -> None:
    """
    Tests save file for Quart-Uploads.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs)
    assert res == 'foo.txt'
    assert tfs.saved == os.path.join(directory, "foo.txt")


@pytest.mark.asyncio
async def test_save_folders(tmp_path: Path) -> None:
    """
    Tests save folders.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs, folder='someguy')
    assert res == 'someguy/foo.txt'
    assert tfs.saved == os.path.join(directory, 'someguy/foo.txt')


@pytest.mark.asyncio
async def test_save_named(tmp_path: Path) -> None:
    """
    Tests saving a named file.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs, name='file_123.txt')
    assert res == 'file_123.txt'
    assert tfs.saved == os.path.join(directory, 'file_123.txt')


@pytest.mark.asyncio
async def test_save_named_ext(tmp_path: Path) -> None:
    """
    Test renaming the file without the extension.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save(tfs, name='photo_123.')
    assert res == 'photo_123.jpg'
    assert tfs.saved == os.path.join(directory, "photo_123.jpg")


@pytest.mark.asyncio
async def test_folder_named_ext(tmp_path: Path) -> None:
    """
    Tests renameing the file without the extension
    and with a custom folder.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save(tfs, folder='someguy', name='photo_123.')
    assert res == 'someguy/photo_123.jpg'
    assert tfs.saved == os.path.join(directory, 'someguy/photo_123.jpg')


@pytest.mark.asyncio
async def test_implict_folder(tmp_path: Path) -> None:
    """
    Tests an implict folder.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='boat.jpg')
    res = await uset.save(tfs, name='someguy/photo_123.')
    assert res == 'someguy/photo_123.jpg'
    assert tfs.saved == os.path.join(directory, 'someguy/photo_123.jpg')


@pytest.mark.asyncio
async def test_secured_filename(tmp_path: Path) -> None:
    """
    Tests a secure filename.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files', ALL)
    uset._config = UploadConfig(dest)

    tfs1 = TestingFileStorage(filename='/etc/passwd')
    tfs2 = TestingFileStorage(filename='../../myapp.wsgi')
    res1 = await uset.save(tfs1)
    assert res1 == 'etc_passwd'
    assert tfs1.saved == os.path.join(directory, 'etc_passwd')
    res2 = await uset.save(tfs2)
    assert res2 == 'myapp.wsgi'
    assert tfs2.saved == os.path.join(directory, 'myapp.wsgi')
