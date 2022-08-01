import pytest
from quart_uploads import UploadConfiguration, UploadSet, TestingFileStorage

def test_filenames():
    """
    Tests filenames with Quart-Uploads.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    name_pairs = (
        ('foo.txt', True),
        ('boat.jpg', True),
        ('warez.ext', False)
    )

    for name, result in name_pairs:
        assert uset.file_allowed(name) is result

@pytest.mark.asyncio
async def test_non_ascii_filenames():
    """
    Tests non ascii filenames.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    tfs = TestingFileStorage(filename='天安门.jpg')
    res = await uset.save(tfs, name='secret.')
    assert res == 'secret.jpg'

def test_default_extensions():
    """
    Tests default file extensions.
    """
    uset = UploadSet('files')
    uset._config = UploadConfiguration('/uploads')

    ext_pairs = (('txt', True), ('jpg', True), ('exe', False))

    for ext, result in ext_pairs:
        assert uset.extension_allowed(ext) is result
