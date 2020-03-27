#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = [
    'requests>=2.23',
    'Click>=7.1',
    'func-timeout>=4.3',
]

SETUP_REQUIREMENTS = [
    'pytest-runner',
]

TEST_REQUIREMENTS = [
    'pytest>=3',
    'pytest-console-scripts>=0.2',
    'flake8>=3.7',
    'pylint>=2.4',
    'pytest-flake8',
    'pytest-pylint',
    'flaky',
    'python-dotenv',
]

setup(
    author="Johan Thorén",
    author_email='johan@thoren.xyz',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Nagios plugin to check SL delays for a given site",
    entry_points='''
        [console_scripts]
        check_sl_delay=check_sl_delay.check_sl_delay:cli
    ''',
    install_requires=REQUIREMENTS,
    license="ISC license",
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords='check_sl_delay',
    name='check_sl_delay',
    packages=find_packages(include=['check_sl_delay', 'check_sl_delay.py']),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    version='0.1.3',
    zip_safe=False,
)
