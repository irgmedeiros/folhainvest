# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='folhainvest',
    version='0.0.1',
    description='Program for automatize trades in folhainvest simulator',
    long_description=readme,
    author='Igor Medeiros',
    author_email='irgmedeiros@gmail.com',
    url='https://github.com/irgmedeiros/folhainvest',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

