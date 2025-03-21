from setuptools import setup, find_packages

setup(
    name='simon-datavalidator',
    version='0.1',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    author='Simon Dickson',
    author_email='simonoche987@gmail.com',
    description='A simple data validation package',
)
