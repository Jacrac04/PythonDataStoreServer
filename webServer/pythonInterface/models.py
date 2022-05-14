from .. import db

class pythonData(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    dataJson = db.Column(db.String(10000))