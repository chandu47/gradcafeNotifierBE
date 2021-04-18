from flask import Flask, Blueprint,  request, Response
from  database.model.user import User
from utils.saveUnisAndProgramsToMongo import saveProgramsToMongo
from utils.saveUnisAndProgramsToMongo import saveUniversitiesToMongo
user_controller = Blueprint('user_controller', __name__)
import uuid

@user_controller.route('/')
def rootRoute():
    return 'Welcome to Grad Cafe Notifier'


@user_controller.route('/api/user/register', methods=['POST'])
def registerUser():
    requestBody  = request.get_json()
    try:
        user = User(**requestBody)
        user.deviceId = uuid.uuid4()
        user.save()
        id = user.deviceId
        return {'status': 'OK', 'id': str(id)}, 200
    except Exception as ex:
        return {'Error': ex.__str__()}, 500