from .. import db
import uuid

def uuidGen():
    return str(uuid.uuid4())

class PythonDataAuthTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    authToken = db.Column(db.String(),default=uuidGen())
    tokenType = db.Column(db.String(10))
    pythonDataId = db.Column(db.Integer, db.ForeignKey('python_data.id'))