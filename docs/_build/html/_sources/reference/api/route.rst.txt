=================
Route for Uploads
=================

The route for the uploads provides a Quart route for serving files 
to the frontend of your Quart application. 

It provides a `Blueprint` for the route, which is then registered to
the app from `configure_uploads`.

.. code-block:: python 
    uploads_mod = Blueprint('_uploads', __name__, url_prefix='/_uploads')

The actual view is as follows:

.. code-block:: python
    @uploads_mod.route('/<setname>/<path:filename>')
    async def uploaded_file(setname, filename):
        """
        Extension route for serving files to the
        frontend.
        """
        config = current_app.upload_set_config.get(setname)
        if config is None:
            abort(404)
        return await send_from_directory(config.destination, filename)