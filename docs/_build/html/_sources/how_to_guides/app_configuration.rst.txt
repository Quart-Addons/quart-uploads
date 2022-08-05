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

If you need to put limits on the file size if the uploaded data. Just use
the Quart default configuration variable `MAX_CONTENT_LENGTH` setting to
determine how large the upload can be.
