from database.model.user import User
from database.model.user import UserSettings
from app_settings import app
from exceptions.user_settings_exception import UserSettingsException

class UserSettingsDAL:

    @staticmethod
    def getAllSettingsForUser(deviceId) -> UserSettings:
        try:
            target = User.objects(deviceId=deviceId)[0]
        except:
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Unable to find the user with deviceId - {}".format(deviceId))

        return target.settings