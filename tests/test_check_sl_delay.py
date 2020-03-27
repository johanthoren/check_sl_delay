#!/usr/bin/env python
# pylint: disable=redefined-outer-name
"""Tests for `check_sl_delay` package."""

from datetime import datetime
import json
import os
import pytest
import click

from dotenv import load_dotenv
from flaky import flaky

from check_sl_delay import check_sl_delay

load_dotenv()
SITE_API_KEY = os.getenv('SITE_API_KEY')
DEPARTURE_API_KEY = os.getenv('DEPARTURE_API_KEY')


@pytest.fixture
def response():
    "Example API response."
    test_response = '''
{
    "StatusCode": 0,
    "Message": null,
    "ExecutionTime": 253,
    "ResponseData": {
        "LatestUpdate":
        "2020-03-19T13:11:41",
        "DataAge":
        33,
        "Metros": [{
            "GroupOfLine": "tunnelbanans blå linje",
            "DisplayTime": "4 min",
            "TransportMode": "METRO",
            "LineNumber": "10",
            "Destination": "Kungsträdgården",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 3052,
            "StopPointDesignation": "6",
            "TimeTabledDateTime": "2020-03-19T13:12:00",
            "ExpectedDateTime": "2020-03-19T13:16:20",
            "JourneyNumber": 30223,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans röda linje",
            "DisplayTime": "Nu",
            "TransportMode": "METRO",
            "LineNumber": "14",
            "Destination": "Mörby centrum",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 1051,
            "StopPointDesignation": "3",
            "TimeTabledDateTime": "2020-03-19T13:12:45",
            "ExpectedDateTime": "2020-03-19T13:12:53",
            "JourneyNumber": 20272,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans röda linje",
            "DisplayTime": "Nu",
            "TransportMode": "METRO",
            "LineNumber": "13",
            "Destination": "Norsborg",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 2052,
            "StopPointDesignation": "2",
            "TimeTabledDateTime": "2020-03-19T13:12:45",
            "ExpectedDateTime": "2020-03-19T13:12:59",
            "JourneyNumber": 20844,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans gröna linje",
            "DisplayTime": "1 min",
            "TransportMode": "METRO",
            "LineNumber": "18",
            "Destination": "Alvik",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 2051,
            "StopPointDesignation": "1",
            "TimeTabledDateTime": "2020-03-19T13:13:30",
            "ExpectedDateTime": "2020-03-19T13:13:30",
            "JourneyNumber": 10561,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans gröna linje",
            "DisplayTime": "2 min",
            "TransportMode": "METRO",
            "LineNumber": "18",
            "Destination": "Farsta strand",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 1052,
            "StopPointDesignation": "4",
            "TimeTabledDateTime": "2020-03-19T13:14:30",
            "ExpectedDateTime": "2020-03-19T13:14:30",
            "JourneyNumber": 10572,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans blå linje",
            "DisplayTime": "3 min",
            "TransportMode": "METRO",
            "LineNumber": "10",
            "Destination": "Hjulsta",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 3051,
            "StopPointDesignation": "5",
            "TimeTabledDateTime": "2020-03-19T13:15:15",
            "ExpectedDateTime": "2020-03-19T13:15:15",
            "JourneyNumber": 30410,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans röda linje",
            "DisplayTime": "3 min",
            "TransportMode": "METRO",
            "LineNumber": "14",
            "Destination": "Liljeholmen",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 2052,
            "StopPointDesignation": "2",
            "TimeTabledDateTime": "2020-03-19T13:16:00",
            "ExpectedDateTime": "2020-03-19T13:15:56",
            "JourneyNumber": 20503,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans röda linje",
            "DisplayTime": "4 min",
            "TransportMode": "METRO",
            "LineNumber": "13",
            "Destination": "Ropsten",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 1051,
            "StopPointDesignation": "3",
            "TimeTabledDateTime": "2020-03-19T13:15:45",
            "ExpectedDateTime": "2020-03-19T13:16:20",
            "JourneyNumber": 20700,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans gröna linje",
            "DisplayTime": "4 min",
            "TransportMode": "METRO",
            "LineNumber": "19",
            "Destination": "Hässelby strand",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 2051,
            "StopPointDesignation": "1",
            "TimeTabledDateTime": "2020-03-19T13:16:30",
            "ExpectedDateTime": "2020-03-19T13:16:30",
            "JourneyNumber": 10565,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans blå linje",
            "DisplayTime": "5 min",
            "TransportMode": "METRO",
            "LineNumber": "11",
            "Destination": "Kungsträdgården",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 3052,
            "StopPointDesignation": "6",
            "TimeTabledDateTime": "2020-03-19T13:17:00",
            "ExpectedDateTime": "2020-03-19T13:17:47",
            "JourneyNumber": 30055,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans gröna linje",
            "DisplayTime": "5 min",
            "TransportMode": "METRO",
            "LineNumber": "17",
            "Destination": "Skarpnäck",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 1052,
            "StopPointDesignation": "4",
            "TimeTabledDateTime": "2020-03-19T13:18:00",
            "ExpectedDateTime": "2020-03-19T13:18:00",
            "JourneyNumber": 10567,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans röda linje",
            "DisplayTime": "6 min",
            "TransportMode": "METRO",
            "LineNumber": "14",
            "Destination": "Mörby centrum",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 1051,
            "StopPointDesignation": "3",
            "TimeTabledDateTime": "2020-03-19T13:18:45",
            "ExpectedDateTime": "2020-03-19T13:19:07",
            "JourneyNumber": 20145,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans röda linje",
            "DisplayTime": "7 min",
            "TransportMode": "METRO",
            "LineNumber": "14",
            "Destination": "Fruängen",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 2052,
            "StopPointDesignation": "2",
            "TimeTabledDateTime": "2020-03-19T13:19:45",
            "ExpectedDateTime": "2020-03-19T13:19:52",
            "JourneyNumber": 20504,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans gröna linje",
            "DisplayTime": "7 min",
            "TransportMode": "METRO",
            "LineNumber": "17",
            "Destination": "Åkeshov",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 2051,
            "StopPointDesignation": "1",
            "TimeTabledDateTime": "2020-03-19T13:20:00",
            "ExpectedDateTime": "2020-03-19T13:20:00",
            "JourneyNumber": 10571,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans blå linje",
            "DisplayTime": "13:20",
            "TransportMode": "METRO",
            "LineNumber": "11",
            "Destination": "Akalla",
            "JourneyDirection": 1,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 3051,
            "StopPointDesignation": "5",
            "TimeTabledDateTime": "2020-03-19T13:20:15",
            "ExpectedDateTime": "2020-03-19T13:20:15",
            "JourneyNumber": 30411,
            "Deviations": null
        }, {
            "GroupOfLine": "tunnelbanans gröna linje",
            "DisplayTime": "8 min",
            "TransportMode": "METRO",
            "LineNumber": "19",
            "Destination": "Hagsätra",
            "JourneyDirection": 2,
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 1051,
            "StopPointNumber": 1052,
            "StopPointDesignation": "4",
            "TimeTabledDateTime": "2020-03-19T13:21:00",
            "ExpectedDateTime": "2020-03-19T13:21:00",
            "JourneyNumber": 10560,
            "Deviations": null
        }],
        "Buses": [{
            "GroupOfLine": null,
            "TransportMode": "BUS",
            "LineNumber": "69",
            "Destination": "Kaknästornet",
            "JourneyDirection": 1,
            "StopAreaName": "Centralen",
            "StopAreaNumber": 10537,
            "StopPointNumber": 10537,
            "StopPointDesignation": "L",
            "TimeTabledDateTime": "2020-03-19T13:19:00",
            "ExpectedDateTime": "2020-03-19T13:21:00",
            "DisplayTime": "8 min",
            "JourneyNumber": 42553,
            "Deviations": null
        }, {
            "GroupOfLine": null,
            "TransportMode": "BUS",
            "LineNumber": "54",
            "Destination": "Storängsbotten",
            "JourneyDirection": 1,
            "StopAreaName": "Centralen",
            "StopAreaNumber": 10537,
            "StopPointNumber": 10537,
            "StopPointDesignation": "L",
            "TimeTabledDateTime": "2020-03-19T13:19:00",
            "ExpectedDateTime": "2020-03-19T13:19:35",
            "DisplayTime": "7 min",
            "JourneyNumber": 38117,
            "Deviations": null
        }],
        "Trains": [{
            "SecondaryDestinationName": null,
            "GroupOfLine": "Pendeltåg",
            "TransportMode": "TRAIN",
            "LineNumber": "41",
            "Destination": "Märsta",
            "JourneyDirection": 2,
            "StopAreaName": "Stockholm City",
            "StopAreaNumber": 5310,
            "StopPointNumber": 5312,
            "StopPointDesignation": "2",
            "TimeTabledDateTime": "2020-03-19T13:15:00",
            "ExpectedDateTime": "2020-03-19T13:15:00",
            "DisplayTime": "2 min",
            "JourneyNumber": 2736,
            "Deviations": null
        }, {
            "SecondaryDestinationName": null,
            "GroupOfLine": "Pendeltåg",
            "TransportMode": "TRAIN",
            "LineNumber": "42X",
            "Destination": "Nynäshamn",
            "JourneyDirection": 1,
            "StopAreaName": "Stockholm City",
            "StopAreaNumber": 5310,
            "StopPointNumber": 5311,
            "StopPointDesignation": "3",
            "TimeTabledDateTime": "2020-03-19T13:16:00",
            "ExpectedDateTime": "2020-03-19T13:16:00",
            "DisplayTime": "3 min",
            "JourneyNumber": 12337,
            "Deviations": null
        }, {
            "SecondaryDestinationName": null,
            "GroupOfLine": "Pendeltåg",
            "TransportMode": "TRAIN",
            "LineNumber": "43",
            "Destination": "Västerhaninge",
            "JourneyDirection": 1,
            "StopAreaName": "Stockholm City",
            "StopAreaNumber": 5310,
            "StopPointNumber": 5313,
            "StopPointDesignation": "4",
            "TimeTabledDateTime": "2020-03-19T13:21:00",
            "ExpectedDateTime": "2020-03-19T13:21:00",
            "DisplayTime": "8 min",
            "JourneyNumber": 2837,
            "Deviations": null
        }],
        "Trams": [{
            "TransportMode": "TRAM",
            "LineNumber": "7",
            "Destination": "Djurgården Skansen",
            "JourneyDirection": 1,
            "GroupOfLine": "Spårväg City",
            "StopAreaName": "T-Centralen",
            "StopAreaNumber": 4301,
            "StopPointNumber": 4300,
            "StopPointDesignation": null,
            "TimeTabledDateTime": "2020-03-19T13:15:00",
            "ExpectedDateTime": "2020-03-19T13:15:00",
            "DisplayTime": "2 min",
            "JourneyNumber": 111,
            "Deviations": null
        }],
        "Ships": [],
        "StopPointDeviations": []
    }
}
'''
    return json.loads(test_response)


@pytest.fixture
def departure_example():
    "Example data."
    example = '''
{
            "SecondaryDestinationName": null,
            "GroupOfLine": "Pendeltåg",
            "TransportMode": "TRAIN",
            "LineNumber": "43",
            "Destination": "Västerhaninge",
            "JourneyDirection": 1,
            "StopAreaName": "Stockholm City",
            "StopAreaNumber": 5310,
            "StopPointNumber": 5313,
            "StopPointDesignation": "4",
            "TimeTabledDateTime": "2020-03-19T13:21:00",
            "ExpectedDateTime": "2020-03-19T13:23:30",
            "DisplayTime": "8 min",
            "JourneyNumber": 2837,
            "Deviations": null
        }
'''
    return json.loads(example)


@pytest.fixture
def traffic_types():
    "Traffic types to be used by tests."
    return ['Buses', 'Metros', 'Trains']


def test_structure_departure(departure_example):
    "Test that the structure_departure function correctly extracts data."
    assert check_sl_delay.structure_departure(departure_example) == {
        'delay': 150,
        'expected': datetime(2020, 3, 19, 13, 23, 30),
        'scheduled': datetime(2020, 3, 19, 13, 21)
    }


def test_extract_departures(response, traffic_types):
    "Test that departures are correctly handled when iterated over."
    func = check_sl_delay.extract_departures

    for traffic_type in traffic_types:
        assert isinstance(func(response, traffic_type), list)

    buses = func(response, 'Buses')
    metros = func(response, 'Metros')
    trains = func(response, 'Trains')

    assert len(buses) == 2
    assert len(metros) == 16
    assert len(trains) == 3
    assert buses[0] == {
        'delay': 120,
        'expected': datetime(2020, 3, 19, 13, 21),
        'scheduled': datetime(2020, 3, 19, 13, 19)
    }
    assert metros[0] == {
        'delay': 260,
        'expected': datetime(2020, 3, 19, 13, 16, 20),
        'scheduled': datetime(2020, 3, 19, 13, 12)
    }
    assert trains[0] == {
        'delay': 0,
        'expected': datetime(2020, 3, 19, 13, 15),
        'scheduled': datetime(2020, 3, 19, 13, 15)
    }


def test_calculate_delays(response, traffic_types):
    "Test that delays are correctly calculated and put into lists."
    func_cal = check_sl_delay.calculate_delays
    func_ext = check_sl_delay.extract_departures

    for traffic_type in traffic_types:
        assert isinstance(func_cal(func_ext(response, traffic_type)), list)
    buses = func_ext(response, 'Buses')
    metros = func_ext(response, 'Metros')
    trains = func_ext(response, 'Trains')

    assert func_cal(buses) == [120, 35]
    assert func_cal(metros) == [
        260, 8, 14, 0, 0, 0, 0, 35, 0, 47, 0, 22, 7, 0, 0, 0
    ]
    assert func_cal(trains) == [0, 0, 0]


def test_convert_minutes(response):
    "Test that whole minutes are correctly calculated from delays."
    func_cal = check_sl_delay.calculate_delays
    func_con = check_sl_delay.convert_minutes
    func_ext = check_sl_delay.extract_departures

    buses = func_cal(func_ext(response, 'Buses'))
    metros = func_cal(func_ext(response, 'Metros'))
    trains = func_cal(func_ext(response, 'Trains'))

    assert func_con(buses) == [2, 0]
    assert func_con(metros) == [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert func_con(trains) == [0, 0, 0]


def test_compare_to_threshold():
    "Test that compare_to_threshold give correct True or False answers."
    func = check_sl_delay.compare_to_threshold

    assert func([0, 2, 0], 0) == [True, True, True]
    assert func([0, 2, 0], 1) == [False, True, False]
    assert func([0, 2, 0], 2) == [False, True, False]
    assert func([0, 2, 0], 3) == [False, False, False]


def test_calculate_percentage_of_offenders():
    "Test that percentages are correctly calculated."
    func = check_sl_delay.calculate_percentage_of_offenders

    assert func([True, True, True]) == 100
    assert func([True, True, False]) == 66
    assert func([True, True, False, False]) == 50


def test_generate_perfdata_string():
    "Thest that proper perfdata strings are generated."
    func = check_sl_delay.generate_perfdata_string

    assert func(5, 0, 10) == '|\'Percentage delayed\'=5%;0;10'
    assert func(5, 10, 0) == '|\'Percentage delayed\'=5%;10;0'
    assert func(0, 10, 0) == '|\'Percentage delayed\'=0%;10;0'
    assert func(5, 10, 20) == '|\'Percentage delayed\'=5%;10;20'
    assert func(5, 10) == '|\'Percentage delayed\'=5%;10;'
    assert func(5) == '|\'Percentage delayed\'=5%;;'
    assert func() == '|\'Percentage delayed\'=U%;;'


@pytest.fixture(params=['0', '1', '2', '3', '4'])
def state_var(request):
    "Range of states for testing purposes."
    return request.param


def test_exit_plugin(state_var):
    "Test that `exit_plugin` does indeed exit with the correct code."
    with pytest.raises(click.ClickException) as pytest_wrapped_e:
        check_sl_delay.exit_plugin(state=state_var)
    assert pytest_wrapped_e.type == click.ClickException
    assert pytest_wrapped_e.value.message == state_var


def test_determine_state():
    "Test that the correct state is determined."
    func = check_sl_delay.determine_state
    assert func(0, warning=0) == 1


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_invalid_site_id(script_runner):
    """Test that the script returns the correct exit code and message on invalid
    site id."""
    ret = script_runner.run('check_sl_delay', '-i', '100', '-m', '1', '-p',
                            '10', '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY,
                            '-T', 'METRO', '-w', '10', '-c', '20', '-t', '5')
    assert not ret.success
    assert ret.stdout == 'UNKNOWN: Invalid site id: 100\n'
    assert ret.stderr == ''
    assert ret.returncode == 3


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_100_percent_ok(script_runner):
    """Test that the script returns the correct exit code and message on 100%
    delays without warning or critical defined."""
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '0',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-t', '5')

    assert ret.success
    assert ret.stdout == ('OK: 100% of the departures at Centralen ' +
                          '(Stockholm) are delayed more than 0 minutes' +
                          '|\'Percentage delayed\'=100%;;\n')
    assert ret.stderr == ''
    assert ret.returncode == 0


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_100_percent_warn(script_runner):
    """Test that the script returns the correct exit code and message on 100%
    delays with warning but no critical defined."""
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '0',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-w', '1', '-t', '5')

    assert not ret.success
    assert ret.stdout == ('WARNING: 100% of the departures at Centralen ' +
                          '(Stockholm) are delayed more than 0 minutes' +
                          '|\'Percentage delayed\'=100%;1;\n')
    assert ret.stderr == ''
    assert ret.returncode == 1


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_100_percent_crit(script_runner):
    """Test that the script returns the correct exit code and message on 100%
    delays with critical but no warning defined."""
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '0',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-c', '1', '-t', '5')

    assert not ret.success
    assert ret.stdout == ('CRITICAL: 100% of the departures at Centralen ' +
                          '(Stockholm) are delayed more than 0 minutes' +
                          '|\'Percentage delayed\'=100%;;1\n')
    assert ret.stderr == ''
    assert ret.returncode == 2


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_wildcard_ok(script_runner):
    """Test that the beginning, the end and the exit code is correct for a general
    query where critical is set to 100."""
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '20',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-c', '100', '-t', '5')

    assert ret.success
    assert ret.stdout.startswith('OK: ')
    assert ret.stdout.endswith(';;100\n')
    assert ret.stderr == ''
    assert ret.returncode == 0


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_wildcard_warn(script_runner):
    """Test that the beginning, the end and the exit code is correct for a general
    query where warn is set to 0."""
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-w', '0', '-t', '5')

    assert not ret.success
    assert ret.stdout.startswith('WARNING: ')
    assert ret.stdout.endswith(';0;\n')
    assert ret.stderr == ''
    assert ret.returncode == 1


@flaky
@pytest.mark.script_launch_mode('subprocess')
def test_wildcard_crit(script_runner):
    """Test that the beginning, the end and the exit code is correct for a general
    query where crit is set to 0."""
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-c', '0', '-t', '5')

    assert not ret.success
    assert ret.stdout.startswith('CRITICAL: ')
    assert ret.stdout.endswith(';;0\n')
    assert ret.stderr == ''
    assert ret.returncode == 2


@pytest.mark.script_launch_mode('subprocess')
def test_timeout(script_runner):
    "Test that the script fails with timeout when timeout is set to 0."
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY, '-p',
                            '10', '-T', 'METRO', '-c', '0', '-t', '0')

    assert not ret.success
    assert ret.stdout.startswith('UNKNOWN: ')
    assert ret.stderr == ''
    assert ret.returncode == 3


@pytest.mark.script_launch_mode('subprocess')
def test_warning_higher_than_critical(script_runner):
    "Test that the script fails when warning is higher than critical."
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-p', '10', '-T', 'METRO', '-c', '10', '-w', '20',
                            '-a', SITE_API_KEY, '-A', DEPARTURE_API_KEY)

    assert not ret.success
    assert ret.stdout == 'ERROR: --warning (20) higher than --critical (10)\n'
    assert ret.stderr == ''
    assert ret.returncode == 4


@pytest.mark.script_launch_mode('subprocess')
def test_long_site_api_key(script_runner):
    "Test that the script fails when the site-api-key is too long."
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-p', '10', '-T', 'METRO', '-w', '10', '-c', '20',
                            '-a', '1234567890123456789012345678901234567890',
                            '-A', DEPARTURE_API_KEY)

    assert not ret.success
    assert ret.stdout.endswith(
        '--site-api-key must be a 32 characters long string.\n')
    assert ret.stderr == ''
    assert ret.returncode == 4


@pytest.mark.script_launch_mode('subprocess')
def test_short_site_api_key(script_runner):
    "Test that the script fails when the site-api-key is too short."
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-p', '10', '-T', 'METRO', '-w', '10', '-c', '20',
                            '-a', '123', '-A', DEPARTURE_API_KEY)

    assert not ret.success
    assert ret.stdout.endswith(
        '--site-api-key must be a 32 characters long string.\n')
    assert ret.stderr == ''
    assert ret.returncode == 4


@pytest.mark.script_launch_mode('subprocess')
def test_long_departure_api_key(script_runner):
    "Test that the script fails when the departure-api-key is too long."
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-p', '10', '-T', 'METRO', '-w', '10', '-c', '20',
                            '-A', '1234567890123456789012345678901234567890',
                            '-a', SITE_API_KEY)

    assert not ret.success
    assert ret.stdout.endswith(
        '--departure-api-key must be a 32 characters long string.\n')
    assert ret.stderr == ''
    assert ret.returncode == 4


@pytest.mark.script_launch_mode('subprocess')
def test_short_departure_api_key(script_runner):
    "Test that the script fails when the departure-api-key is too short."
    ret = script_runner.run('check_sl_delay', '-v', '-i', '1002', '-m', '1',
                            '-p', '10', '-T', 'METRO', '-w', '10', '-c', '20',
                            '-A', '1234567890123456789012345678901234567890',
                            '-a', SITE_API_KEY)

    assert not ret.success
    assert ret.stdout.endswith(
        '--departure-api-key must be a 32 characters long string.\n')
    assert ret.stderr == ''
    assert ret.returncode == 4


@pytest.mark.script_launch_mode('subprocess')
def test_help_options(script_runner):
    "Test that both -h and --help shows the help."
    short_ret = script_runner.run('check_sl_delay', '-h')
    long_ret = script_runner.run('check_sl_delay', '--help')

    assert short_ret.success
    assert long_ret.success
    assert short_ret.stdout.startswith('Usage: check_sl_delay [OPTIONS]\n')
    assert long_ret.stdout.startswith('Usage: check_sl_delay [OPTIONS]\n')
    assert short_ret.stdout.endswith('Show this message and exit.\n')
    assert long_ret.stdout.endswith('Show this message and exit.\n')
    assert short_ret.stderr == ''
    assert long_ret.stderr == ''
    assert short_ret.returncode == 0
    assert long_ret.returncode == 0
