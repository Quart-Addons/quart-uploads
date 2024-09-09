"""
test.tests_path_url
"""
import pytest
from quart import Quart, url_for
from quart_uploads import UploadConfig, UploadSet, configure_uploads


def test_path() -> None:
    """
    Tests the file path.
    """
    uset = UploadSet('files')
    uset._config = UploadConfig('/uploads')

    assert uset.path('foo.txt') == '/uploads/foo.txt'
    assert uset.path('someguy/foo.txt') == '/uploads/someguy/foo.txt'
    assert (uset.path('foo.txt', folder='someguy') ==
            '/uploads/someguy/foo.txt')
    assert (uset.path('foo/bar.txt', folder='someguy') ==
            '/uploads/someguy/foo/bar.txt')


@pytest.mark.asyncio
async def test_url_generated() -> None:
    """
    Tests the generated url.
    """
    app = Quart(__name__)
    app.config.update(
        UPLOADED_FILES_DEST='/uploads'
    )

    uset = UploadSet('files')
    configure_uploads(app, uset)

    async with app.test_request_context("/"):
        url = uset.url('foo.txt')
        gen = url_for('_uploads.uploaded_file', setname='files',
                      filename='foo.txt', _external=True)
        assert url == gen


@pytest.mark.asyncio
async def test_url_base() -> None:
    """
    Tests the url base.
    """
    app = Quart(__name__)
    app.config.update(
        UPLOADED_FILES_DEST='/uploads',
        UPLOADED_FILES_URL='http://localhost:5001/'
    )

    uset = UploadSet('files')
    configure_uploads(app, uset)

    async with app.test_request_context("/"):
        url = uset.url('foo.txt')
        assert url == 'http://localhost:5001/foo.txt'

    assert '_uploads' not in app.blueprints
