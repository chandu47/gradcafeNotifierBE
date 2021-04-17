from database.db import db
import mongoengine_goodjson as gj
import datetime

class ProgramCommitInfo(gj.EmbeddedDocument):
    program = db.StringField()
    count = db.IntField(default = 1)
    #last_fetch_commit of the programs
    last_fetch_commit = db.IntField(default = -1)
    last_notif_commit = db.IntField(default = -1)

class Program(gj.EmbeddedDocument):
    program = db.StringField()
    last_fetch_commit = db.IntField(default = -1)
    settingId = db.IntField()
    university = db.StringField()
    degree = db.StringField()
    season = db.StringField()

    def __eq__(self, other):
        if self.program==other.program and self.season==other.season and self.university==other.university and self.degree==other.degree:
            return True
        return False

class UserSettings(gj.EmbeddedDocument):
    selectedPrograms = db.EmbeddedDocumentListField(Program, default = [])
    enableRejectNotifs = db.BooleanField(default = False)
    enableInfoNotifs = db.BooleanField(default = False)

    def get_setting(self, settingId):
        for p in self.selectedPrograms:
            if p.settingId == settingId:
                return p
        return None

    def check_dup(self, data):
        for p in self.selectedPrograms:
            if p.settingId == data.settingId:
                continue
            if p == data:
                return True
        return False

class User(gj.Document):
    deviceId = db.StringField(required = True, unique=True)
    device_type = db.StringField(required = True)
    created_at = db.DateTimeField(default = datetime.datetime.utcnow)
    last_notif_at = db.DateTimeField()
    settings = db.EmbeddedDocumentField(UserSettings)
    program_commit_info = db.EmbeddedDocumentListField(ProgramCommitInfo, default = [])

    def has_program(self, program):
        for info in self.program_commit_info:
            if info.program == program:
                return info
        return None