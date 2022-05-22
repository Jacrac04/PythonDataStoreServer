from webServer import db
from ..pythonInterface.models import PythonData
from .models import PythonDataAuthTokens
import json 
from .errors import *

class Data():
    
    modeDict = {
        'a': 1, # Can append 
        'r': 2, # Can read
        'a+': 3, # Can append and read
        'w': 4  # Can write and read
    }
    appendPerms = [1,3,4]
    readPerms = [2,3,4]
    writePerms = [4]
    
    def __init__(self, id, token):
        self.id = id
        self.token = token
        self._getInternals()
    
    def _getInternals(self):
        data = PythonData.query.filter_by(id=self.id).first()
        if not data:
            raise DataNotFoundError('error No data found')
        authToken = PythonDataAuthTokens.query.filter_by(authToken=self.token).first()
        if not authToken in data.authTokens:
            raise AuthTokenError('error Invalid authToken')
        self.authToken = authToken
        self.data = data
        self.modeNum = Data.modeDict[authToken.tokenType] if authToken.tokenType in Data.modeDict else 0
        
    
    def getData(self):
        if not self.modeNum in Data.readPerms:
            return 'error No permission'
        return self.data.dataJson
    
    def setData(self, data):
        if not self.modeNum in Data.writePerms:
            return 'error No permission'
        self.data.dataJson = data
        db.session.commit()
        return 'success'
        
    def appendData(self, newData):
        if not self.modeNum in Data.appendPerms:
            return 'error No permission'
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
        return 'success'