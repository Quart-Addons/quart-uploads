.. _photolog:

==================
Tutorial: Photolog
==================

In this tutorial will build a simple application that will act as a photolog.
We'll then render the posts on the server and serve the HTML in the browser.

This tutorial is meant to serve as an introduction to using Quart Uploads with
your Quart application. If you want to skip to the end the code is on Github.

1: Creating the project
-----------------------

We need to create a project for our photolog server. We will use 
`Poetry`_ to do this. Poetry can be installed via pip.

.. _Poetry: https://python-poetry.org

.. code-block:: console
    
    pip3 install poetry 

We then use Poetry to create a new photolog project:

.. code-block:: console

    poetry new --examples photolog

Our project can now be be developed in the photolog log directory, and all
subsequent commands should be in run the *photolog* directory.

2: Adding the Dependencies
--------------------------

The photolog requires the following dependencies:

- Quart
- Flask SQLAlchemy 
- Quart Uploads

.. code-block:: console

    poetry add quart

    poetry add Flask_SQLAlchemy

    poetry add quart_uploads

Poetry will ensure that the dependencies are present and the paths are
correct by running:

.. code-block:: console

    poetry install

3: Creating the application
---------------------------

We need a Quart app to be our web server, which is created by the 
following addition to *photolog/__init__.py*:

.. code-block:: python
    :caption: photolog/__init__.py

    from quart import Quart

    DEBUG = True 
    SECRET_KEY = ('\xa3\xb6\x15\xe3E\xc4\x8c\xbaT\x14\xd1:'
              '\xafc\x9c|.\xc0H\x8d\xf2\xe5\xbd\xd5')
    
    app = Quart(__name__)
    app.configuration.form_object(__name__)

    def run() -> None:
        app.run()
    
As you can see we set the *DEBUG* and *SECRET_KEY* configuration variables
here as well, which we will need. 

To make the app easy to run we can all the run method from a poetry 
script, by adding the following to *pyproject.toml*:

.. code-block:: toml
    :caption: pyproject.toml

    [tool.poetry.scripts]
    start = "photolog:run"

Which allows the following command to start the app:

.. code-block:: console

    poetry run start

4: Setup user login information 
-------------------------------

We will set values for a username and password in the Quart
configuration to allow a user to login into the photolog.

.. code-block:: python
    :caption: photolog/__init__.py

    from quart import Quart

    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'quartftw'

We also need to setup a function to handle the login and logout.

.. code-block:: python
    :caption: photolog/__init__.py

    from quart import g, session

    @app.before_first_request
    def login_handle():
        """Handles user login"""
        g.logged_in = bool(session.get('logged_in'))

Prior to creating routes for logging in and out. We will add
a quick utility to redirect the user to the index or main page
of the photolog. Note this actual route will be created in later
in this tutorial. 

.. code-block:: python
    :caption: photolog/__init__.py

    from quart import redirect, url_for

    def to_index():
        """
        Redirects to the index of the frontend.
        """
        return redirect(url_for('index'))

Next we need to create the routes that will allow the user to 
login and logout. 

.. code-block:: python
    :caption: photolog/__init__.py

    from quart import flash, render_template, request

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


5: Setup Quart Uploads
----------------------

Next we need to create an upload set from Quart Uploads and configure it 
with the application. As the name suggests we are going to upload images,
so we will pass the *IMAGES* allowed file types to the upload set. 

.. code-block:: python
    :caption: photolog/__init__.py

    from quart_uploads import UploadSet, configure_uploads, IMAGES

    UPLOADED_PHOTOS_DEST = '/tmp/photolog'

    uploaded_photos = UploadSet('photos', IMAGES)

    configure_uploads(app, uploaded_photos)

We also add a function to delete all the photos that were added if need.

.. code-block:: python
    :caption: photolog/__init__.py

    import shutil

    def remove_photo_dir() -> None:
        """Remove photo dir"""
        shutil.rmtree(UPLOADED_PHOTOS_DEST)  

The final step to setting up the database is to update the poetry scripts 
in *pyproject.toml* to be:

.. code-block:: toml
    :caption: pyproject.toml

    [tool.poetry.scripts]
    photo_rm = "photolog:remove_photo_dir"
    start = "photolog.run"

Now we can run the following to create and update the database:

.. code-block:: console

    poetry run photo_rm

.. warning::

    Running this command will wipe any existing photo files.

6: Creating the database
------------------------

There are many datbase management systems to choose from depending
upon the needs and requirements. In this case we are going to use
SQL Alchemy and do so by *Flask_SQLAlchemy*. 

First we need to import the dependencies and setup the configuration 
values for the database.

.. note::

    Since we are using a *Flask* extension and not a *Quart* extension 
    for the database. We need to make use of flask_patch module provided
    with *Quart*. This must be at the top of your python file. More 
    information on this can be found in the Quart `documentation`_.
    
.. _documentation: https://quart.palletsprojects.com/en/latest/how_to_guides/flask_extensions.html

.. code-block:: python
    :caption: photolog/__init__.py

    import quart.flask_patch

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/phtolog.db'

    db = SQLAlchemy(app)

Next we will create our database model, which will be used to store our
data to the database. 

.. code-block:: python
    :caption: photolog/__init__.py

    class Post(db.Model):
        """
        Post Database Model.
        """
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String, nullable=False)
        filename = db.Column(db.String, nullable=False)
        caption = db.Column(db.String, nullable=False)
        published = db.Column(db.DateTime, nullable=False, server_defaults=db.func.current_timestamp())

Now we need to create a function that will create the database. 

.. warning::

    Dropping and clearing the database is only for example purposes and 
    you shouldn't do this for a real life application. 

.. code-block:: python
    :caption: photolog/__init__.py

    def init_db() -> None:
        """
        Inits the database.
        """
        db.drop_all()
        db.create_all()

The final step to setting up the database is to update the poetry scripts 
in *pyproject.toml* to be:

.. code-block:: toml
    :caption: pyproject.toml

    [tool.poetry.scripts]
    photo_rm = "photolog:remove_photo_dir"
    init_db = "photolog:init_db"
    start = "photolog.run"

Now we can run the following to create and update the database:

.. code-block:: console

    poetry run init_db

.. warning::

    Running this command will wipe any existing data.

7: Displaying posts in the database
-----------------------------------

With can now display the posts present in the database. To do so we
first need a template to render the posts as HTML. This is as follows
and should be added to *src/blog/templates/posts.html*:

.. code-block:: html
    :caption: photolog/templates/index.html

    {% extends "layout.html" %}

    {% block title %}Index{% endblock title %}

    {% block body %}

    {% for post in posts %}
    <div class ="col-sm-6">
        <div class="card">
            <img src="{{ post.imgsrc }}">
            <div class="card-body">
                <h5 class="card-title">{{ post.title }}</h5>
                {% if post.caption %}
                <p class="card-text">{{ post.caption }}</p>
                {% else %}
                <p class="card-text">No posts yet.</p>
                {% endif %}
                <p class="card-text">
                    Published: {{ post.published.strftime("%A, %B %d %Y at %I:%M:%S %p") }}
                </p>
                <a href="{{ post.imgsrc }}" class="btn btn-primary"></a>
            </div>
        </div>
    </div>
    {% endfor %}    

    {% endblock body %}

Now we need to create a route to query the database, retrieve the posts, 
and render the template. This will be done using the following code which 
should be added to *photolog/__init__.py*.

.. code-block:: python
    :caption: photolog/__init__.py

    @app.route('/')
    async def index():
        """Index route."""
        posts = Post.query.order_by(Post.created.desc()).all()
        return render_template('index.html', posts=posts)

8: Creating a new post
----------------------

To create blog posts we first need a form into which a user can enter
the post details. This is done via the following template code that should
be added to *photolog/templates/new.html*:

.. code-block:: html
    :caption: photolog/templates/new.html

    {% extends "layout.html" %}

    {% block title %}Add a new post{% endblock title %}

    {% block body %}

    <div class="col-md-12">
        <h2>New Post</h2>

        <form action="{{ url_for('new') }}" method=POST enctype=multipart/form-data>
            <div class="row">
                <div class="col-sm-12">
                    <input type="text" name="title" class="form-control" placeholder="title">
                </div>
                <div class="col-sm-12">
                    <input type="file" name="file" class="form-control" placeholder="file">
                </div>
                <div class="col-sm-12">
                    <textarea name="caption" class="form-control" rows="5" placeholder="Enter a caption."></textarea>
                </div>
                <div class="col-sm-12">
                    <input type="submit" value="Post">
                </div>
            </div>
        </form>
    </div>

    {% endblock body %}

To allow a visitor to create a blog post we need to accept the POST
request generated by this form in the browser. To do so the following
should be added to *photolog/__init__.py*:

.. code-block:: python
    :caption: photolog/__init__.py

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
                    await flash("The upload was not allowed", "danger")
                else:
                    db.session.add(Post(title=title, caption=caption, filename=filename))
                    db.session.commit()
                    await flash("Post successful", "success")
                    return to_index()
        return await render_template('new.html')

This route handler will render the creation form in response to a GET
request e.g. via navigation in the browser. However, for a POST
request it will extract the form data to create a post before
redirecting the user to the page with the posts.

9: Conclusion
-------------

We have built a simple database backed photlog server. This should be a 
good starting point for using *quart_uploads*. 
