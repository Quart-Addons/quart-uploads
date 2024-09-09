"""
tests.test_preconditions
"""
from pathlib import Path
import pytest
from quart_uploads import UploadConfig, UploadSet, TestingFileStorage


def test_filenames() -> None:
    """
    Tests filenames with Quart-Uploads.
    """
    uset = UploadSet('files')
    uset._config = UploadConfig('/uploads')

    name_pairs = (
        ('foo.txt', True),
        ('boat.jpg', True),
        ('warez.ext', False)
    )

    for name, result in name_pairs:
        assert uset.file_allowed(name) is result


@pytest.mark.asyncio
async def test_non_ascii_filenames(tmp_path: Path) -> None:
    """
    Tests non ascii filenames.
    """
    directory = tmp_path / "uploads"
    directory.mkdir()
    dest = directory.absolute().as_posix()

    uset = UploadSet('files')
    uset._config = UploadConfig(dest)

    tfs = TestingFileStorage(filename='天安门.jpg')
    res = await uset.save(tfs)
    assert res == 'jpg'
    res = await uset.save(tfs, name='secret.')
    assert res == 'secret.jpg'


def test_default_extensions() -> None:
    """
    Tests default file extensions.
    """
    uset = UploadSet('files')
    uset._config = UploadConfig('/uploads')

    ext_pairs = (('txt', True), ('jpg', True), ('exe', False))

    for ext, result in ext_pairs:
        assert uset.extension_allowed(ext) is result
