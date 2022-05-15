from webServer import db
from ..pythonInterface.models import PythonData
from .models import PythonDataAuthTokens
import json 

class Data():
    
    modeDict = {
        'a': 1, # Can append 
        'r': 2, # Can read
        'a+': 3, # Can append and read
        'w': 4,  # Can write and read
    }
    
    def __init__(self, id, token):
        self.id = id
        self.token = token
        self._getInternals()
    
    def _getInternals(self):
        data = PythonData.query.filter_by(id=self.id).first()
        if not data:
            return None
        authToken = PythonDataAuthTokens.query.filter_by(authToken=self.token).first()
        if not authToken in data.authTokens.all():
            return None
        self.authToken = authToken
        self.data = data
        self.mode = authToken.tokenType
        
    
    def getData(self):
        return self.data.dataJson
    
    def setData(self, data):
        self.data.dataJson = data
        db.session.commit()
        
    def appendData(self, newData):
        newData = json.loads(newData)
        data = json.loads(self.data.dataJson)
        if type(newData) != type(data):
            print('Data types do not match')
            return False 
        if type(newData) == dict:
            data.update(newData)
        elif type(newData) == list:
            data += newData
        self.data.dataJson = json.dumps(data)
        db.session.commit()