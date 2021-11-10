from django.conf import settings
from django.core.cache import cache
from .client import BusTrackerApi


cta = BusTrackerApi(settings.CTA_BUSTRACKER_API_KEY)


def get_routes():
    key = 'routes'
    routes = cache.get(key)
    if not routes:
        routes = cta.get_routes()
        cache.set(key, routes, 3600)
    return routes


def get_directions_by_route(route):
    key = f'route:{route}:directions'
    directions = cache.get(key)
    if not directions:
        directions = cta.get_directions(rt=route)
        cache.set(key, directions, 3600)
    return directions


def get_vehicles_by_route(route):
    key = f'route:{route}:vehicles'
    vehicles = cache.get(key)
    if not vehicles:
        vehicles = cta.get_vehicles(rt=route)
        cache.set(key, vehicles, 180)
    return vehicles


def get_stops_by_route_and_direction(route, direction):
    key = f'route:{route}:direction:{direction.lower()}:stops'
    stops = cache.get(key)
    if not stops:
        stops = cta.get_stops(rt=route, dir=direction)
        cache.set(key, stops, 3600)
    return stops


def get_predictions_by_vehicle(vehicle):
    key = f'vehicle:{vehicle}:predictions'
    predictions = cache.get(key)
    if not predictions:
        predictions = cta.get_predictions(vid=vehicle)
        cache.set(key, predictions, 90)
    return predictions


def get_predictions_by_stop(stop):
    key = f'stop:{stop}:predictions'
    predictions = cache.get(key)
    if not predictions:
        predictions = cta.get_predictions(stpid=stop)
        cache.set(key, predictions, 90)
    return predictions
