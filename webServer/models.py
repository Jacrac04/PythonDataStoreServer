from flask_login import UserMixin
from . import db
from .pythonInterface.models import PythonData
from .dataManagment.models import PythonDataAuthTokens
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, email, password, name, admin=False):
        self.email = email
        self.password = self._generate_password_hash(password)
        self.name = name
        self.admin = admin
    
    @staticmethod
    def _generate_password_hash (password_plaintext: str):
        return generate_password_hash(password_plaintext, method='sha256')
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
    
# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our user table, use it in the query for the user