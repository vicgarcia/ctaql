import time
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from bustracker.client import BusTrackerApi
from bustracker.models import Route, Pattern, Stop


class Command(BaseCommand):
    help = 'Sync data to local database from CTA Bustracker API'

    def handle(self, *args, **options):
        api = BusTrackerApi(settings.CTA_BUSTRACKER_API_KEY)

        # deleting all routes cascades to patterns and stops
        Route.objects.all().delete()

        # iterate over routes from the API
        for r in api.get_routes():
            route = Route.objects.create(
                number=r['rt'],
                name=r['rtnm'],
            )

            # iterate over patterns for the route from the API
            try:
                for p in api.get_patterns(rt=r['rt']):
                    pattern = Pattern.objects.create(
                        route=route,
                        number=p['pid'],
                        direction=p['rtdir'],
                    )

                    # iterate over stops in the pattern in the response
                    for s in p['pt']:
                        if s['typ'] == 'S':
                            stop = Stop.objects.create(
                                pattern=pattern,
                                number=s['stpid'],
                                sequence=s['seq'],
                                name=s['stpnm'],
                                latitude=s['lat'],
                                longitude=s['lon'],
                            )
            except Exception as e:
                pass

        self.stdout.write('data import complete')
