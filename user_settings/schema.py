from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from database.model.user import UserSettings, Program
from main import app
from model.enums.degreeEnum import DegreeType
from exceptions.user_settings_exception import ValidationException
from model.enums.seasonEnum import AdmitSeason

ma = Marshmallow(app)

class ProgramSettingsSchema(ma.Schema):
    university = fields.Str()
    program = fields.Str()
    degree = fields.Str()
    season = fields.Str()
    class Meta:
        fields = ('program', 'university','settingId','season','degree')

    @validates('degree')
    def validate_degree( _, value):
        if not DegreeType.has_value(value):
            raise ValidationError('Invalid Degree passed in request')

    @validates('season')
    def validate_season( _ , value):
        if value not in AdmitSeason.validSeasons:
            raise ValidationError('Invalid Season passed in request')


class UserSettingsSchema(ma.Schema):
    selectedPrograms = fields.List(ma.Nested(ProgramSettingsSchema))
    enableRejectNotifs = fields.Boolean()
    enableInfoNotifs = fields.Boolean()

    class Meta:
        fields = ('enableRejectNotifs','enableInfoNotifs','selectedPrograms')