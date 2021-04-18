from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from app import app

ma = Marshmallow(app)

class UniResultSchema(ma.Schema):
    class Meta:
        fields = ('university', 'degree', 'season', 'decision', 'decision_date', 'status', 'notes', 'decision_medium')


class ProgramResultSchema(ma.Schema):
    universities = fields.List(ma.Nested(UniResultSchema))

    class Meta:
        fields = ('program','latest_commit','universities')

class ResultSchema(ma.Schema):
    results = fields.List(ma.Nested(ProgramResultSchema))

    class Meta:
        fields = ('results','dummy')