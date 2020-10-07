import requests
import json


class BusTrackerException(Exception):
    pass


class BusTrackerApi(object):
    base_url = 'http://ctabustracker.com/bustime/api/v2'

    def __init__(self, api_key):
        self.api_key = api_key

    def _get(self, url, params={}):

        # use the api key as a request param for all requests
        params['key'] = self.api_key

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
        url = f'{self.base_url}/gettime'
        return self._get(url)


    def get_vehicles(self, vid=None, rt=None, tmres=None):
        url = f'{self.base_url}/getvehicles'
        params = {}
        if vid:
            params['vid'] = vid
        if rt:
            params['rt'] = rt
        if tmres:
            params['tmres'] = tmres
        return self._get(url, params)['vehicle']


    def get_routes(self):
        url = f'{self.base_url}/getroutes'
        return self._get(url)['routes']


    def get_directions(self, rt=None):
        url = f'{self.base_url}/getdirections'
        params = {}
        if rt:
            params['rt'] = rt
        return self._get(url, params)['directions']


    def get_stops(self, rt=None, dir=None):
        url = f'{self.base_url}/getstops'
        params = {}
        if rt:
            params['rt'] = rt
        if dir:
            params['dir'] = dir
        return self._get(url, params)['stops']


    def get_patterns(self, rt=None, pid=None):
        url = f'{self.base_url}/getpatterns'
        params = {}
        if rt:
            params['rt'] = rt
        if pid:
            params['pid'] = pid
        return self._get(url, params)['ptr']


    def get_predictions(self, stpid=None, rt=None, vid=None, top=None):
        url = f'{self.base_url}/getpredictions'
        params = {}
        if stpid:
            params['stpid'] = stpid
        if rt:
            params['rt'] = rt
        if vid:
            params['vid'] = vid
        if top:
            params['top'] = top
        return self._get(url, params)['prd']


    def get_service_bulletins(self, rt=None, rtdir=None, stpid=None):
        url = f'{self.base_url}/getservicebulletins'
        params = {}
        if rt:
            params['rt'] = rt
        if rtdir:
            params['rtdir'] = rtdir
        if stpid:
            params['stpid'] = stpid
        return self._get(url, params)['sb']