"""
quart_uploads.route

Provides the quart route for the extension. The route is used to serve files.
"""
from quart import abort, Blueprint, current_app, send_from_directory

__all__ = ['uploads_mod']

uploads_mod = Blueprint('_uploads', __name__, url_prefix='/_uploads')


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
