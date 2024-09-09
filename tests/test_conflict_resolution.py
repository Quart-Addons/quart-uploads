"""
tests.test_conflict_resolution
"""
import os
from pathlib import Path
import pytest
from quart_uploads import UploadConfig, UploadSet, TestingFileStorage, ALL


def test_self(tmp_path: Path) -> None:
    """
    Tests if path existis.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    file = directory / "foo.txt"
    file.write_text("Some foo text.")

    assert os.path.exists(file)


@pytest.mark.asyncio
async def test_conflict(tmp_path: Path) -> None:
    """
    Test file conflict with Quart-Uploads.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    file = directory / "foo.txt"
    file.write_text("Some foo text.")
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs)
    assert res == 'foo_1.txt'


@pytest.mark.asyncio
async def test_multi_condition(tmp_path: Path) -> None:
    """
    Test multiple file conflicts with Quart-Uploads.
    """
    data = "Some foo text."

    directory = tmp_path / "uploads"
    directory.mkdir()
    file = directory / "foo.txt"
    file.write_text(data)
    dest = directory.absolute().as_posix()

    for n in range(1, 6):
        file = directory / f"foo_{n}.txt"
        file. write_text(data)

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)
    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs)

    assert res == 'foo_6.txt'


@pytest.mark.asyncio
async def test_conflict_without_extension(tmp_path) -> None:
    """
    Test file conflict without file extension.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    file = directory / "foo"
    file.write_text("Some foo data.")

    uset = UploadSet('files', extensions=ALL)
    uset._config = UploadConfig(directory)

    tfs = TestingFileStorage(filename='foo')
    res = await uset.save(tfs)

    assert res == 'foo_1'
