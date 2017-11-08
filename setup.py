#!/usr/bin/env python

from setuptools import setup, find_packages
from stringify import stringify_py
import os

# provide correct path for version
__version__ = None
here = os.path.dirname(os.path.dirname(__file__))
exec(open(os.path.join(here, 'jockey/version.py')).read())

requirements = [
    "subdue >= 0.1.6",
    "tk_tools"
]

setup_requires = [
    'stringify'
]

with open('readme.md', 'r') as f:
    long_description = f.read()

stringify_py(source_path='images/app', destination_file='jockey/images.py')

setup(
    name='jockey',
    version=__version__,
    description='Easy creation of hardware-oriented tests',
    long_description=long_description,
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/subdue',
    license='MIT',
    keywords='test labview visa instrument hardware',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    setup_requires=setup_requires,
    zip_safe=False
)
