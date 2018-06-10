import os
from flask import Flask
from flask_restful import reqparse, Resource, Api
from peewee import *
from job import Job
from theme import Theme
from status import Status
from output import Output

app = Flask(__name__)
api = Api(app)

db = PostgresqlDatabase('postgres',
                        user='postgres',
                        password='pa55w0rd',
                        host='0.0.0.0')

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


class AddJob(Resource):
    def post(self):
        args = parser.parse_args()
        db.connect()
        db.create_tables([Job])
        job = Job(user_name=args["user_name"],
                  user_key=args["user_key"],
                  title=args["title"],
                  area=args["area"],
                  start_date_time=args["start_date_time"],
                  end_date_time=args["end_date_time"],
                  interval=args["interval"],
                  theme=Theme[args["theme"].upper()].value,
                  speed=args["speed"],
                  resolution=args["resolution"],
                  output=Output[args["output"].upper()].value,
                  format=args["format"],
                  status=Status.QUEUED.value
                  )
        job.save()
        db.close()
        return "success"


api.add_resource(AddJob, '/api/job')

if __name__ == '__main__':
    p = os.environ.get('PORT')
    app.run(debug=True, port=p)
