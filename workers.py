import peewee
import cdsapi_wrapper as cds
import datetime
import threading
from job import *
import os
from status import Status
from magics.grib import grib_to_png
from magics.areas import Areas
from video.convert import VideoConvert
import time

class Worker:
    def __init__(self, job):
        self.job = job
        self.complete = False

    def do_the_work(self):
        # Get GRIB files from the server
        self.job.status = Status.PROCESSING.value
        self.job.save()
        print(self.job)
        print("Getting GRIB from CDS")
        time.sleep(2)
        cds.get_grib_files(self.job, 1)


        # Convert GRIB files into PNG's
        for f in os.listdir("downloads/%d" % self.job.job_id):
            f = ("downloads/%d/" % self.job.job_id) + f
            print("Converting to PNG file" + str(self.job.job_id))
            print(self.job)
            grib_to_png(f, self.job.dataset, area=Areas[self.job.area.upper()], width=self.job.resolution, dark=self.job.theme)

            print("finished converting PNG file")
        # Compile PNG's into MP4
        vc = VideoConvert(self.job.job_id, self.job.speed)
        vc.run()

        print("video transcoding done")
        # Clean up temporary files.
        cds.clean_up_temporary_files(self.job.job_id)

        self.job.status = Status.COMPLETED.value
        self.job.save()
        self.complete = True


def workerController():
    print("worker connecting to DB")
    db = PostgresqlDatabase('docker',
                            user='docker',
                            password='pa55w0rd',
                            host='0.0.0.0')
    db.connect()

    print("worker connected to DB")
    while True:
        queued_jobs = Job.select().where(Job.status == Status.QUEUED.value)
        if queued_jobs.count() > 0:
            job = queued_jobs[0]
            w = Worker(job)
            print(threading.current_thread())
            print(threading.active_count())
            w.do_the_work()

        # Loop through current workers and remove the ones that are finished.
        ##i = 0
        ##while i < len(workers):
        ##    if workers[i].complete:
        ##        workers.remove(workers[i])
        ##    else:
        ##        i += 1

        ##if len(workers) < max_number_of_workers:
        ##    # There are less workers running than the maximum number of workers.
        ##    # We can schedule some new workers.
        ##
        ##    # Check to see if there are any jobs that are in the queue
        ##    queued_jobs = Job.select().where(Job.status == Status.QUEUED.value).order_by(Job.job_id)
        ##    if queued_jobs.count() > 0:
        ##        w = Worker(queued_jobs[0])
        ##        workers.append(w)
        ##        w.job.status = Status.PROCESSING.value
        ##        w.job.save()
        ##        thread = threading.Thread(target=w.run, daemon=True)
        ##        thread.start()
