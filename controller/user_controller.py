from flask import Flask, Blueprint,  request, Response
from  database.model.user import User
from utils.saveUnisAndProgramsToMongo import saveProgramsToMongo
from utils.saveUnisAndProgramsToMongo import saveUniversitiesToMongo
user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/')
def rootRoute():
    return 'Welcome to Grad Cafe Notifier'


@user_controller.route('/api/user/register', methods=['POST'])
def registerUser():
    requestBody  = request.get_json()
    user = User(**requestBody).save()
    id = user.id
    return {'id': str(id), 'status': 'OK'}, 200