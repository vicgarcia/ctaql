import pytest
import re
import os

from ctaql.bustracker.client import BusTrackerApi, BusTrackerApiError


# configure pytest vcr to store yaml in ./tests/vcr/<module name>/<test name>.yaml

@pytest.fixture(scope='module')
def vcr_cassette_dir(request):
    return os.path.join(os.path.dirname(__file__), 'vcr', request.module.__name__)


# configure pytest vcr to sanitize the api key from the request

@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_query_parameters': [ ('key', 'CTA-API-KEY'), ],
    }


# fixture for bus tracker api class w/ api key from environment

@pytest.fixture
def bustracker():
    return BusTrackerApi(os.getenv('CTA_API_KEY', 'api-key-not-available'))


# test methods of bus tracker api class

TIMESTAMP_TO_MINUTE_REGEX = '^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]$'

TIMESTAMP_TO_SECOND_REGEX = '^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]$'

FULLERTON_BUS_ROUTE = '74'  # fullerton bus is 24 hour, should always return results

FULLERTON_BUS_DIRECTION = 'Eastbound'

FULLERTON_BUS_PATTERN = '8422'  # fullerton bus eastbound pattern

FULLERTON_BUS_STOP = '6597'  # fullerton redline stop eastbound


@pytest.mark.vcr()
def test_get_time(bustracker):

    # make api request
    get_time_response = bustracker.get_time()

    # response contains expected dict structure
    assert 'tm' in get_time_response, \
           "api response contains wrong fields"

    # response contains a timestamp string
    assert re.match(TIMESTAMP_TO_SECOND_REGEX, get_time_response['tm']), \
           "api response timestamp format is not correct"


@pytest.mark.vcr()
def test_get_vehicles(bustracker):

    # fields to verify in api response
    fields = [ 'vid', 'tmstmp', 'lat', 'lon', 'hdg', 'pid', 'rt', 'des', 'pdist', 'dly', 'tablockid', 'tatripid', 'zone' ]

    # make api request using the route as a parameter, default to minute resolution
    by_route_response = bustracker.get_vehicles(rt=FULLERTON_BUS_ROUTE)

    # all elements for the queried route, each containing expected fields, minute resolution
    assert all(v['rt'] == FULLERTON_BUS_ROUTE for v in by_route_response), \
           "api response contains wrong routes"
    assert all(all(f in v for f in fields) for v in by_route_response), \
           "api response contains wrong fields"
    assert all(re.match(TIMESTAMP_TO_MINUTE_REGEX, v['tmstmp']) for v in by_route_response), \
           "api response timestamp format should be to minutes"

    # use the vehicle number from the first result above for the next request
    vehicle_id = by_route_response[0]['vid']

    # make api request using the vehicle id as parameter, specify for second resolution
    by_vehicle_response = bustracker.get_vehicles(vid=vehicle_id, tmres='s')

    # single element, containing expected fields, second resolution
    assert len(by_vehicle_response) == 1, \
           "api response contains extra results"
    assert all(f in by_route_response[0] for f in fields), \
           "api response contains wrong fields"
    assert re.match(TIMESTAMP_TO_SECOND_REGEX, by_vehicle_response[0]['tmstmp']), \
           "api response timestamp format should be to seconds"


@pytest.mark.vcr()
def test_get_routes(bustracker):

    # fields to verify in api response
    fields = [ 'rt', 'rtnm', 'rtclr', 'rtdd' ]

    # make api request
    get_routes_response = bustracker.get_routes()

    # list of elements, containing expected fields
    assert isinstance(get_routes_response, list), \
           "api response is not a list of elements"
    assert all(all(f in r for f in fields) for r in get_routes_response), \
           "api response contains wrong fields"


@pytest.mark.vcr()
def test_get_directions(bustracker):

    # fields to verify in api response
    fields = [ 'dir', ]

    # make api request with route param
    get_directions_response = bustracker.get_directions(rt=FULLERTON_BUS_ROUTE)

    # list of elements, containing expected fields
    assert isinstance(get_directions_response, list), \
           "api response is not a list of elements"
    assert all(all(f in r for f in fields) for r in get_directions_response), \
           "api response contains wrong fields"

    # make api request without params, expect an exception
    with pytest.raises(BusTrackerApiError) as exc:
        bustracker.get_directions()
    assert str(exc.value).startswith('rt parameter missing')


@pytest.mark.vcr()
def test_get_stops(bustracker):

    # fields to verify in api response
    fields = [ 'stpid', 'stpnm', 'lat', 'lon' ]

    # make api request with route and direction params
    get_stops_response = bustracker.get_stops(rt=FULLERTON_BUS_ROUTE, dir=FULLERTON_BUS_DIRECTION)

    # list of elements, containing expected fields
    assert isinstance(get_stops_response, list), \
           "api response is not a list of elements"
    assert all(all(f in r for f in fields) for r in get_stops_response), \
           "api response contains wrong fields"


@pytest.mark.vcr()
def test_get_patterns(bustracker):

    # fields to verify in api response
    pattern_fields = [ 'pid', 'ln', 'rtdir', 'pt' ]
    point_fields = [ 'seq', 'lat', 'lon', 'typ', 'pdist' ]

    # make api request with route param
    get_patterns_response = bustracker.get_patterns(rt=FULLERTON_BUS_ROUTE)

    # list of pattern elements, containing expected fields, one of which is a list of point elements
    assert isinstance(get_patterns_response, list), \
           "api response is not a list of elements"
    for pattern_element in get_patterns_response:
        assert all(f in pattern_element for f in pattern_fields), \
               "api response contains wrong fields"
        assert all(all(f in s for f in point_fields) for s in pattern_element['pt']), \
               "api response contains wrong fields"

    # make api request with pattern id param
    get_pattern_response = bustracker.get_patterns(pid=FULLERTON_BUS_PATTERN)

    # single pattern element, containing expected fields, on of which is a list of point elements
    assert len(get_pattern_response) == 1, \
           "api response contains extra results"
    assert all(f in get_pattern_response[0] for f in pattern_fields), \
           "api response contains wrong fields"
    assert all(all(f in s for f in point_fields) for s in get_pattern_response[0]['pt']), \
           "api response contains wrong fields"


@pytest.mark.vcr()
def test_get_predictions(bustracker):

    # fields to verify in api response
    fields = [ 'tmstmp', 'typ', 'stpnm', 'stpid', 'vid', 'dstp', 'rt', 'rtdd', 'rtdir', 'des', 'prdtm', 'tablockid', 'tatripid', 'dly', 'prdctdn', 'zone' ]

    # make api request with stop id and route params
    get_predictions_by_stop_and_route = bustracker.get_predictions(stpid=FULLERTON_BUS_STOP, rt=FULLERTON_BUS_ROUTE)

    # list of elements, containing expected fields
    assert isinstance(get_predictions_by_stop_and_route, list), \
           "api response is not a list of elements"
    assert all(all(f in r for f in fields) for r in get_predictions_by_stop_and_route), \
           "api response contains wrong fields"

    # use the vehicle number from the first result above for the next request
    vehicle_id = get_predictions_by_stop_and_route[0]['vid']

    # make api request with vehicle id and top params
    get_two_predictions_by_vehicle = bustracker.get_predictions(vid=vehicle_id, top=2)

    # list of elements, containing two predictions, containing expected fields
    assert isinstance(get_predictions_by_stop_and_route, list), \
           "api response is not a list of elements"
    assert len(get_two_predictions_by_vehicle) == 2, \
           "api response contains the wrong number of predictions"
    assert all(all(f in r for f in fields) for r in get_predictions_by_stop_and_route), \
           "api response contains wrong fields"


@pytest.mark.vcr()
def test_get_service_bulletins(bustracker):

    # fields to verify in api response
    fields = [ 'nm', 'sbj', 'dtl', 'brf', 'prty', 'srvc' ]

    # make api request with no params
    get_route_service_bulletins = bustracker.get_service_bulletins(rt=FULLERTON_BUS_ROUTE)

    #  list of elements, , containing expected fields
    assert isinstance(get_route_service_bulletins, list), \
           "api response is not a list of elements"
    assert all(all(f in sb for f in fields) for sb in get_route_service_bulletins), \
           "api response contains wrong fields"
