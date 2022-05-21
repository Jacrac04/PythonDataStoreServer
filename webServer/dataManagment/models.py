from .. import db
import uuid

def uuidGen():
    return str(uuid.uuid4())

class PythonDataAuthTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    authToken = db.Column(db.String(),default=uuidGen())
    tokenType = db.Column(db.String(10))
    pythonDataId = db.Column(db.Integer, db.ForeignKey('python_data.id'))
    pythonData = db.relationship('PythonData', back_populates='authTokens')
    
    def __init__(self, tokenType, pythonDataId):
        self.authToken = uuidGen()
        self.tokenType = tokenType
        self.pythonDataId = pythonDataId
        
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    # pythonDataId = db.Column(db.Integer, db.ForeignKey('python_data.id'))
    pythonData = db.relationship('PythonData', back_populates="project") # backref='Project', lazy='dynamic')
    ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates="projects")
    def __init__(self, name, ownerId, description):
        self.name = name
        self.ownerId = ownerId
        self.description = description