#!/usr/bin/env python

from distutils.core import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='Honeygain.py',
    version='1.0',
    description='Python wrapper for the Honeygain API.',
    long_description=long_description,
    url='https://github.com/DismissedGuy/honeygain.py',

    author='Mike A.',
    author_email='dismissed.is.a.guy@gmail.com',
    packages=['honeygain'],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ]
)
