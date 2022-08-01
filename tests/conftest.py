import pytest
from quart import Quart

@pytest.fixture
def app():
    """
    Creates a Quart app.
    """
    app = Quart(__name__)
    app.config['TESTING'] = True
    return app