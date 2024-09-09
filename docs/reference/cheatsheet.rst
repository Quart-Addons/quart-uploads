.. _cheatsheet:

==========
Cheatsheet
==========

Basic App
---------

.. code-block:: python

    from quart import Quart, render_template
    from quart_uploads import UploadSet, configure_uploads, FE

    app = Quart(__name__)

    photos = UploadSet('photos', FE.Images)
    configure_uploads(app, photos)

    @app.route("/hello")
    async def upload():
        if request.method == 'POST' and 'photo' in (await request.files):
            filename = await photos.save((await request.files)['photo'])
            # Save filename to your database of choice here.
            flash("Photo saved.")
            return redirect(url_for('show', id=rec.id))
        return await render_template('upload.html')

Large Applications
------------------

.. code-block:: python
    :caption: yourapplication/photos.py

    from quart import Blueprint 
    from quart_uploads import UploadSet, FE

    bp = Blueprint('photos', __name__, url_prefix='/photos')

    photos = UploadSet('photos', FE.Images)

    # Routes & additional code here. 

.. code-block:: python
    :caption: youapplication/audio.py

    from quart import Blueprint 
    from quart_uploads import UploadSet, FE

    bp = Blueprint('audio', __name__, url_prefix='/audio')

    audio = UploadSet('audio', FE.Audio)

    # Routes & additional code here.

.. code-block:: python
    :caption: youapplication/app.py

    from quart import Quart
    from quart_uploads import configure_uploads

    def create_app() -> Quart:
        app = Quart(__name__)

        
        from .photos import bp as photo_bp
        app.register_blueprint(photo_bp)

        from .audio import bp as audio_bp
        app.register_blueprint(audio_bp)

        from .photo import photos
        from .audio import audio
        usets = (photos, audio)
        configure_uploads(app, usets)

        # Other app registration here. 
        
        return app

Upload Set 
-----------

.. code-block:: python 
    
    from quart_uploads import UploadSet, FE

    photos = UploadSet('photos', FE.Images)photos = UploadSet('photos', FE.Images)

    @app.route('/upload', methods=['GET', 'POST'])
    async def some_route():
        photos.config # Current configuration for the upload set.
        photos.url('name.jpg') # Gets the url of file using extension route.
        photos.path('name.jpg') # Absolute path of uploaded file.
        photos.file_allowed('name.jpg') # If the file is allowed
        photos.extension_allowed('.jpg') # IF the file extension is allowed.
        photos.get_basename('name.jpg') # File basename.
        file_name = await photos.save('photo.jpg') # Save a FileStorage file. 
        await photos.resolve_conflict('/uploads', 'photo.jpg') # Resolves filename conflict.


FileStorage Testing
-------------------

.. code-block:: python

    from quart_uploads import UploadSet, TestingFileSorage
    
    uset = UploadSet('photos') # Upload Set to use for testing
    tfs = TestingFileSorage(filename='photo.jpg') # File Storage Testing Object
    file_name = await uset.save(tfs) # Mock saving the file.
