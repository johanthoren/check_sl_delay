#!/usr/bin/env python
# pylint: disable=too-many-arguments
"""Main module."""

from datetime import datetime
import json
import sys
import click
from func_timeout import func_timeout, FunctionTimedOut
import requests


def maybe_output(print_on_levels=[0], actual_level=0, msg=''):
    "Determine wether or not to print output to stdout based on verbosity."
    if msg and actual_level in print_on_levels:
        click.echo(msg)


def generate_perfdata_string(value='U', warning='', critical=''):
    """Generate a valid perfdata string based on `value`, `warning` and
    `critical`."""
    perfdata_string = ('|\'Percentage delayed\'=' + str(value) + '%;' +
                       str(warning) + ';' + str(critical))
    return perfdata_string


def exit_plugin(state=3,
                value='U',
                name='',
                warning='',
                critical='',
                minutes='',
                error='No error information provided',
                verbosity=0):
    "Exit the plugin with a valid exit code and string."
    # The function will not literally exit, but throw a click.ClickException
    # which will be caught in the `cli` function.

    # Service status options to pick from, depending on the state to return.
    service_status_options = {
        0: 'OK',
        1: 'WARNING',
        2: 'CRITICAL',
        3: 'UNKNOWN'
    }
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg='Deciding what service status to print. (exit_plugin)')
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg='State is: ' + str(state) + '. (exit_plugin)')

    # Pick the service status corresponding to `state`, or fallback to 'ERROR'.
    service_status = service_status_options.get(state, 'ERROR')

    # Early bail if the state is either 'ERROR' or 'UNKNOWN'.
    if service_status in ('ERROR', 'UNKNOWN'):
        # Print the actual check output and then raise the exception.
        click.echo(service_status + ': ' + error)
        raise click.ClickException(str(state))

    if name:
        name_string = ('at ' + name + ' ')
    else:
        name_string = ''

    # Make sure that we give the message with the correct wording, either plural
    # or singular.
    if isinstance(minutes, int) and minutes >= 2 or minutes == 0:
        # Output for -vv:
        maybe_output(
            print_on_levels=[2],
            actual_level=verbosity,
            msg='Formatting value message for minutes in plural. (exit_plugin)'
        )
        value_message = ('% of the departures ' + name_string +
                         'are delayed more than ' + str(minutes) + ' minutes')
    elif isinstance(minutes, int):
        # Output for -vv:
        maybe_output(
            print_on_levels=[2],
            actual_level=verbosity,
            msg=
            'Formatting value message for minutes in singular. (exit_plugin)')
        value_message = ('% of the departures ' + name_string +
                         'are delayed more than ' + str(minutes) + ' minute')
    else:
        value_message = ''

    # Output for -vv:
    maybe_output(
        print_on_levels=[2],
        actual_level=verbosity,
        msg='Generating exit message and perfdata string. (exit_plugin)')

    # Print the short version of the output if the option -v has not been set.
    maybe_output(print_on_levels=[0],
                 actual_level=verbosity,
                 msg=str(service_status + ': ' + str(value) + '%' +
                         generate_perfdata_string(value, warning, critical)))

    # Print the longer version of the output if either -v or -vv have been set.
    maybe_output(print_on_levels=[1, 2],
                 actual_level=verbosity,
                 msg=str(service_status + ': ' + str(value) + value_message +
                         generate_perfdata_string(value, warning, critical)))

    # Finally throw the exception to exit the plugin via the exception being
    # caught in `cli`.

    # The `state` needs to be awkwardly converted to a string to be passed on
    # as an exception message.
    raise click.ClickException(str(state))


def exit_invalid_id(site_id):
    "Exit the plugin with an error message noting the invalid id."
    exit_plugin(state=3, error='Invalid site id: ' + str(site_id))


def fetch_site(site_id, verbosity=0):
    "Verify that the site_id is valid and return the `name` of the site."
    api_key = '76be1103a7cc4a458cbf807e814b0dd6'
    url = ('https://api.sl.se/api2/typeahead.json/'
           '?key=' + api_key + '&searchstring=' + str(site_id))
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg=str('URL: ' + url + ' (fetch_site)'))

    try:
        # Output for -vv:
        maybe_output(print_on_levels=[2],
                     actual_level=verbosity,
                     msg=str('Fetching API response for site : ' +
                             str(site_id) + '. (fetch_site)'))
        response = requests.get(url)

    # If there is a problem with the connection:
    except requests.exceptions.ConnectionError as exception_message:
        exit_plugin(state=3,
                    error='Encountered an exception during HTTP request: ' +
                    str(exception_message))

    try:
        json_response = response.json()

    # If the response does not conform to json, or some other error while
    # decoding the json:
    except json.decoder.JSONDecodeError as exception_message:
        exit_plugin(state=3,
                    error='Encountered an exception during JSON Decoding: ' +
                    str(exception_message))

    try:
        response_id = json_response['ResponseData'][0]['SiteId']
        response_name = json_response['ResponseData'][0]['Name']
        # Because some names have extra whitespaces in them:
        stripped_name = ' '.join(response_name.split())

    except KeyError:
        exit_invalid_id(site_id)
    except IndexError:
        exit_invalid_id(site_id)

    # More than 1 items indicates that there was no exact match on the id.
    if len(json_response['ResponseData']) > 1:
        exit_invalid_id(site_id)

    # As a last security, double check that the given `site_id` is in fact
    # the same as the object returned.
    if str(response_id) != str(site_id):
        # Output for -vv:
        maybe_output(print_on_levels=[2],
                     actual_level=verbosity,
                     msg='Response ID does not correspond to Site ID.')
        exit_invalid_id(site_id)

    # Return the name for later use in the message.
    return stripped_name


def fetch_response(site_id, time_window, verbosity=0):
    "Method to fetch the API response."
    api_key = '0f3031b9578149649068f90f7e499b35'
    url = ('https://api.sl.se/api2/realtimedeparturesV4.json/'
           '?key=' + api_key + '&siteid=' + str(site_id) + '&timewindow=' +
           str(time_window))
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg=str('URL: ' + url + ' (fetch_response)'))

    try:
        # Output for -vv:
        maybe_output(print_on_levels=[2],
                     actual_level=verbosity,
                     msg='Fetching API response. (fetch_response)')
        response = requests.get(url)

    # If there is a problem with the connection:
    except requests.exceptions.ConnectionError as exception_message:
        exit_plugin(state=3,
                    error='Encountered an exception during HTTP request: ' +
                    str(exception_message))

    try:
        json_response = response.json()

    # If the response does not conform to json, or some other error while
    # decoding the json:
    except json.decoder.JSONDecodeError as exception_message:
        exit_plugin(state=3,
                    error='Encountered an exception during JSON Decoding: ' +
                    str(exception_message))

    # Return the full json reponse.
    return json_response


def structure_departure(departure):
    """Structure data for a given `departure` into a dictionary containing the
    key `scheduled`, `expected` and `delay`."
    """
    datetime_re = '%Y-%m-%dT%H:%M:%S'
    scheduled = datetime.strptime(departure['TimeTabledDateTime'], datetime_re)
    expected = datetime.strptime(departure['ExpectedDateTime'], datetime_re)

    # If the departure is delayed, then calculate the diff.
    if expected > scheduled:
        delay_time = expected - scheduled
        delay = delay_time.seconds
    else:
        delay = 0

    return {'scheduled': scheduled, 'expected': expected, 'delay': delay}


def extract_departures(response, traffic_type, verbosity=0):
    "Method to parse API response."
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg='Parsing API response. (extract_departures)')
    departures = []
    # Populate the list of departures with dictionaries representing each
    # departure. The format of the dictionaries is like this:

    # {'delay': 120,
    #  'expected': datetime(2020, 3, 19, 13, 21),
    #  'scheduled': datetime(2020, 3, 19, 13, 19)}

    for departure in response['ResponseData'][traffic_type]:
        departures.append(structure_departure(departure))
    return departures


def calculate_delays(departures, verbosity=0):
    "Method to extract all delays from the parsed data."
    # Output for -vv:
    maybe_output(
        print_on_levels=[2],
        actual_level=verbosity,
        msg='Extracting the delays from the parsed data. (calculate_delays)')
    delays = []
    # Extract the delays from the dictionaries of departures like this:
    # [0, 125, 30, 0]
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


def get_diffs(site_id, time_window, traffic_type, verbosity=0):
    """Get the diffs between scheduled and expected departures and return them
    in whole minutes."""
    # Output for -vv:
    maybe_output(
        print_on_levels=[2],
        actual_level=verbosity,
        msg=
        'Calculating diff between expected and scheduled departures. (get_diffs)'
    )
    # This higher order function calls on the various functions to get to work.
    diffs = calculate_delays(
        extract_departures(fetch_response(site_id, time_window, verbosity),
                           traffic_type, verbosity), verbosity)
    minutes = convert_minutes(diffs)
    return minutes


def compare_to_threshold(diffs, threshold, verbosity=0):
    "Compare the diffs to the threshold and return True for offenders."
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg=str('Comparing diffs to threshold: ' + str(threshold) +
                         ' (compare_to_threshold)'))
    results = []
    # Will produce a list of either True or False, like this:
    # [True, True, False]
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


def calculate_final_value(site_id,
                          time_window,
                          traffic_type,
                          threshold,
                          verbosity=0):
    """Calculate the final `value` based on the results from `get_diffs`
    using `calculate_percentage_of_offenders` and `compare_to_threshold`."""
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg='Calculating the final value. (calculate_final_value)')
    diffs = get_diffs(site_id, time_window, traffic_type, verbosity)
    value = calculate_percentage_of_offenders(
        compare_to_threshold(diffs, threshold, verbosity))
    return value


def determine_state(value, warning='', critical=''):
    """Based on `value`, calculate if it is greater or equal either `critical`
    or `warning` and return the corresponding state as an integer of either
    2 (CRITICAL), 1 (WARNING) or 0 (OK)."""
    if isinstance(critical, int) and value >= critical:
        return 2
    if isinstance(warning, int) and value >= warning:
        return 1
    return 0


def plugin_main(site_id,
                period,
                traffic_type_api_format,
                minutes,
                warning,
                critical,
                verbosity=0):
    """Main function that will execute the actual API call function and
    determine the state based on the value returned."""
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg="Enter the function `plugin_main`.")
    name = fetch_site(site_id, verbosity)

    value = calculate_final_value(site_id, period, traffic_type_api_format,
                                  minutes, verbosity)
    # Output for -vv:
    maybe_output(print_on_levels=[2],
                 actual_level=verbosity,
                 msg=str('Percentage of departures delayed above threshold: ' +
                         str(value) + ' (plugin_main)'))

    state = determine_state(value, warning, critical)

    if not isinstance(warning, int):
        warning = ''
    if not isinstance(critical, int):
        critical = ''

    exit_plugin(state=state,
                value=value,
                name=name,
                warning=warning,
                critical=critical,
                minutes=minutes,
                verbosity=verbosity)


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
@click.option('-i',
              '--site-id',
              required=True,
              type=click.IntRange(1, ),
              help='Site-id to check.')
@click.option('-m',
              '--minutes',
              required=True,
              type=click.IntRange(0, ),
              help='Delay threshold, in minutes.')
@click.option('-p',
              '--period',
              required=True,
              type=click.INT,
              help='Time period to check, in minutes.')
@click.option('-t',
              '--timeout',
              default=10,
              type=click.IntRange(0, ),
              help='Plugin timeout, in seconds.')
@click.option('-T',
              '--traffic-type',
              required=True,
              type=click.Choice(['BUS', 'METRO', 'TRAIN']),
              help='Traffic type to check.')
@click.option('-v',
              '--verbose',
              count=True,
              help='Use 2 times for higher verbosity.')
@click.version_option()
def cli(warning, critical, site_id, minutes, period, timeout, traffic_type,
        verbose):
    """check_sl_delay will connect to the SL API to determine the percentage of
    delayed departures for any given site-id.

    The site-id can be found using the API SL Platsuppslag:
        https://www.trafiklab.se/api/sl-platsuppslag/dokumentation

    Example: check_sl_delay -p 10 -m 1 -i 1002 -T METRO -w 20 -c 30

    The above example will check the site 1002 (T-Centralen) for all METRO
    departures in the coming 10 minutes. It will warn if the percentage of
    departures that are more than 1 minute late is 20% or more of the total
    amount of departures for the time period. It will crit if the same
    percentage is 30% or more."""

    # Misc output for -vv:
    maybe_output(print_on_levels=[2], actual_level=verbose, msg='Variables:')
    maybe_output(print_on_levels=[2],
                 actual_level=verbose,
                 msg=str('Threshold = ' + str(minutes) + ' minutes.'))
    maybe_output(print_on_levels=[2],
                 actual_level=verbose,
                 msg=str('Warning = ' + str(warning)))
    maybe_output(print_on_levels=[2],
                 actual_level=verbose,
                 msg=str('Critical = ' + str(critical)))

    traffic_type_api_format_options = {
        'METRO': 'Metros',
        'BUS': 'Buses',
        'TRAIN': 'Trains'
    }

    # Convert the transportation type string to be in a format recognized
    # by the API:
    traffic_type_api_format = traffic_type_api_format_options[traffic_type]

    # Exit functionality below:

    # This seemingly ugly solution is necessary to escape the grip of 'click'
    # with an exit code other than 0 and without printing anything to stderr.
    def exit_with_correct_code(exit_code):
        sys.exit(int(str(exit_code)))

    # Wrap the `plugin_main` function in `func_timeout` to be able to set a
    # timeout option (-t) for the whole plugin, not only network related
    # functions.
    try:
        # Validation of crit and warn needs to be inside the try clause to
        # correctly exit.
        if isinstance(critical, int) and isinstance(
                warning, int) and warning > critical:
            exit_plugin(
                4,
                error=('--warning (' + str(warning) +
                       ') higher than --critical (' + str(critical) + ')'))

        func_timeout(timeout,
                     plugin_main,
                     args=(site_id, period, traffic_type_api_format, minutes,
                           warning, critical, verbose))

    # This is the common exit point for most cases not related to input
    # validation or timeouts:
    except click.ClickException as exit_code:
        exit_with_correct_code(exit_code)

    except FunctionTimedOut:
        if timeout == 1:
            timeout_message = 'Timeout reached after 1 second'
        else:
            timeout_message = ('Timeout reached after ' + str(timeout) +
                               ' seconds')

        # Go through the `exit_plugin` function to set the correct message.
        try:
            exit_plugin(error=timeout_message)

        # This is the actual exit point for timeouts:
        except click.ClickException as exit_code:
            exit_with_correct_code(exit_code)
