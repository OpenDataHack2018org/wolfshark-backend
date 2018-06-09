import cdsapi_wrapper as cds
import datetime
from flask import Flask
from flask_restful import reqparse, Resource, Api
from job import Job

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument()

class AddJob(Resource):
    def post(self):


        return {'hello': 'world'}


api.add_resource(AddJob, '/api/job')

if __name__ == '__main__':
    app.run(debug=True)
