#!/usr/bin/env python

from setuptools import setup, find_packages


requirements = [
    "subdue >= 0.1.6",
    "tk_tools"
]

with open('readme.md', 'r') as f:
    long_description = f.read()

setup(
    name='jockey',
    version='v0.0.1',
    description='Easy creation of hardware-oriented tests',
    long_description=long_description,
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/subdue',
    license='MIT',
    keywords='test labview visa instrument hardware',
    packages=find_packages(),
    entry_points={'console_scripts': [
      'subdue = subdue.__main__:main']
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)
