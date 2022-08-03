=============
Upload Sets
=============

An "upload set" is a single collection of files. You just declare them in the
code::

    photos = UploadSet('photos', IMAGES)

And then you can use the `~UploadSet.save` method to save uploaded files and
`~UploadSet.path` and `~UploadSet.url` to access them. For example::

.. code-block:: python 

    @app.route('/upload', methods=['GET', 'POST'])
    async def upload():
        if request.method == 'POST' and 'photo' in (await request.files):
            filename = await photos.save((await request.files)['photo'])
            rec = Photo(filename=filename, user=g.user.id)
            rec.store()
            flash("Photo saved.")
            return redirect(url_for('show', id=rec.id))
        return await render_template('upload.html')
    
    @app.route('/photo/<id>')
    async def show(id):
        photo = Photo.load(id)
        if photo is None:
            abort(404)
        url = photos.url(photo.filename)
        return await render_template('show.html', url=url, photo=photo)

If you have a "default location" for storing uploads - for example, if your
app has an "instance" directory like `Zine`_ and uploads should be saved to
the instance directory's ``uploads`` folder - you can pass a ``default_dest``
callable to the set constructor. It takes the application as its argument.
For example::

    media = UploadSet('media', default_dest=lambda app: app.instance_path)

This won't prevent a different destination from being set in the config,
though. It's just to save your users a little configuration time.

.. _Zine: http://zine.pocoo.org/