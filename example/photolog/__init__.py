"""
photolog.py
===========
This is a simple example app for Quart-Uploads. It is a
simple photolog app that lets you submit blog posts that
are photos.
"""
from quart import (Quart, request, url_for, redirect, render_template,
                  flash, session, g)

from quart_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed

# default configuration values
DEBUG = False
SECRET_KEY = ('\xa3\xb6\x15\xe3E\xc4\x8c\xbaT\x14\xd1:'
              '\xafc\x9c|.\xc0H\x8d\xf2\xe5\xbd\xd5')

UPLOADED_PHOTOS_DEST = '/tmp/photolog'

# application
app = Quart(__name__)
app.config.from_object(__name__)

# uploads
uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

# database

# utils 

def to_index():
    return redirect(url_for('index'))

# views

@app.route('/')
def index():
    posts = Post.all()
    return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
async def new():
    if request.method == 'POST':
        files = await request.files
        form = await request.form
        photo = files.get('photo')
        title = form.get('title')
        caption = form.get('caption')
        if not (photo and title and caption):
            flash("You must fill in all the fields")
        else:
            try:
                filename = await uploaded_photos.save(photo)
            except UploadNotAllowed:
                await flash("The upload was not allowed")
            else:
                post = Post(title=title, caption=caption, filename=filename)
                post.id = unique_id()
                post.store()
                await flash("Post successful")
                return to_index()
    return await render_template('new.html')


@app.route('/login', methods=['GET', 'POST'])
async def login():
    if session.get('logged_in'):
        flash("You are already logged in")
        return to_index()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == app.config['ADMIN_USERNAME'] and
            password == app.config['ADMIN_PASSWORD']):
            session['logged_in'] = True
            await flash("Successfully logged in")
            return to_index()
        else:
            await flash("Those credentials were incorrect")
    return await render_template('login.html')


@app.route('/logout')
async def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        await flash("Successfully logged out")
    else:
        await flash("You weren't logged in to begin with")
    return to_index()


def run() -> Quart:
    return app