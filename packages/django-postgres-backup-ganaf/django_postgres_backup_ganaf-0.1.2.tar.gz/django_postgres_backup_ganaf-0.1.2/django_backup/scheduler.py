import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .backup.postgres import create_postgres_backup
from .backup.s3 import upload_to_s3
from .backup.utils import cleanup_local_backups

logger = logging.getLogger('django_backup')

# Initialize the scheduler
scheduler = BackgroundScheduler()

def run_db_backup():
    """Run the complete backup process."""
    try:
        logger.info("Starting database backup process")
        backup_file = create_postgres_backup()
        
        if getattr(settings, 'BACKUP_UPLOAD_TO_S3', False):
            upload_to_s3(backup_file)
        
        keep_count = getattr(settings, 'BACKUP_KEEP_COUNT', 2)
        cleanup_local_backups(keep_count)
        
        logger.info("Backup process completed successfully")
    except Exception as e:
        error_msg = f"Backup process failed: {e}"
        logger.error(error_msg)
        raise

def start_scheduler():
    """Start the backup scheduler with configured settings."""
    if scheduler.running:
        logger.warning("Scheduler is already running. Skipping.")
        return
    
    backup_schedule = getattr(settings, 'BACKUP_SCHEDULE', {})
    
    if not backup_schedule:
        scheduler.add_job(run_db_backup, 'cron', hour='*')
        logger.info("Scheduled backup job with default schedule (hourly)")
    else:
        scheduler.add_job(
            run_db_backup, 
            'cron', 
            **backup_schedule
        )
        logger.info(f"Scheduled backup job with custom schedule: {backup_schedule}")
    
    # Start the scheduler
    scheduler.start()
    logger.info("Backup scheduler started")

def stop_scheduler():
    """Stop the backup scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Backup scheduler stopped")