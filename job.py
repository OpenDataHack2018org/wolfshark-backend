from peewee import *

STATUS_QUEUED = 1
STATUS_PROCESSING = 2
STATUS_COMPLETED = 3
STATUS_ERROR = 4

THEME_DARK = 5
THEME_LIGHT = 6

db = SqliteDatabase('jobs.db')


class Job(Model):
    job_id = AutoField()
    title = CharField()
    user_name = CharField()
    user_key = CharField()
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    interval = IntegerField()
    no_of_frames = IntegerField()
    area = CharField()                     # needs to be an enum
    theme = IntegerField()
    fps = IntegerField()
    status = IntegerField()

    def __init__(self, title, user_name, user_key, start_date_time, end_date_time, interval, no_of_frames, area, theme, fps):
        Model.__init__(self)
        self.title = title
        self.user_name = user_name
        self.user_key = user_key
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.interval = interval
        self.no_of_frames = no_of_frames
        self.area = area
        self.theme = theme
        self.fps = fps
        self.status = STATUS_QUEUED

    class Meta:
        database = db
