import cdsapi_wrapper as cds
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    cds.make_request("1", "2009", "03", "21", "14:00")
    return 'Hello, World!'
