from flask import Blueprint, request
from webServer import db
from ..models import PythonData, PythonDataAuthTokens
from ..dataManagment.management import Data
from ..dataManagment.errors import DataError
import json

api = Blueprint('api', __name__)


@api.route('/old/get/<int:id>', methods=['POST'])
def oldGetData(id):
    authToken = json.loads(request.get_json())['authToken']
    storedData = PythonData.query.filter_by(id=id).first()
    token = PythonDataAuthTokens.query.filter_by(authToken=authToken).first()
    if token not in storedData.authTokens:
        return 'error Invalid authToken'
    if not storedData:
        return 'None'
    return storedData.dataJson


@api.route('/old/create', methods=['post'])
def createData():
    data = request.get_json()
    newData = PythonData(dataJson=data)
    db.session.add(newData)
    db.session.commit()
    return str(newData.id)

# Update data


@api.route('/old/update/<int:id>', methods=['post'])
def oldUpdateData(id):
    requestData = json.loads(request.get_json())
    data = requestData['data']
    authToken = requestData['authToken']
    storedData = PythonData.query.filter_by(id=id).first()
    storedAuthToken = PythonDataAuthTokens.query.filter_by(
        authToken=authToken).first()
    if storedAuthToken not in storedData.authTokens:
        return 'error Invalid authToken'
    if not storedData:
        return 'No Data Found'
    storedData.dataJson = data
    db.session.commit()
    return str(storedData.id)


@api.route('/get/<int:id>', methods=['post'])
def getData(id):
    data = json.loads(request.get_json())
    try:
        dataObj = Data(id, data['token'])
        return dataObj.getData()
    except DataError as e:
        return str(e)


@api.route('/append/<int:id>', methods=['post'])
def appendData(id):
    data = json.loads(request.get_json())
    dataObj = Data(id, data['token'])
    return dataObj.appendData(data['data'])  # dataObj.getData()


@api.route('/update/<int:id>', methods=['post'])
def updateData(id):
    data = json.loads(request.get_json())
    dataObj = Data(id, data['token'])
    return dataObj.setData(data['data'])  # dataObj.getData()


@api.route('/testCreateAuth/<int:id>', methods=['GET'])
def createAuthToken(id):
    newToken = PythonDataAuthTokens(tokenType='r', pythonDataId=id)
    db.session.add(newToken)
    db.session.commit()
    return str(newToken.authToken)
