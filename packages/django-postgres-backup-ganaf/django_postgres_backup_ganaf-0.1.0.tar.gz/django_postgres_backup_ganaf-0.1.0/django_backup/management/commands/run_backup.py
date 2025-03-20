from django.core.management.base import BaseCommand
from django_backup.backup.postgres import create_postgres_backup
from django_backup.backup.s3 import upload_to_s3
from django_backup.backup.utils import cleanup_local_backups
from django.conf import settings
import logging

logger = logging.getLogger('django_backup')

class Command(BaseCommand):
    help = 'Run database backup manually'

    def add_arguments(self, parser):
        parser.add_argument(
            '--upload',
            action='store_true',
            help='Upload backup to S3',
        )
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Clean up old backups',
        )
        parser.add_argument(
            '--keep-count',
            type=int,
            default=2,
            help='Number of backups to keep when cleaning up',
        )

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Starting backup process...'))
            
            # Create backup
            backup_file = create_postgres_backup()
            self.stdout.write(self.style.SUCCESS(f'Backup created: {backup_file}'))
            
            # Upload to S3 if requested or by default setting
            should_upload = options['upload'] or getattr(settings, 'BACKUP_UPLOAD_TO_S3', True)
            if should_upload:
                upload_to_s3(backup_file)
                self.stdout.write(self.style.SUCCESS('Backup uploaded to S3'))
            
            # Clean up old backups if requested or by default setting
            should_cleanup = options['cleanup'] or getattr(settings, 'BACKUP_CLEANUP_ENABLED', True)
            if should_cleanup:
                keep_count = options['keep_count']
                cleanup_local_backups(keep_count)
                self.stdout.write(self.style.SUCCESS(f'Cleaned up old backups, keeping {keep_count} most recent'))
                
            self.stdout.write(self.style.SUCCESS('Backup process completed successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Backup process failed: {e}'))
            logger.error(f"Backup command failed: {e}", exc_info=True)
            raise