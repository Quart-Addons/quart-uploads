"""
photolog.py
===========
This is a simple example app for Quart-Uploads. It is a
simple photolog app that lets you submit blog posts that
are photos.
"""
from quart import flask_patch
from quart import (Quart, request, url_for, redirect, render_template,
                  flash, session, g)
from flask_sqlalchemy import SQLAlchemy
from quart_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed

# default configuration values
DEBUG = False
SECRET_KEY = ('\xa3\xb6\x15\xe3E\xc4\x8c\xbaT\x14\xd1:'
              '\xafc\x9c|.\xc0H\x8d\xf2\xe5\xbd\xd5')

UPLOADED_PHOTOS_DEST = '/tmp/photolog'

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/phtolog.db'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'quartftw'

# application
app = Quart(__name__)
app.config.from_object(__name__)

# uploads
uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

# database
db = SQLAlchemy(app)

class Post(db.Model):
    """
    Post Database Model.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=False)
    published = db.Column(db.DateTime, nullable=False, server_defaults=db.func.current_timestamp())

def init_db() -> None:
    """
    Inits the database
    """
    db.drop_all()
    db.create_all()

# utils
def to_index():
    """
    Redirects to the index of the frontend.
    """
    return redirect(url_for('index'))

@app.before_first_request
def login_handle():
    """Handles user login"""
    g.logged_in = bool(session.get('logged_in'))

# views
@app.route('/')
def index():
    """Index route."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
async def new():
    """New post route."""
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
                db.session.add(Post(title=title, caption=caption, filename=filename))
                db.session.commit()
                await flash("Post successful")
                return to_index()
    return await render_template('new.html')


@app.route('/login', methods=['GET', 'POST'])
async def login():
    """User login route."""
    if session.get('logged_in'):
        await flash("You are already logged in")
        return to_index()
    if request.method == 'POST':
        form = await request.form
        username = form.get('username')
        password = form.get('password')
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
    """User logout route."""
    if session.get('logged_in'):
        session['logged_in'] = False
        await flash("Successfully logged out")
    else:
        await flash("You weren't logged in to begin with")
    return to_index()


def run() -> Quart:
    """Runs the Photolog Example"""
    return app
