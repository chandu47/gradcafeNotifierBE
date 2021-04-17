from flask import Flask, Blueprint,  request, Response
from flask_restplus import Resource, Api
from user_settings.schema import UserSettingsSchema, ProgramSettingsSchema
from database.model.user import User
from user_settings.dal import UserSettingsDAL

settings_controller = Blueprint('settings_controller', __name__)
api = Api(settings_controller)
user_setting_schema = UserSettingsSchema()
program_schema = ProgramSettingsSchema()

@api.route('/api/user/<string:deviceId>/settings')
class Settings(Resource):
    def get(self, deviceId): #Get all settings for a deviceId
        try:
            return (user_setting_schema.dump(UserSettingsDAL.getAllSettingsForUser(deviceId))), 200
        except Exception as ex:
            return {'Error' : ex.__str__()},500

    def post(self, deviceId): #Add a setting for a deviceId
        request_data = request.get_json()
        errors = user_setting_schema.validate(request_data)
        if errors:
            return {"message": "Double check the JSON data that it has everything needed to create a setting.", "errors": errors}, 400
        else:
            try:
                userSettings = UserSettingsDAL.addSettingsForUser(deviceId, request_data)
                return {"status": "ok", "data": user_setting_schema.dump(userSettings)}, 200
            except Exception as ex:
                return {'Error' : ex.__str__()},500

    def put(self, deviceId):
        request_data = request.get_json()
        errors = user_setting_schema.validate(request_data)
        if errors:
            return {"message": "Double check the JSON data that it has everything needed to create a setting.",
                    "errors": errors}, 400
        else:
            try:
                userSettings = UserSettingsDAL.updateSettingsForUser(deviceId, request_data)
                return {"status": "ok", "data": user_setting_schema.dump(userSettings)}, 200
            except Exception as ex:
                return {'Error': ex.__str__()}, 500

@api.route('/api/user/<string:deviceId>/settings/<int:settingId>')
class UserSetting(Resource):
    def get(self, deviceId, settingId): # Get a setting with settingId for deviceId
        try:
            data = UserSettingsDAL.getOneSettingForUser(deviceId, settingId)
            return {"status": "ok", "data": program_schema.dump(data)}, 200
        except Exception as ex:
            return {"Error" : str(ex)}, 500


    def put(self, deviceId, settingId): # Edit a given setting
        request_data = request.get_json()
        errors = program_schema.validate(request_data)
        if errors:
            return {"message": "Double check the JSON data that it has everything needed to create a setting.", "errors": errors}, 400
        try:
            updatedSetting = UserSettingsDAL.updateOneSettingForUser(deviceId, settingId, request_data)
            return {"status": "ok", "data": program_schema.dump(updatedSetting)}, 200
        except Exception as ex:
            return {"Error": str(ex)}, 500


    def delete(self, deviceId, settingId): # delete a given setting
        try:
            data = UserSettingsDAL.removeOneSettingForUser(deviceId, settingId)
            return {"status": "ok", "data": user_setting_schema.dump(data)}, 200
        except Exception as ex:
            return {"Error" : str(ex)}, 500