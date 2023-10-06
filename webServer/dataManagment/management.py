from webServer import db
from .models import PythonDataAuthTokens, PythonData
import json
from .errors import DataNotFoundError, AuthTokenError


class Data():

    modeDict = {
        'a': 1,  # Can append
        'r': 2,  # Can read
        'a+': 3,  # Can append and read
        'w': 4  # Can write and read
    }
    appendPerms = [1, 3, 4] # You can append if you have permission to append, read, or write
    readPerms = [2, 3, 4] # You can read if you have permission to read, or write
    writePerms = [4] # You can write if you have permission to write

    def __init__(self, id, token):
        self.id = id # The id of the data
        self.token = token # The token which will be used to access the data
        self._getInternals()

    def _getInternals(self):
        # Get the PythonData object from the database
        data = PythonData.query.filter_by(id=self.id)[0]
        # If there is no data, raise an exception
        if not data:
            raise DataNotFoundError('error No data found')
        # Get the authToken object from the database
        authToken = PythonDataAuthTokens.query.filter_by(
            authToken=self.token)[0]
        # If the authToken is not associated with the data, raise an exception
        if authToken not in data.authTokens:
            raise AuthTokenError('error Invalid authToken')
        # Set the authToken, data, and modeNum for this object
        self.authToken = authToken
        self.data = data
        self.modeNum = Data.modeDict[authToken.tokenType] if authToken.tokenType in Data.modeDict else 0

    def getData(self):
        # Check if the user has permission to read
        if self.modeNum not in Data.readPerms:
            # If not, return an error message
            return 'error No permission'
        # If they do, return the data
        return self.data.dataJson

    def setData(self, data):
        # Check if the user has permission to write
        if self.modeNum not in Data.writePerms:
            # If not, return an error message
            return 'error No permission'
        # If they do, set the data
        self.data.dataJson = data
        # db.session.connection.commit()
        return 'success'

    def appendData(self, newData):
        # Check if the user has permission to append
        if self.modeNum not in Data.appendPerms:
            # If not, return an error message
            return 'error No permission'
        
        # If they do, append the data
        # Convert the JSON data in the new data object to a Python object
        newData = json.loads(newData)
        # Convert the JSON data in the current data object to a Python object
        data = json.loads(self.data.dataJson)
        
        # If the data is a list append the new data to the end of the list
        if isinstance(data, list):
            data.append(newData)
            self.data.dataJson = json.dumps(data)
            return 'success'
        
        # Check if the new data object can be merged with the current data object
        if not isinstance(newData, type(data)):
            return 'error Data type mismatch'
        
        # Merge the new data object with the current data object
        if isinstance(newData, dict):
            data.update(newData)
        elif isinstance(newData, list) or isinstance(newData, tuple) or isinstance(newData, set) or isinstance(newData, str):
            data += newData
        else:
            return 'error Data type not appendable or updateable'
        # Convert the merged data object back to JSON and set it as the data
        self.data.dataJson = json.dumps(data)
        # db.session.connection.commit()
        return 'success'
