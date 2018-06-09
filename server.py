import cdsapi_wrapper as cds
import datetime
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    start_date = datetime.date(2009, 3, 20)
    start_time = datetime.time(14, 0, 0)
    end_date = datetime.date(2009, 3, 20)
    end_time = datetime.time(16, 0, 0)
    interval = 1
    
    
    cds.get_grib_files("1", start_date, start_time, end_date, end_time, interval)
    return 'Hello, World!'
