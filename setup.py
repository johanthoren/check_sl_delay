#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests>=2.23', 'py-dateutil>=2.2', 'Click>=7.1', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Johan Thorén",
    author_email='johan@thoren.xyz',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A simple Nagios plugin to check SL delays.",
    entry_points='''
        [console_scripts]
        check_sl_delay=check_sl_delay.check_sl_delay:cli
    ''',
    install_requires=requirements,
    license="ISC license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='check_sl_delay',
    name='check_sl_delay',
    packages=find_packages(include=['check_sl_delay.py']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.0',
    zip_safe=False,
)
