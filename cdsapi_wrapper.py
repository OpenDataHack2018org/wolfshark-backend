import cdsapi
import os
import datetime
from shutil import rmtree
from dataset import dataset as ds
import concurrent.futures


def get_grib_files(job, threads):
    # current_datetime = job.start_date_time
    interval_timedelta = datetime.timedelta(hours=job.interval)
    n = (job.end_date_time - job.start_date_time) / interval_timedelta

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(n):
            current_datetime = job.start_date_time + (i * interval_timedelta)
            executor.submit(make_request,
                            i,
                            job.job_id,
                            str(current_datetime.year),
                            str(current_datetime.month),
                            str(current_datetime.day),
                            "%02d:00" % current_datetime.hour,
                            job.dataset)
    # number = 1
    # while current_datetime <= job.end_date_time:
    #     print("Looking up " + str(current_datetime))
    #     make_request(number, job.job_id,
    #         str(current_datetime.year),
    #         str(current_datetime.month),
    #         str(current_datetime.day),
    #         "%02d:00" % current_datetime.hour,
    #         job.dataset)
    #     current_datetime += interval_timedelta
    #     number += 1


def make_request(number, job_id, year, month, day, time, dataset):

    print(number)
    filename = str(job_id) + "/%09d" % number
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
