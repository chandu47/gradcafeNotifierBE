from database.db import db
import mongoengine_goodjson as gj
from mongoengine import queryset_manager
import datetime
from mongoengine.queryset.visitor import Q

class Program(gj.Document):
    program = db.StringField()
    count = db.IntField(default=0)
    last_commit = db.IntField(default=-1)
    last_commit_at = db.DateTimeField(default=datetime.datetime.utcnow)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)



    @queryset_manager
    def get_programs_for_scraping(self, queryset):
        # Query is count should be gt 0 and last_commit_at lt now - 15 mins
        resultSet = queryset.filter( Q(count__gt=0) & Q(last_commit_at__lt=datetime.datetime.utcnow()-datetime.timedelta(minutes=15))).order_by('-count')
        # By default only 50 items returned
        return resultSet[:min(len(resultSet), 50)]