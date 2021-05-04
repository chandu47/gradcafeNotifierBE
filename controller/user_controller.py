from flask import Flask, Blueprint,  request, Response
from flask_restplus import Resource, Api
from  database.model.user import User
from utils.saveUnisAndProgramsToMongo import saveProgramsToMongo
from utils.saveUnisAndProgramsToMongo import saveUniversitiesToMongo
import uuid

user_controller = Blueprint('user_controller', __name__)

api = Api(user_controller)

@user_controller.route('/')
def rootRoute():
    return 'Welcome to Grad Cafe Notifier'


@api.route("/api/user/register")
class RegisterUser(Resource):
    def post(self):
        requestBody = request.get_json()
        try:
            user = User(**requestBody)
            user.deviceId = str(uuid.uuid4())
            user.save()
            id = user.deviceId
            return {'status': 'OK', 'id': str(id)}, 200
        except Exception as ex:
            return {'Error': ex.__str__()}, 500

    def put(self):
        requestBody = request.get_json()
        try:
            deviceId = requestBody['deviceId']
            user = User.objects(deviceId=deviceId).first()
            user.device_token = requestBody['device_token']
            user.save()
            return {'status': 'OK', 'id': str(deviceId)}, 200
        except Exception as ex:
            return {'Error': ex.__str__()}, 500