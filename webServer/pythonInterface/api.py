from flask import Blueprint, render_template, redirect, url_for, request, flash
from webServer import db
from .models import PythonData
from ..dataManagment.management import Data
import json

api = Blueprint('api', __name__)



@api.route('/get/<int:id>', methods=['GET'])
def getData(id):
    storedData = pythonData.query.filter_by(id=id).first()
    if not storedData:
        return 'No Data Found'
    return storedData.dataJson

@api.route('/create', methods=['post'])
def createData():
    data = request.get_json()
    newData = pythonData(dataJson=data)
    db.session.add(newData)
    db.session.commit()
    return str(newData.id)

# Update data
@api.route('/update/<int:id>', methods=['post'])
def updateData(id):
    data = request.get_json()
    storedData = pythonData.query.filter_by(id=id).first()
    if not storedData:
        return 'No Data Found'
    storedData.dataJson = data
    db.session.commit()
    return str(storedData.id)

# Test New
@api.route('/test/<int:id>', methods=['post'])
def test(id):
    data = json.loads(request.get_json())
    dataObj = Data(id, data['token'])
    return dataObj.getData()
