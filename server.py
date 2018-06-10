import os
from flask import Flask, send_from_directory
from flask_restful import reqparse, Resource, Api
from peewee import *
from job import Job
from theme import Theme
from status import Status
from output import Output

app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)

db = PostgresqlDatabase('postgres',
                        user='postgres',
                        password='pa55w0rd',
                        host='0.0.0.0')

db.connect()
db.create_tables([Job])
db.close()

parser = reqparse.RequestParser()
parser.add_argument("user_name")
parser.add_argument("user_key")
parser.add_argument("title")
parser.add_argument("dataset")
parser.add_argument("area")
parser.add_argument("start_date_time")
parser.add_argument("end_date_time")
parser.add_argument("interval")
parser.add_argument("theme")
parser.add_argument("speed")
parser.add_argument("resolution")
parser.add_argument("output")
parser.add_argument("format")


class Jobs(Resource):
    def post(self):
        args = parser.parse_args()
        db.connect()
        try:
            job = Job(user_name=args["user_name"],
                      user_key=args["user_key"],
                      title=args["title"],
                      area=args["area"],
                      start_date_time=args["start_date_time"],
                      end_date_time=args["end_date_time"],
                      interval=args["interval"],
                      dataset=args["dataset"],
                      theme=Theme[args["theme"].upper()].value,
                      speed=args["speed"],
                      resolution=args["resolution"],
                      output=Output[args["output"].upper()].value,
                      format=args["format"],
                      status=Status.QUEUED.value
                      )
            job.save()
        except DataError:
            return "invalid data"

        db.close()
        return "success"

    def get(self):
        a = []
        db.connect()
        for job in Job.select():
            a.append({'job_id': job.job_id, 'user_name': job.user_name, 'title': job.title,
                      'start_date_time': str(job.start_date_time),
                      'end_date_time': str(job.end_date_time), 'interval': job.interval,
                      'dataset': job.dataset, 'area': job.area, 'theme': job.theme,
                      'speed': job.speed, 'status': job.status, 'resolution': job.resolution,
                      'output': job.output, 'format': job.format})
        db.close()
        return a


api.add_resource(Jobs, '/api/job')

if __name__ == '__main__':
    p = os.environ.get('PORT')
    app.run(debug=True, port=p)
