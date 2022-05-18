import pytest
from webServer import models
from webServer import create_app, db


@pytest.fixture(scope='module')
def newUser():
    user = models.User('test@test.com', 'test', 'test')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.TestingConfig')
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            
            yield test_client
            db.session.remove()
            user = models.User.query.filter_by(email='register@test.com').first()
            if user:
                db.session.delete(user)
                db.session.commit()
            
    