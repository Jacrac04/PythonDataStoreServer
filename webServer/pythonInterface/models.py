from .. import db

class PythonData(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(20))
    dataJson = db.Column(db.String(10000))
    authTokens = db.relationship('PythonDataAuthTokens', back_populates='pythonData')
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', back_populates="pythonData")