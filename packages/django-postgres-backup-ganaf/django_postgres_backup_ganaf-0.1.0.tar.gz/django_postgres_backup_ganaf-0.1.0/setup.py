from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-postgres-backup-ganaf",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Django app to backup PostgreSQL databases to S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/django-postgres-backup",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/django-postgres-backup/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "boto3>=1.26.0",
        "apscheduler>=3.9.0",
    ],
    include_package_data=True,
)