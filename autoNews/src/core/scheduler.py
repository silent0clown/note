from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Callable
from src.utils.logger import get_logger

logger = get_logger()


class Scheduler:
    """Manages scheduled tasks using APScheduler"""

    def __init__(self, timezone: str = "UTC"):
        self.scheduler = BackgroundScheduler(timezone=timezone)
        self.jobs = {}

    def add_job(
        self,
        func: Callable,
        cron: str,
        job_id: str = "main_fetch",
        **kwargs
    ):
        """
        Add a scheduled job

        Args:
            func: Function to execute
            cron: Cron expression (e.g., "0 8 * * *" for daily at 8am)
            job_id: Unique job identifier
            **kwargs: Additional job parameters
        """
        try:
            trigger = CronTrigger.from_crontab(cron)

            job = self.scheduler.add_job(
                func,
                trigger=trigger,
                id=job_id,
                replace_existing=True,
                **kwargs
            )

            self.jobs[job_id] = job
            logger.info(f"Scheduled job '{job_id}' with cron: {cron}")

        except Exception as e:
            logger.error(f"Failed to add job '{job_id}': {e}")
            raise

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
        else:
            logger.warning("Scheduler is already running")

    def stop(self):
        """Stop the scheduler gracefully"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
            logger.info("Scheduler stopped")
        else:
            logger.warning("Scheduler is not running")

    def pause_job(self, job_id: str):
        """Pause a specific job"""
        self.scheduler.pause_job(job_id)
        logger.info(f"Job '{job_id}' paused")

    def resume_job(self, job_id: str):
        """Resume a paused job"""
        self.scheduler.resume_job(job_id)
        logger.info(f"Job '{job_id}' resumed")

    def remove_job(self, job_id: str):
        """Remove a job"""
        self.scheduler.remove_job(job_id)
        self.jobs.pop(job_id, None)
        logger.info(f"Job '{job_id}' removed")

    def get_jobs(self):
        """Get list of all jobs"""
        return self.scheduler.get_jobs()

    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self.scheduler.running
