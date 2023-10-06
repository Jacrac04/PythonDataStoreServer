from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash
from webServer.dataManagment.models import PythonDataAuthTokens, Project, PythonData  # noqa: F401


class User(db.Model):
    id = db.Field('id', data_type='int', primary_key=True)
    email = db.Field('email', data_type='varchar')
    password = db.Field('password', data_type='varchar')
    name = db.Field('name', data_type='varchar')
    admin = db.Field('admin', data_type='boolean')
    projects = db.Relationship('Project', 'owner')
    
    def __init__(self, email, password, name, admin=False):
        self.email = email
        self.password = self._generate_password_hash(password)
        self.name = name
        self.admin = admin
        self._proxy = None
    
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
    
    @property
    def has_active_proxy(self):
        return self._proxy is not None
    
    @property
    def proxy(self):
        return self._proxy
    
    @proxy.setter
    def proxy(self, proxy):
        self._proxy = proxy

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name
