import cdsapi
import os
import datetime
from shutil import rmtree

def get_grib_files(job_id, start_date, start_time, end_date, end_time, interval):
    current_datetime = datetime.datetime(start_date.year, start_date.month, start_date.day, hour=start_time.hour)
    end_datetime = datetime.datetime(end_date.year, end_date.month, end_date.day, hour=end_time.hour)
    interval_timedelta = datetime.timedelta(hours=interval)
    while current_datetime <= end_datetime:
        print("Looking up " + str(current_datetime))
        make_request(job_id, str(current_datetime.year), str(current_datetime.month), str(current_datetime.day), str(current_datetime.hour) + ":00")
        current_datetime += interval_timedelta

def make_request(job_id, year, month, day, time):

    filename = "%s/%s-%s-%s-%s" % (job_id, year, month, day, time.replace(":", ""))

    if not os.path.exists('downloads/%s' % job_id):
        os.makedirs('downloads/%s' % job_id)
    
    c = cdsapi.Client()

    r = c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type':'reanalysis',
            'year':year,
            'month':month,
            'day':day,
            'time':time,
            'format':'grib'
        })
    r.download('downloads/%s.grib' % filename)

def clean_up_temporary_files(job_id):
    rmtree("downloads/%s" % job_id)

if __name__ == "__main__":
    start_date = datetime.date(2009, 3, 20)
    start_time = datetime.time(14, 0, 0)
    end_date = datetime.date(2009, 3, 20)
    end_time = datetime.time(16, 0, 0)
    interval = 1
    
    get_grib_files("1", start_date, start_time, end_date, end_time, interval)

    clean_up_temporary_files("1")
