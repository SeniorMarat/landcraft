import time
from db_manager.db_manager import DatabaseManager
from log_manager.log_manager import LogManager
from job.job import Job, JobType, JobStatus
from job_manager.job_manager import JobManager

class Controller:
  SLEEP_TIME = 5

  def __init__(self):
    self.logger: LogManager = LogManager.get_logger(name="landcraft_runtime", log_file="landcraft_runtime.log")
    self.db_manager = DatabaseManager()
    self.job_manager = JobManager(db_manager=self.db_manager)

  def main_loop(self):
    while True:
      jobs_to_create = self.db_manager.get_jobs(
        job_type=JobType.CREATE,
        statuses=[JobStatus.NEW, JobStatus.DONE]
      )

      # TODO: ignored for now
      # jobs_to_edit = db_manager.get_jobs(
      #     job_type=JobType.EDIT,
      #     statuses=[JobStatus.NEW, JobStatus.DONE]
      # )

      self.handle_jobs(jobs_to_create)
      # TODO: ignored for now
      # handle_jobs(jobs_to_edit)

      time.sleep(self.SLEEP_TIME)

  def handle_jobs(self, jobs):
    if jobs:
      for job in jobs:
        self.handle_job(job)
      self.logger.info(
        f"All jobs ({len(jobs)}) processed. Sleeping for {self.SLEEP_TIME} seconds..."
      )
    else:
      self.logger.info(
        f"No jobs to execute. Sleeping for {self.SLEEP_TIME} seconds..."
      )

  def handle_job(self, job):
    try:
      self.logger.info(
        f"Processing job '{job.id}' with status '{job.status.value}'"
      )

      # TODO: WHAT TO DO??
      if job.status == JobStatus.BEGIN:
        self.job_manager.process_job(job)
      elif job.status == JobStatus.FINISH:
        self.job_manager.stop_job(job)

    except Exception as e:
      # restart job if failed
      if job.status == JobStatus.FAILED:
        self.db_manager.update_job_status(
          job_id=job.id, new_status=JobStatus.RETRY_FAILED
        )
      else:
        self.db_manager.update_job_status(
          job_id=job.id, new_status=JobStatus.FAILED
        )
      self.logger.error(f"Error processing job '{job.id}': {e}")

if __name__ == "__main__":
  Controller().main_loop()
