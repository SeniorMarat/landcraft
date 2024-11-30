from job.job import Job, JobType, JobStatus

class JobManager:
  def __init__(self, db_manager):
    self.db_manager = db_manager

  def process_job(self, job: Job) -> None:
    # TODO: process job logic
    print("process job logic")
    raise NotImplementedError

  def stop_job(self, job: Job) -> None:
    # TODO: stop job logic
    print("stop job logic")
    raise NotImplementedError
