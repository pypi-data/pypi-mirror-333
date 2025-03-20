import os
import logging
import boto3
from django.conf import settings
from botocore.exceptions import ClientError

logger = logging.getLogger('django_backup')

def get_s3_settings():
    """Get S3 settings from Django settings."""
    return {
        'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', ''),
        'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
        'AWS_SECRET_ACCESS_KEY': getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
    }

def upload_to_s3(file_path):
    """Upload a file to S3 bucket with support for large files."""
    s3_settings = get_s3_settings()
    
    # Validate S3 settings
    for key, value in s3_settings.items():
        if not value:
            raise ValueError(f"Missing S3 setting: {key}")
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=s3_settings['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=s3_settings['AWS_SECRET_ACCESS_KEY']
    )

    file_name = os.path.basename(file_path)
    school_folder = f"{getattr(settings, 'BACKUP_DIR', 'database_backups').replace(' ', '_')}/"
    s3_key = f"{school_folder}{file_name}"
    file_size = os.path.getsize(file_path)

    try:
        # Check if the folder exists, create if not
        try:
            s3.head_object(Bucket=s3_settings['AWS_STORAGE_BUCKET_NAME'], Key=school_folder)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                s3.put_object(Bucket=s3_settings['AWS_STORAGE_BUCKET_NAME'], Key=school_folder, Body=b'')
                logger.info(f"Created folder: {school_folder}")

        # Use multipart upload for large files
        if file_size > 50 * 1024 * 1024:  # 50MB threshold
            config = boto3.s3.transfer.TransferConfig(
                multipart_threshold=50 * 1024 * 1024,
                max_concurrency=4,
                multipart_chunksize=10 * 1024 * 1024,
                use_threads=True
            )
            transfer = boto3.s3.transfer.S3Transfer(client=s3, config=config)
            transfer.upload_file(file_path, s3_settings['AWS_STORAGE_BUCKET_NAME'], s3_key)
        else:
            s3.upload_file(file_path, s3_settings['AWS_STORAGE_BUCKET_NAME'], s3_key)
        
        logger.info(f"Uploaded to S3: {s3_key} (Size: {file_size} bytes)")
        return True

    except Exception as e:
        error_msg = f"S3 upload failed: {e}"
        logger.error(error_msg)
        raise