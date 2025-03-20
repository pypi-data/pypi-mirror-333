from arrakis.constants import DEFAULT_MATCH
from arrakis.flight import RequestType, create_command
from pyarrow import flight

from .. import constants, schemas


def test_count_flight_info(mock_server):
    cmd = create_command(
        RequestType.Count,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
    )

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.count()


def test_find_flight_info(mock_server):
    cmd = create_command(
        RequestType.Find,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
    )

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.find()


def test_describe_flight_info(mock_server, mock_channels):
    channels = list(mock_channels.keys())
    cmd = create_command(RequestType.Describe, channels=channels)

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.describe()


def test_stream_flight_info(mock_server, mock_channels):
    channels = list(mock_channels.keys())
    cmd = create_command(
        RequestType.Stream,
        channels=channels,
        start=None,
        end=None,
    )

    info = mock_server.make_flight_info(cmd)
    assert info.schema == schemas.stream(list(mock_channels.values()))


def test_get_count(mock_server):
    cmd = create_command(
        RequestType.Count,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
    )
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(endpoint.ticket)


def test_get_find(mock_server):
    cmd = create_command(
        RequestType.Find,
        pattern=DEFAULT_MATCH,
        data_type=[],
        min_rate=0,
        max_rate=16384,
        publisher=[],
    )
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(endpoint.ticket)


def test_get_describe(mock_server, mock_channels):
    channels = list(mock_channels.keys())
    cmd = create_command(RequestType.Describe, channels=channels)
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(endpoint.ticket)


def test_get_stream(mock_server, mock_channels):
    channels = list(mock_channels.keys())
    cmd = create_command(
        RequestType.Stream,
        channels=channels,
        start=1187000000,
        end=1187001000,
    )
    endpoint = flight.FlightEndpoint(cmd, [constants.DEFAULT_LOCATION])

    # FIXME: find out how to parse a RecordBatchStream if possible
    mock_server.process_get_request(endpoint.ticket)
