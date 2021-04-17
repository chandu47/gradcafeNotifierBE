from database.db import db
import mongoengine_goodjson as gj
import datetime
from mongoengine.queryset.visitor import Q
from mongoengine import queryset_manager

class UniResult(gj.EmbeddedDocument):
    university = db.StringField()
    commit_id = db.IntField()
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


class ProgramResult(gj.Document):
    program = db.StringField()
    latest_commit = db.IntField()
    created_at = db.DateTimeField(default = datetime.datetime.utcnow)
    universities = db.EmbeddedDocumentListField(UniResult)
    meta = {'collection': 'program_result'}

    @queryset_manager
    def get_program_results_after_commit(self, queryset, program, commit):
        resultSet = queryset.filter(Q(program=program) & Q(latest_commit__gt=commit)).order_by('-latest_commit')
        return resultSet