#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

requirements = [
    'requests>=2.23',
    'Click>=7.1',
    'func-timeout>=4.3',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest>=3',
    'pytest-console-scripts>=0.2',
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
    install_requires=requirements,
    license="ISC license",
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords='check_sl_delay',
    name='check_sl_delay',
    packages=find_packages(include=['check_sl_delay', 'check_sl_delay.py']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.1',
    zip_safe=False,
)
