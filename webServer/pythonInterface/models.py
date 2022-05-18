from .. import db

class PythonData(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    dataJson = db.Column(db.String(10000))
    authTokens = db.relationship('PythonDataAuthTokens', backref='PythonData', lazy='dynamic')
    project = db.Column(db.Integer, db.ForeignKey('project.id'))