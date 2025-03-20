from setuptools import setup, find_packages

setup(
    name='cronpie',
    version='0.2.0',
    packages=find_packages(include=['cronpie', 'cronpie.*']),
    install_requires=[
        'schedule==1.2.2',
        'APScheduler==3.11.0'
    ],
    author='Marjon Godito',
    description='A simple cron job scheduler with less boilerplate code',
)