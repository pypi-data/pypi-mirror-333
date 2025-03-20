# Django PostgreSQL Backup

A reusable Django app to automatically backup PostgreSQL databases to S3.

## Features

- Scheduled or manual backups of PostgreSQL databases
- S3 storage of backups
- Automatic cleanup of old backups
- Docker fallback for pg_dump
- Configurable scheduling

## Installation

```bash
pip install django-postgres-backup
```

Or add to your requirements.txt:

```
django-postgres-backup==0.1.0
```

## Configuration

Add to your `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    # other apps
    'django_backup',
]
```

Configure your settings.py with the following settings:

```python
# Database settings
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'your_database'
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'

# S3 settings
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'

# Backup settings
BACKUP_DIR = 'database_backups'
BACKUP_SCHEDULER_ENABLED = True  # Set to False to disable automatic backups
BACKUP_UPLOAD_TO_S3 = True       # Set to False to disable S3 upload
BACKUP_CLEANUP_ENABLED = True    # Set to False to disable automatic cleanup
BACKUP_KEEP_COUNT = 2            # Number of backups to keep

# Optional: Server ownership settings
IS_LOCAL = False                # Set to True for local development
SERVER_USER = 'www-data'        # User who should own backup files
SERVER_GROUP = 'www-data'       # Group who should own backup files

# Backup schedule (uses APScheduler cron syntax)
BACKUP_SCHEDULE = {
    'hour': '0',     # Run at midnight
    'minute': '0',
}
```

## Usage

### Automatic Backups

If `BACKUP_SCHEDULER_ENABLED` is set to `True`, backups will run automatically according to your schedule.

### Manual Backups

Run a backup manually:

```bash
python manage.py run_backup
```

Options:
- `--upload`: Force upload to S3 (even if disabled in settings)
- `--cleanup`: Force cleanup of old backups
- `--keep-count=N`: Specify number of backups to keep when cleaning up

## How It Works

1. The app creates backups using PostgreSQL's pg_dump tool
2. If pg_dump is not available, it falls back to using a Docker container
3. Backups are stored locally in the directory specified by `BACKUP_DIR`
4. If enabled, backups are uploaded to the S3 bucket
5. Old backups are cleaned up, keeping only the most recent ones

## License

MIT