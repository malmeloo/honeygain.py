#!/usr/bin/env python

from distutils.core import setup

with open('README.md', 'r') as file:
    long_description = file.read()

try:
    with open('requirements.txt', 'r') as file:
        requirements = [f.strip() for f in file.readlines()]
except FileNotFoundError:
    print('[!] Falling back to hardcoded requirements')
    requirements = ['requests>=2.27,<2.28', 'pydantic>=1.9.0,<1.10.0']

setup(
    name='Honeygain.py',
    version='1.1',
    description='Python wrapper for the Honeygain API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DismissedGuy/honeygain.py',

    author='Mike A.',
    author_email='dismissed.is.a.guy@gmail.com',
    packages=['honeygain'],
    install_requires=requirements,

    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ]
)
