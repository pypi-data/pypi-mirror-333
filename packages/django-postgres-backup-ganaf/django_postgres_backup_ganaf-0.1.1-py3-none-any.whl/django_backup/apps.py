from django.apps import AppConfig


class DjangoBackupConfig(AppConfig):
    name = 'django_backup'
    verbose_name = 'Django Database Backup'

    def ready(self):
        from django.conf import settings
        
        # Only start scheduler if BACKUP_SCHEDULER_ENABLED is True
        if getattr(settings, 'BACKUP_SCHEDULER_ENABLED', False):
            from .scheduler import start_scheduler
            start_scheduler()