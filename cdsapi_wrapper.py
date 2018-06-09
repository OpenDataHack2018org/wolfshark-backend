import cdsapi

def make_request(year, month, day, time, filename):
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
    
