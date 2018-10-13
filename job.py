from peewee import *

db = PostgresqlDatabase('docker',
                        user='docker',
                        password='pa55w0rd',
                        host='0.0.0.0')


class Job(Model):
    job_id = AutoField()
    user_name = CharField()
    title = CharField()
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    interval = IntegerField()
    dataset = CharField()
    area = CharField()                # TODO use blobs or JSON
    theme = BooleanField()
    speed = IntegerField()
    status = IntegerField()
    resolution = IntegerField()
    output = IntegerField()
    format = CharField()

    class Meta:
        database = db
