from database import db
import mongoengine_goodjson as gj
import datetime



class UniResult(gj.EmbeddedDocument):
    university = db.StringField()
    degree = db.StringField()
    season = db.StringField()
    decision = db.StringField()
    decision_date = db.StringField()
    decision_medium = db.StringField()
    """
    Status Key: A: American; U: International, with US degree; I: International, without US degree; O: Other; ?: Unknown
    """
    status = db.StringField()
    date_added = db.StringField()
    notes = db.StringField()


class ProgramResult(gj.document):
    program = db.StringField()
    latest_commit = db.IntField()
    created_at = db.DateTimeField(default = datetime.datetime.utcnow)
    universities = db.EmbeddedDocumentListField(UniResult)
    meta = {'collection': 'program_result'}
