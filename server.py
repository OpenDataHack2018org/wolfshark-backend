import cdsapi_wrapper as cds
import datetime
from flask import Flask
from flask_restful import reqparse, Resource, Api
import os
from job import Job
from peewee import *
import threading
import workers

app = Flask(__name__)
api = Api(app)

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
        print(args)
        return {'hello': 'world'}


api.add_resource(AddJob, '/api/job')

if __name__ == '__main__':
    p = os.environ.get('PORT')

    db = PostgresqlDatabase('postgres',
                        user='postgres',
                        password='pa55w0rd',
                        host='127.0.0.1')
    db.connect()
    db.create_tables([Job])

    # Launch worker to ansyncronously handle the video generation
    worker = threading.Thread(target=workers.workerController, args=(2,))
    worker.start()
    
    app.run(debug=True, port=p)

# , "user_key", , , , ,, , , , ,
