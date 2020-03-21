#!/usr/bin/env python
# pylint: disable=too-many-arguments
"""Main module."""

from datetime import datetime
import json
import logging
import sys
import click
from func_timeout import func_timeout, FunctionTimedOut
import requests

LOG = logging.getLogger(__name__)
API_KEY = '0f3031b9578149649068f90f7e499b35'


def generate_perfdata_string(value='U', warning='', critical=''):
    """Generate a valid perfdata string based on `value`, `warning` and
    `critical`."""
    perfdata_string = ('|\'Percentage delayed\'=' + str(value) + '%;' +
                       str(warning) + ';' + str(critical))
    return perfdata_string


def exit_plugin(state=3,
                value='U',
                warning='',
                critical='',
                minutes='',
                error='No error information provided'):
    "Exit the plugin with a valid exit code and string."
    service_status_options = {
        0: 'OK',
        1: 'WARNING',
        2: 'CRITICAL',
        3: 'UNKNOWN'
    }
    service_status = service_status_options.get(state, 'ERROR')

    if service_status in ('ERROR', 'UNKNOWN'):
        print(service_status + ': ' + error)
        sys.exit(state)

    if minutes and minutes >= 2 or minutes == 0:
        value_message = ('% of the departures are delayed more than ' +
                         str(minutes) + ' minutes')
    elif minutes:
        value_message = ('% of the departures are delayed more than ' +
                         str(minutes) + ' minute')
    else:
        value_message = ''

    exit_message = (service_status + ': ' + str(value) + value_message +
                    generate_perfdata_string(value, warning, critical))
    print(exit_message)
    sys.exit(state)


def fetch_response(site_id, time_window):
    "Method to fetch the API response."
    LOG.info('Fetching API response')
    url = ('https://api.sl.se/api2/realtimedeparturesV4.json/'
           '?key=' + API_KEY + '&siteid=' + str(site_id) + '&timewindow=' +
           str(time_window))

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as exception_message:
        exit_plugin(state=3,
                    error='Encountered an exception during HTTP request: ' +
                    str(exception_message))

    try:
        json_response = response.json()
    except json.decoder.JSONDecodeError as exception_message:
        exit_plugin(state=3,
                    error='Encountered an exception during JSON Decoding: ' +
                    str(exception_message))

    return json_response


def structure_departure(departure):
    """Structure data for a given `departure` into a dictionary containing the
    key `scheduled`, `expected` and `delay`."
    """
    datetime_re = '%Y-%m-%dT%H:%M:%S'
    scheduled = datetime.strptime(departure['TimeTabledDateTime'], datetime_re)
    expected = datetime.strptime(departure['ExpectedDateTime'], datetime_re)

    if expected > scheduled:
        delay_time = expected - scheduled
        delay = delay_time.seconds
    else:
        delay = 0

    return {'scheduled': scheduled, 'expected': expected, 'delay': delay}


def extract_departures(response, traffic_type):
    "Method to parse API response."
    LOG.info('Parsing API response')
    departures = []
    for departure in response['ResponseData'][traffic_type]:
        departures.append(structure_departure(departure))
    return departures


def calculate_delays(departures):
    "Method to extract all delays from the parsed data."
    LOG.info('Extracting the delays from the parsed data')
    delays = []
    for departure in departures:
        delays.append(departure['delay'])
    return delays


def to_whole_minutes(seconds):
    "Divide `seconds` by 60 to convert to whole minutes."
    minutes = seconds // 60
    return minutes


def convert_minutes(diffs):
    "Convert all `diffs` to be in whole minutes instead of seconds."
    minutes = []
    for seconds in diffs:
        minutes.append(to_whole_minutes(seconds))
    return minutes


def get_diffs(site_id, time_window, traffic_type):
    """Get the diffs between scheduled and expected departures and return them
    in whole minutes."""
    diffs = calculate_delays(
        extract_departures(fetch_response(site_id, time_window), traffic_type))
    minutes = convert_minutes(diffs)
    return minutes


def compare_to_threshold(diffs, threshold):
    "Compare the diffs to the threshold and return True for offenders."
    results = []
    for diff in diffs:
        results.append(int(diff) >= int(threshold))
    return results


def calculate_percentage_of_offenders(results):
    """Calculate what percentage of `results` are True, which means that they
    were deemed above the threshold by `compare_to_threshold`."""
    total_count = len(results)
    true_count = results.count(True)

    # Limit the result to an integer, for easy comparison.
    # Acceptable since we are only going to compare against integers,
    # and since we only care wether or not the result is equal to or greater
    # than the threshold.
    if true_count > 0 and total_count > 0:
        percentage = int(100 * float(true_count) / float(total_count))
    else:
        percentage = 0

    return percentage


def calculate_final_value(site_id, time_window, traffic_type, threshold):
    """Calculate the final `value` based on the results from `get_diffs`
    using `calculate_percentage_of_offenders` and `compare_to_threshold`."""
    diffs = get_diffs(site_id, time_window, traffic_type)
    value = calculate_percentage_of_offenders(
        compare_to_threshold(diffs, threshold))
    return value


def determine_state(value, warning='', critical=''):
    """Based on `value`, calculate if it is above either `critical` or
    `warning` and return the corresponding state as an integer of either
    2 (CRITICAL), 1 (WARNING) or 0 (OK)."""
    if critical and value >= critical:
        return 2
    if warning and value >= warning:
        return 1
    return 0


def plugin_main(site_id, period, traffic_type_api_format, minutes, warning,
                critical):
    """Main function that will execute the actual API call function and
    determine the state based on the value returned."""
    value = calculate_final_value(site_id, period, traffic_type_api_format,
                                  minutes)
    LOG.debug('Percentage of departures delayed above threshold: ' +
              str(value) + '%')

    state = determine_state(value, warning, critical)

    if not warning:
        warning = ''
    if not critical:
        critical = ''

    exit_plugin(state=state,
                value=value,
                warning=warning,
                critical=critical,
                minutes=minutes)


@click.command()
@click.option(
    '-w',
    '--warning',
    type=click.IntRange(0, 100),
    help=('Warning threshold (0-100), warning if the percentage ' +
          'of departures having delays above --minutes is greater ' +
          'or equal than this option. Must be less than ' + '--critical.'))
@click.option(
    '-c',
    '--critical',
    type=click.IntRange(0, 100),
    help=('Critical threshold (0-100), critical if the percentage ' +
          'of departures having delays above --minutes is greater ' +
          'or equal than this option. Must be greater than ' + '--warning.'))
@click.option('-p',
              '--period',
              required=True,
              type=click.INT,
              help='Time period to check, in minutes.')
@click.option('-m',
              '--minutes',
              required=True,
              type=click.IntRange(0, ),
              help='Delay threshold, in minutes.')
@click.option('-i',
              '--site-id',
              required=True,
              type=click.INT,
              help='Site-id to check')
@click.option('-t',
              '--timeout',
              default=10,
              type=click.IntRange(1, ),
              help='Plugin timeout, in seconds.')
@click.option('-T',
              '--traffic-type',
              required=True,
              type=click.Choice(['BUS', 'METRO', 'TRAIN']),
              help='Traffic type to check')
def cli(warning, critical, period, minutes, site_id, timeout, traffic_type):
    "Main function."
    if critical and warning > critical:
        exit_plugin(4, ('--warning (' + str(warning) +
                        ') higher than --critical (' + str(critical) + ')'))

    LOG.debug('Threshold: ' + str(minutes) + ' minutes')
    if warning:
        LOG.debug('Warning: ' + str(warning) + '%')
    if critical:
        LOG.debug('Critical: ' + str(critical) + '%')

    traffic_type_api_format_options = {
        'METRO': 'Metros',
        'BUS': 'Buses',
        'TRAIN': 'Trains'
    }

    traffic_type_api_format = traffic_type_api_format_options[traffic_type]

    try:
        func_timeout(timeout,
                     plugin_main,
                     args=(site_id, period, traffic_type_api_format, minutes,
                           warning, critical))

    except FunctionTimedOut:
        if timeout == 1:
            timeout_message = 'Timeout reached after 1 second'
        else:
            timeout_message = ('Timeout reached after ' + str(timeout) +
                               ' seconds')

        exit_plugin(error=timeout_message)
