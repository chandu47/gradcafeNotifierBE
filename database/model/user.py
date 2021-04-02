from database.db import db
import mongoengine_goodjson as gj
import datetime

class University(gj.EmbeddedDocument):
    settingId = db.IntField()
    university = db.StringField()
    degree = db.StringField()
    season = db.StringField()

class Program(gj.EmbeddedDocument):
    program = db.StringField()
    selectedUniversities = db.EmbeddedDocumentListField(University)

class UserSettings(gj.EmbeddedDocument):
    selectedPrograms = db.EmbeddedDocumentListField(Program)
    enableRejectNotifs = db.BooleanField(default = False)
    enableInfoNotifs = db.BooleanField(default = False)

class User(gj.Document):
    deviceId = db.StringField(required = True, unique=True)
    created_at = db.DateTimeField(default = datetime.datetime.utcnow)
    last_notif_at = db.DateTimeField()
    last_commit = db.IntField(default = -1)
    settings = db.EmbeddedDocumentField(UserSettings)