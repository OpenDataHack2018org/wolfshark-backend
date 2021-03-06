import os
from flask import Flask, send_from_directory, render_template
from flask_restful import reqparse, Resource, Api
from peewee import *
import threading
import workers
from job import Job
from theme import Theme
from status import Status
from output import Output

app = Flask(__name__, static_folder='dist/static', template_folder='dist')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


api = Api(app)

db = PostgresqlDatabase('docker',
                        user='docker',
                        password='pa55w0rd',
                        host='0.0.0.0')

db.connect()
db.create_tables([Job])
db.close()

if not os.path.exists('./dist/static/videos'):
    os.makedirs('./dist/static/videos')

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
        for job in Job.select().order_by(Job.job_id.desc()):
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
    # Launch worker to ansyncronously handle the video generation
    print("starting the worker thread")
    worker = threading.Thread(target=workers.workerController)
    worker.start()
    app.run(debug=True, host='0.0.0.0', port=p, use_reloader=False)
