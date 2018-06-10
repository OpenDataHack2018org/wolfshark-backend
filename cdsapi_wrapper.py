import cdsapi
import os
import datetime
from shutil import rmtree
from dataset import dataset as ds

def get_grib_files(job):
    current_datetime = job.start_date_time
    interval_timedelta = datetime.timedelta(hours=job.interval)
    while current_datetime <= job.end_date_time:
        print("Looking up " + str(current_datetime))
        make_request(job.job_id, str(current_datetime.year), str(current_datetime.month), str(current_datetime.day), str(current_datetime.hour) + ":00", job.dataset)
        current_datetime += interval_timedelta
        number += 1

def make_request(number, job_id, year, month, day, time, dataset):

    filename = str(number) + "%d09" % i
    if not os.path.exists('downloads/%s' % job_id):
        os.makedirs('downloads/%s' % job_id)

    c = cdsapi.Client()

    request_params = {
        'year':year,
        'month':month,
        'day':day,
        'time':time,
    }

    extra_params = ds[dataset].keys()
    for k in extra_params:
        request_params[k] = ds[dataset][k]

    print(request_params)

    r = c.retrieve(
        'reanalysis-era5-single-levels', request_params)
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
