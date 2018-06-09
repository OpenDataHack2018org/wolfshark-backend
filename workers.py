import peewee
import cdsapi_wrapper as cds
import datetime
import threading
from job import *

class Worker:
    def __init__(self, job):
        self.job = job
        self.complete = False

    def run(self):
        # Get GRIB files from the server
        get_grib_files(self.job.job_id,
                       datetime.date(self.job.start_date_time.year,
                                     self.job.start_date_time.month,
                                     self.job.start_date_time.day),
                       datetime.time(self.job.start_date_time.hour),
                       datetime.date(self.job.end_date_time.year,
                                     self.job.end_date_time.month,
                                     self.job.end_date_time.day),
                       datetime.time(self.job.end_date_time.hour),
                       self.job.interval)
    

        # Convert GRIB files into PNG's

        # Compile PNG's into MP4

        self.complete = True
        

def workerController(max_number_of_workers):
    workers = []
    
    while True:
        # Loop through current workers and remove the ones that are finished.
        i = 0
        while i < len(workers):
            if workers[i].complete:
                workers.remove(workers[i])
            else:
                i += 1
        
        if len(workers) < max_number_of_workers:
            # There are less workers running than the maximum number of workers.
            # We can schedule some new workers.

            # Check to see if there are any jobs that are in the queue
            ##queued_jobs = Job.select().order_by(Job.id)
            print("--")
            for j in Job.select().where(Job.status == STATUS_QUEUED).order_by(Job.job_id):
                print(j.job_id)
    
