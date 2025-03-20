import os
import logging
import shutil
from pathlib import Path
from django.conf import settings

logger = logging.getLogger('django_backup')

def get_backup_dir():
    """Get the backup directory from settings or use default."""
    backup_dir_name = getattr(settings, 'BACKUP_DIR', 'database_backups').replace(" ", "_")
    backup_dir = os.path.join(os.getcwd(), backup_dir_name)
    return backup_dir

def ensure_backup_dir():
    """Create backup directory if it doesn't exist."""
    backup_dir = get_backup_dir()
    os.makedirs(backup_dir, exist_ok=True)
    logger.info(f"Created backup directory: {backup_dir}")
    
    # Change ownership if not in local mode and settings provided
    if not getattr(settings, 'IS_LOCAL', True):
        server_user = getattr(settings, 'SERVER_USER', None)
        server_group = getattr(settings, 'SERVER_GROUP', None)
        
        if server_user and server_group:
            try:
                shutil.chown(backup_dir, user=server_user, group=server_group)
                logger.info(f"Changed ownership of {backup_dir} to {server_user}:{server_group}")
            except PermissionError:
                logger.warning(f"Permission denied: Could not change ownership of {backup_dir}. Try running as root.")
    
    return backup_dir

def cleanup_local_backups(keep_count=2):
    """Delete old backups, keeping only the most recent ones."""
    backup_dir = get_backup_dir()
    backup_files = sorted(
        Path(backup_dir).glob('postgres_backup_*.sql'),
        key=os.path.getctime
    )

    if len(backup_files) > keep_count:
        logger.info(f"Found {len(backup_files)} backups, keeping the {keep_count} most recent")
        for backup_file in backup_files[:-keep_count]:
            try:
                os.remove(backup_file)
                logger.info(f"Deleted old backup: {backup_file}")
            except Exception as e:
                logger.error(f"Failed to delete backup {backup_file}: {e}")
    else:
        logger.info(f"Found only {len(backup_files)} backups, no cleanup needed")