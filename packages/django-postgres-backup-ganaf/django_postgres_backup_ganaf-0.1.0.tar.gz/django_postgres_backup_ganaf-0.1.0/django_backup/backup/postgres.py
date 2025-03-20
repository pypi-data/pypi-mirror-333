import os
import re
import subprocess
import shutil
import logging
from datetime import datetime
from django.conf import settings
from .utils import ensure_backup_dir

logger = logging.getLogger('django_backup')

def get_db_settings():
    """Get database settings from Django settings."""
    return {
        'DB_HOST': getattr(settings, 'DB_HOST', 'localhost'),
        'DB_PORT': getattr(settings, 'DB_PORT', '5432'),
        'DB_NAME': getattr(settings, 'DB_NAME', ''),
        'DB_USER': getattr(settings, 'DB_USER', ''),
        'DB_PASSWORD': getattr(settings, 'DB_PASSWORD', ''),
    }

def get_server_version():
    """Get PostgreSQL server version."""
    db_settings = get_db_settings()
    
    try:
        # Use psql to get server version
        cmd = [
            'psql',
            '-h', db_settings['DB_HOST'],
            '-p', db_settings['DB_PORT'],
            '-U', db_settings['DB_USER'],
            '-d', db_settings['DB_NAME'],
            '-c', 'SELECT version();'
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = db_settings['DB_PASSWORD']

        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            match = re.search(r'PostgreSQL (\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        error_msg = f"Failed to get server version: {e}"
        logger.warning(error_msg)

    return "17.2"  # Default version if can't determine

def find_pg_dump():
    """Find the pg_dump executable."""
    pg_dump_path = shutil.which("pg_dump")
    if pg_dump_path:
        logger.info(f"Found pg_dump at: {pg_dump_path}")
        return pg_dump_path
    else:
        logger.error("pg_dump not found in the system PATH. Falling back to Docker.")
        return "docker"

def create_postgres_backup():
    """Create a PostgreSQL backup."""
    backup_dir = ensure_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{backup_dir}/postgres_backup_{timestamp}.sql"
    pg_dump_path = find_pg_dump()
    db_settings = get_db_settings()

    try:
        if pg_dump_path == "docker":
            cmd = [
                'docker', 'run', '--rm',
                '--network=host',
                'postgres:17',
                'pg_dump',
                '-h', db_settings['DB_HOST'],
                '-p', db_settings['DB_PORT'],
                '-U', db_settings['DB_USER'],
                '-d', db_settings['DB_NAME'],
                '-f', f"/backup/{os.path.basename(backup_file)}",
                '-F', 'p',
                '--no-owner',
                '--no-acl'
            ]
            env = os.environ.copy()
        else:
            # Note: Removed --no-owner and --no-acl flags as in the updated version
            cmd = [
                pg_dump_path,
                '-h', db_settings['DB_HOST'],
                '-p', db_settings['DB_PORT'],
                '-U', db_settings['DB_USER'],
                '-d', db_settings['DB_NAME'],
                '-f', backup_file,
                '-F', 'p',
            ]
            env = os.environ.copy()
            env['PGPASSWORD'] = db_settings['DB_PASSWORD']

        logger.info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)

        if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
            file_size = os.path.getsize(backup_file)
            logger.info(f"PostgreSQL backup created: {backup_file} (Size: {file_size} bytes)")
            return backup_file
        else:
            error_msg = f"Backup file is empty or not created: {backup_file}"
            logger.error(error_msg)
            raise Exception("Backup file is empty or not created")

    except subprocess.CalledProcessError as e:
        error_msg = (f"PostgreSQL backup creation failed: {e}\n"
                    f"Output: {e.stdout}\n"
                    f"Error: {e.stderr}")
        logger.error(error_msg)
        raise