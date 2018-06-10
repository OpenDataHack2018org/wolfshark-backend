import peewee
import cdsapi_wrapper as cds
import datetime
import threading
from job import *
import os
from status import Status
from magics.grib import grib_to_png
from video.convert import VideoConvert

class Worker:
    def __init__(self, job):
        self.job = job
        self.complete = False

    def run(self):
        # Get GRIB files from the server
        get_grib_files(self.job)


        # Convert GRIB files into PNG's
        for f in os.listdir("downloads/%d" % self.job.job_id):
            grib_to_png(f, "test", area=job.area, width=job.width, dark=job.theme)

        # Compile PNG's into MP4
        vc = VideoConvert("downloads/%d" % self.job.job_id, self.job.speed)
        vc.run()

        # Clean up temporary files.
        clean_up_temporary_files(self.job.job_id)

        self.job.status = Status.COMPLETED.value
        self.job.save()
        self.complete = True


def workerController(max_number_of_workers):
    workers = []

    db = PostgresqlDatabase('postgres',
                            user='postgres',
                            password='pa55w0rd',
                            host='0.0.0.0')
    db.connect()

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
            queued_jobs = Job.select().where(Job.status == Status.QUEUED.value).order_by(Job.job_id)
            if queued_jobs.count() > 0:
                w = Worker(queued_jobs[0])
                workers.append(w)
                w.job.status = Status.PROCESSING.value
                w.job.save()
                thread = threading.Thread(target=w.run, daemon=True)
                thread.start()
