"""
quart_uploads.route

Provides the quart route for the extension. The route is used to serve files.
"""
from quart import abort, Blueprint, current_app, Response, send_from_directory

from .core import Uploads


uploads_mod = Blueprint('_uploads', __name__, url_prefix='/_uploads')


@uploads_mod.route('/<setname>/<filename>')
async def uploaded_file(setname: str, filename: str) -> Response:
    """
    Extension route for serving files to the
    frontend.
    """
    uploads: Uploads = current_app.extensions['uploads']
    config = uploads.get(setname)
    if config is None:
        abort(404)
    return await send_from_directory(config.destination, filename)
