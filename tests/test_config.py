"""
Test Quart-Uploads Configuration.
"""
import os
import pytest
from quart import Quart
from quart_uploads import configure_uploads, UploadConfiguration, UploadSet

@pytest.fixture
def app() -> Quart:
    """
    Creates a Quart app to use for testing
    the configuration.
    """
    app = Quart(__name__)
    app.config['TESTING'] = True
    return app

def configure(app: Quart, *sets, **options):
    """
    Configures the sets for the tests.
    """
    app.config.update(options)
    configure_uploads(app, sets)
    return app.upload_set_config

def test_manual(app):
    """
    Tests configuration for manually serving the files.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADED_FILES_DEST = '/var/files',
        UPLOADED_FILES_URL = 'http://localhost:6001/',
        UPLOADED_PHOTOS_DEST = '/mnt/photos',
        UPLOADED_PHOTOS_URL = 'http://localhost:6002/'
    )

    file_conf = set_config['files']
    photos_conf = set_config['photos']
    assert file_conf == UploadConfiguration('/var/files', 'http://localhost:6001/')
    assert photos_conf == UploadConfiguration('/mnt/photos', 'http://localhost:6002/')

def test_self_serve(app):
    """
    Tests configuration for self serving the files.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADED_FILES_DEST = '/var/files',
        UPLOADED_PHOTOS_DEST = '/mnt/photos',
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == UploadConfiguration('/var/files', None)
    assert photos_conf == UploadConfiguration('/mnt/photos', None)

def test_defaults(app):
    """
    Tests default configuration.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADS_DEFAULT_DEST = '/var/uploads',
        UPLOADS_DEFAULT_URL = 'http://localhost:6000/',
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == UploadConfiguration('/var/uploads/files',
                                            'http://localhost:6000/files/')
    assert photos_conf == UploadConfiguration('/var/uploads/photos',
                                              'http://localhost:6000/photos/')

def test_default_self_serve(app):
    """
    Tests default configuration for self serving the files.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADS_DEFAULT_DEST = '/var/uploads'
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == UploadConfiguration('/var/uploads/files', None)
    assert photos_conf == UploadConfiguration('/var/uploads/photos', None)

def test_mixed_defaults(app):
    """
    Tests configuration default and set specific configuration.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADS_DEFAULT_DEST = '/var/uploads',
        UPLOADS_DEFAULT_URL = 'http://localhost:6001/',
        UPLOADED_PHOTOS_DEST = '/mnt/photos/',
        UPLOADED_PHOTOS_URL = 'http://localhost:6002/'
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == UploadConfiguration('/var/uploads/files','http://localhost:6001/files/')
    assert photos_conf == UploadConfiguration('/mnt/photos/', 'http://localhost:6002/')

def test_default_dest_callables(app):
    """
    Tests default destination as a callable.
    """
    files = UploadSet('files', default_dest=lambda app: os.path.join(
                      app.config['INSTANCE'], 'files'))
    photos = UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        INSTANCE = '/home/me/webapps/thisapp',
        UPLOADED_PHOTOS_DEST = '/mnt/photos/',
        UPLOADED_PHOTOS_URL = 'http://localhost:6002/'
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == UploadConfiguration('/home/me/webapps/thisapp/files', None)
    assert photos_conf == UploadConfiguration('/mnt/photos/', 'http://localhost:6002/')
