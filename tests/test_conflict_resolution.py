"""
Tests folder conflict resolution with
Quart-Uploads.
"""
import os
import pytest
from quart_uploads import UploadConfiguration, UploadSet, TestingFileStorage

def test_self(tmp_path):
    """
    Tests if path existis.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()
    file = dir / "foo.txt"
    file.write_text("Some foo text.")

    assert os.path.exists(file)

@pytest.mark.asyncio
async def test_conflict(tmp_path):
    """
    Test file conflict with Quart-Uploads.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()
    file = dir / "foo.txt"
    file.write_text("Some foo text.")

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs)
    assert res == 'foo_1.txt'

@pytest.mark.asyncio
async def test_multi_condition(tmp_path):
    """
    Test multiple file conflicts with Quart-Uploads.
    """
    data = "Some foo text."

    dir = tmp_path / "uploads"
    dir.mkdir()
    file = dir / "foo.txt"
    file.write_text(data)

    for n in range(1, 6):
        file = dir / f"foo_{n}.txt"
        file. write_text(data)

    uset = UploadSet('files')
    uset._config = UploadConfiguration(dir)
    tfs = TestingFileStorage(filename='foo.txt')
    res = await uset.save(tfs)

    assert res == 'foo_6.txt'

@pytest.mark.asyncio
async def test_conflict_without_extension(tmp_path):
    """
    Test file conflict without file extension.
    """
    dir = tmp_path / "uploads"
    dir.mkdir()
    file = dir / "foo"
    file.write_text("Some foo data.")

    uset = UploadSet('files', extensions=(''))
    uset._config = UploadConfiguration(dir)

    tfs = TestingFileStorage(filename='foo')
    res = await uset.save(tfs)

    assert res == 'foo_1'
