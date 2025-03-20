from setuptools import setup, find_packages

setup(
    name="server-report-django_2",
    version="0.1.0",
    packages=find_packages(),  # Automatically includes all subdirectories with __init__.py
    include_package_data=True,
    install_requires=[
        "django>=5.1.6",
        "djangorestframework",
    ],
    entry_points={
        "console_scripts": [
            "server-report-run=health_report.manage:main",  # Adjust if manage.py is inside a folder
        ],
    },
)
