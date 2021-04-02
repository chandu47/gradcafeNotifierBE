from flask import Flask, Blueprint,  request, Response
from flask_restplus import Resource, Api
from user_settings.schema import UserSettingsSchema, UniversitySettingsSchema, ProgramSettingsSchema
from database.model.user import User
from user_settings.dal import UserSettingsDAL

settings_controller = Blueprint('settings_controller', __name__)
api = Api(settings_controller)
user_setting_schema = UserSettingsSchema()

@api.route('/api/user/<string:deviceId>/settings')
class Settings(Resource):
    def get(self, deviceId): #Get all settings for a deviceId
        try:
            return (user_setting_schema.dump(UserSettingsDAL.getAllSettingsForUser(deviceId))), 200
        except Exception as ex:
            return {'Error' : ex.__str__()},400

    def post(self, deviceId): #Add a setting for a deviceId
        pass

@api.route('/api/user/<string:deviceId>/settings/<int:settingId>')
class UserSetting(Resource):
    def get(self, deviceId, settingId): # Get a setting with settingId for deviceId
        print("Its in Settings get with deviceId - {} and settingId - {}".format(deviceId, settingId))
        return {"status": "ok"}, 200

    def put(self): # Edit a given setting
        pass

    def delete(self): # delete a given setting
        pass
