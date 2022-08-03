=================
App Configuration
=================

An upload set's configuration is stored on an app. That way, you can have
upload sets being used by multiple apps at once. You use the
`configure_uploads` function to load the configuration for the upload sets.
You pass in the app and all of the upload sets you want configured. Calling
`configure_uploads` more than once is safe. ::

    configure_uploads(app, (photos, media))

If your app has a factory function, that is a good place to call this
function.

By default, though, Quart doesn't put any limits on the size of the uploaded
data. To protect your application, you can use `patch_request_class`. If you
call it with `None` as the second parameter, it will use the
`MAX_CONTENT_LENGTH` setting to determine how large the upload can be. ::

    patch_request_class(app, None)

You can also call it with a number to set an absolute limit, but that only
exists for backwards compatibility reasons and is not recommended for
production use. In addition, it's not necessary for Flask 0.6 or greater, so
if your application is only intended to run on Flask 0.6, you don't need it.