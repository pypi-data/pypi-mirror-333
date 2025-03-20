from setuptools import setup, find_packages

setup(
    name='cronpie',
    version='0.1.0',
    packages=find_packages(include=['cronpie', 'cronpie.*']),
    install_requires=[
        'schedule==1.1.0'
    ],
    author='Marjon Godito'
)