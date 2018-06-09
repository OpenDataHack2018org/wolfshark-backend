import cdsapi
import os

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
    
