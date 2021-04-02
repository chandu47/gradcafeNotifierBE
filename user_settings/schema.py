from marshmallow import fields
from flask_marshmallow import Marshmallow
from database.model.user import UserSettings, Program, University
from app_settings import app

ma = Marshmallow(app)

"""def init_settings_marshmallow(app):
    ma.init_app(app)"""


class UniversitySettingsSchema(ma.Schema):
    class Meta:
        fields = ('university','settingId','season','degree')

class ProgramSettingsSchema(ma.Schema):
    selectedUniversities = fields.List(ma.Nested(UniversitySettingsSchema))

    class Meta:
        fields = ('program', 'selectedUniversities')

class UserSettingsSchema(ma.Schema):
    selectedPrograms = fields.List(ma.Nested(ProgramSettingsSchema))

    class Meta:
        fields = ('enableRejectNotifs','enableInfoNotifs','selectedPrograms')




"""class UserSettingsSchema(ma.Schema):
    deviceId = fields.Str(required=True)
    setting_id = fields.Int(required=True)
    enableRejectNotifs = fields.Bool()
    enableInfoNotifs = fields.Bool()
    universitySettings = fields.List(fields.Nested("UniversitySettingSchema", many=True))

    class Meta:
        fields = ("deviceId", "setting_id", "enableRejectNotifs", "enableInfoNotifs", "universitySettings")


class UniversitySettingSchema(ma.Schema):
    university = fields.Str()
    program = fields.Str()
    degree = fields.Str()
    season = fields.Str()

    class Meta:
        fields = ("university", "program", "degree", "season")"""