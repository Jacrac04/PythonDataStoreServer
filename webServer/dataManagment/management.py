from webServer import db
from ..pythonInterface.models import PythonData
from .models import PythonDataAuthTokens

class Data():
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