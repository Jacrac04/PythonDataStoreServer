from .. import db
import uuid


def uuidGen():
    return str(uuid.uuid4())


class PythonDataAuthTokens(db.Model):
    id = db.Field('id', data_type='int', primary_key=True)
    authToken = db.Field('authToken', data_type='varchar')
    tokenType = db.Field('tokenType', data_type='varchar')
    pythonDataId = db.ForeignKey('python_data.id')
    pythonData = db.Relationship('PythonData', 'authTokens')

    def __init__(self, tokenType, pythonDataId):
        self.authToken = uuidGen()
        self.tokenType = tokenType
        self.pythonDataId = pythonDataId

class Project(db.Model):
    id = db.Field('id', data_type='int', primary_key=True)
    name = db.Field('name', data_type='varchar')
    description = db.Field('description', data_type='varchar')
    pythonData = db.Relationship('PythonData', 'project')
    ownerId = db.ForeignKey('user.id')
    owner = db.Relationship('User', 'projects')
    pass

    def __init__(self, name, ownerId, description):
        self.name = name
        self.ownerId = ownerId
        self.description = description

class PythonData(db.Model):
    id = db.Field('id', data_type='int', primary_key=True)
    name = db.Field('name', data_type='varchar')
    dataJson = db.Field('dataJson', data_type='varchar')
    authTokens = db.Relationship('PythonDataAuthTokens', 'pythonData')
    projectId = db.ForeignKey('project.id')
    project = db.Relationship('Project', "pythonData")
    pass 