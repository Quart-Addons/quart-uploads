"""
Test Quart-Uploads Configuration.
"""
from quart import Quart
from quart_uploads import configure_uploads, UploadConfiguration, UploadSet

def configure(app: Quart, *sets, **options):
    """
    Configures the sets for the tests.
    """
    app.config.update(options)
    configure_uploads(app, sets)
    return app.upload_set_config

Config = UploadConfiguration

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
        UPLOADED_PHOTOS_DEST = '/mnt/photos/',
        UPLOADED_PHOTOS_URL = 'http://localhost:6002/'
    )

    file_conf = set_config['files']
    photos_conf = set_config['photos']
    assert file_conf == Config('/var/files', 'http://localhost:6001/', allow=(), deny=())
    assert photos_conf == Config('/mnt/photos', 'http://localhost:6002/', allow=(), deny=())

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
        UPLOADED_PHOTOS_DEST = '/mnt/photos/',
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == Config('/var/files', None)
    assert photos_conf == Config('/mnt/photos', None)

def test_defaults(app):
    """
    Tests default configuration.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADED_DEFAULT_DEST = '/var/uploads',
        UPLOADED_DEFAULT_URL = 'http://localhost:6000/',
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == Config('/var/uploads/files',
                               'http://localhost:6000/files/')
    assert photos_conf == Config('/var/uploads/photos',
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
        UPLOADED_DEFAULT_DEST = '/var/uploads'
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == Config('/var/uploads/files', None)
    assert photos_conf == Config('/var/uploads/photos', None)

def test_mixed_defaults(app):
    """
    Tests configuration default and set specific configuration.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        UPLOADED_DEFAULTS_DEST = '/var/uploads',
        UPLOADED_DEFAULTS_URL = 'http://localhost:6001/',
        UPLOADED_PHOTOS_DEST = '/mnt/photos/',
        UPLOADED_PHOTOS_URL = 'http://localhost:6002/'
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == Config('/var/uploads/files',
                               'http://localhost:6001/files/')
    assert photos_conf == Config('/mnt/photos', 'http://localhost:6002/')

def test_default_dest_callables(app):
    """
    Tests default destination as a callable.
    """
    files, photos = UploadSet('files'), UploadSet('photos')

    set_config = configure(
        app,
        files,
        photos,
        INSTANCE = '/home/me/webapps/thisapp',
        UPLOADED_PHOTOS_DEST = '/mnt/photos/',
        UPLOADED_PHOTOS_URL = 'http://localhost:6002/'
    )

    file_conf, photos_conf = set_config['files'], set_config['photos']

    assert file_conf == Config('/home/me/webapps/thisapp/files', None)
    assert photos_conf == Config('/mnt/photos', 'http://localhost:6002/')
