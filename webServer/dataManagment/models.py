from .. import db
import uuid

def uuidGen():
    return str(uuid.uuid4())

class PythonDataAuthTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    authToken = db.Column(db.String(),default=uuidGen())
    tokenType = db.Column(db.String(10))
    pythonDataId = db.Column(db.Integer, db.ForeignKey('python_data.id'))
    
    def __init__(self, tokenType, pythonDataId):
        self.authToken = uuidGen()
        self.tokenType = tokenType
        self.pythonDataId = pythonDataId
        
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    # pythonDataId = db.Column(db.Integer, db.ForeignKey('python_data.id'))
    pythonDataId = db.relationship('PythonData', backref='Project', lazy='dynamic')
    owner =  db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, name, pythonDataId, owner):
        self.name = name
        self.pythonDataId = pythonDataId
        self.owner = owner