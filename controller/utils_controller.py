from flask import Flask, Blueprint,  request, Response
from  database.model.user import User
from utils.saveUnisAndProgramsToMongo import saveProgramsToMongo
from utils.saveUnisAndProgramsToMongo import saveUniversitiesToMongo
utils_controller = Blueprint('utils_controller', __name__)


@utils_controller.route('/api/program/save', methods=['POST'])
def savePrograms():
    saveProgramsToMongo()
    return {'status': 'OK'}, 200

@utils_controller.route('/api/university/save', methods=['POST'])
def saveUniversities():
    saveUniversitiesToMongo()
    return {'status': 'OK'}, 200