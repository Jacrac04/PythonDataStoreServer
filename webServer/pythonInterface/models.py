from .. import db


class PythonData(db.Model):
    id = db.Field('id', data_type='int', primary_key=True)
    name = db.Field('name', data_type='varchar')
    dataJson = db.Field('dataJson', data_type='varchar')
    authTokens = db.Relationship('PythonDataAuthTokens', 'pythonData')
    projectId = db.ForeignKey('project.id')
    project = db.Relationship('Project', "pythonData")
    pass