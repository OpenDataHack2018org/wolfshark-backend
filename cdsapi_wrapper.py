import cdsapi
import os
import datetime

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
    
