#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jake Cui
# Mail: cqp@cau.edu.cn
# Created Time:  2022-06-25
#############################################

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


requirements = [
    'Bio',
    'pandas',
    'numpy',
    'cvmblaster >= 0.4.5',
    'setuptools'
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'PointBlaster', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)


# Get the long description from the relevant file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="PointBlaster",
    version=about['__version__'],
    keywords=["pip", "wgs", "blastn", "pointmutation"],
    description="find point mutation in assembled genomes",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    include_package_data=True,
    # package_data={'': ['*']},
    platforms="any",
    install_requires=requirements,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'PointBlaster=PointBlaster.PointBlaster:main',
        ],
    },
)
