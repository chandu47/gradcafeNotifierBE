from database.db import db
import mongoengine_goodjson as gj
import datetime

class Program(gj.Document):
    program = db.StringField()
    count = db.IntField(default=0)
    last_commit = db.IntField(default=-1)
    last_commit_at = db.DateTimeField(default=datetime.datetime.utcnow)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)