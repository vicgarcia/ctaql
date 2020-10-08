from django.conf import settings
import requests
import json


BASE_URL = 'http://ctabustracker.com/bustime/api/v2'


class BusTrackerException(Exception):
    pass


def _get(url, params={}):

    # use the api key as a request param for all requests
    params['key'] = settings.CTA_BUSTRACKER_API_KEY

    # force the api to use json instead of default to xml for all requests
    params['format'] = 'json'

    # make the GET request, raise a custom exception if an error occurs
    try:
        response = requests.get(url, params)
    except requests.exceptions.RequestException as e:
        raise BusTrackerException(f'error while making api request : {str(e).lower()}')

    # parse the response json, raise a custom exception for response parsing errors
    try:
        parsed = json.loads(response.text)
        assert 'bustime-response' in parsed, "missing 'bustime-response' root element"
    except (json.JSONDecodeError, AssertionError) as e:
        raise BusTrackerException(f'error while parsing api response : {str(e).lower()}')

    # check the response for an api error, raise a custom exception with the error message
    try:
        error_message = ', '.join([ e['msg'] for e in parsed['bustime-response']['error'] ])
        raise BusTrackerException(f'error response from api : {error_message.lower()}')
    except KeyError:
        pass

    # return the results from the response below the bustime-response root element
    return parsed['bustime-response']


def get_time(self):
    url = f'{BASE_URL}/gettime'
    return _get(url)


def get_vehicles(vid=None, rt=None, tmres=None):
    url = f'{BASE_URL}/getvehicles'
    params = {}
    if vid:
        params['vid'] = vid
    if rt:
        params['rt'] = rt
    if tmres:
        params['tmres'] = tmres
    return _get(url, params)['vehicle']


def get_routes():
    url = f'{BASE_URL}/getroutes'
    return _get(url)['routes']


def get_directions(rt=None):
    url = f'{BASE_URL}/getdirections'
    params = {}
    if rt:
        params['rt'] = rt
    return _get(url, params)['directions']


def get_stops(rt=None, dir=None):
    url = f'{BASE_URL}/getstops'
    params = {}
    if rt:
        params['rt'] = rt
    if dir:
        params['dir'] = dir
    return _get(url, params)['stops']


def get_patterns(rt=None, pid=None):
    url = f'{BASE_URL}/getpatterns'
    params = {}
    if rt:
        params['rt'] = rt
    if pid:
        params['pid'] = pid
    return _get(url, params)['ptr']


def get_predictions(stpid=None, rt=None, vid=None, top=None):
    url = f'{BASE_URL}/getpredictions'
    params = {}
    if stpid:
        params['stpid'] = stpid
    if rt:
        params['rt'] = rt
    if vid:
        params['vid'] = vid
    if top:
        params['top'] = top
    return _get(url, params)['prd']


def get_service_bulletins(rt=None, rtdir=None, stpid=None):
    url = f'{BASE_URL}/getservicebulletins'
    params = {}
    if rt:
        params['rt'] = rt
    if rtdir:
        params['rtdir'] = rtdir
    if stpid:
        params['stpid'] = stpid
    return _get(url, params)['sb']
