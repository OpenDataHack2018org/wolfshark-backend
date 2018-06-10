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
        make_request(job.job_id,
            str(current_datetime.year),
            str(current_datetime.month),
            str(current_datetime.day),
            "%02d:00" % current_datetime.hour,
            job.dataset)
        current_datetime += interval_timedelta

def make_request(job_id, year, month, day, time, dataset):

    filename = "%s/%s-%s-%s-%s" % (job_id, year, month, day, time.replace(":", ""))

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
