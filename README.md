check\_sl\_delay
================
[![image](https://img.shields.io/pypi/v/check_sl_delay.svg)](https://pypi.python.org/pypi/check_sl_delay)
[![Build Status](https://travis-ci.com/johanthoren/check_sl_delay.svg?token=xKPVyJ8cXNtwnz8Trqfu&branch=master)](https://travis-ci.com/johanthoren/check_sl_delay)

## Introduction

*check_sl_delay* is a simple Nagios plugins to check the percentage of late departures for any given site.

## Installation

The easiest way to install *check_sl_delay* is via *pip*. Make sure to run this with python3, in some environments *pip* should be replaced with *pip3* or similar.

### For a specific user:
```bash
$ pip install --user check-sl-delay
```

This will put the executable *check_sl_delay* in ~/.local/bin/, so make sure that this is part of your $PATH variable.

### System wide:
```bash
# pip install check-sl-delay
```

This will put the executable *check_sl_delay* in /usr/local/bin/, which is usually already part of the system wide $PATH. Check the documentation of your specific OS.

## Usage

Once you have made sure that *check_sl_delay* is on your $PATH, you can find some useful information with the `--help` option:

```bash
$ check_sl_delay --help
Usage: check_sl_delay [OPTIONS]

  check_sl_delay will connect to the SL API to determine the percentage of
  delayed departures for any given site-id.

  The site-id can be found using the API SL Platsuppslag:
  https://www.trafiklab.se/api/sl-platsuppslag/dokumentation

  Example: check_sl_delay -p 10 -m 1 -i 1002 -T METRO -w 20 -c 30

  The above example will check the site 1002 (T-Centralen) for all METRO
  departures in the coming 10 minutes. It will warn if the percentage of
  departures that are more than 1 minute late is 20% or more of the total
  amount of departures for the time period. It will crit if the same
  percentage is 30% or more.

Options:
  -w, --warning INTEGER RANGE     Warning threshold (0-100), warning if the
                                  percentage of departures having delays above
                                  --minutes is greater or equal than this
                                  option. Must be less than --critical.

  -c, --critical INTEGER RANGE    Critical threshold (0-100), critical if the
                                  percentage of departures having delays above
                                  --minutes is greater or equal than this
                                  option. Must be greater than --warning.

  -p, --period INTEGER            Time period to check, in minutes.
                                  [required]

  -m, --minutes INTEGER RANGE     Delay threshold, in minutes.  [required]
  -i, --site-id INTEGER           Site-id to check.  [required]
  -t, --timeout INTEGER RANGE     Plugin timeout, in seconds.
  -T, --traffic-type [BUS|METRO|TRAIN]
                                  Traffic type to check.  [required]
  --help                          Show this message and exit
  ```
