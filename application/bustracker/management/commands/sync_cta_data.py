import time
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import bustracker.client as cta
from bustracker.models import Route, Pattern, Stop


class Command(BaseCommand):
    help = 'Sync data to local database from CTA Bustracker API'

    def handle(self, *args, **options):

        # deleting all routes cascades to patterns and stops
        Route.objects.all().delete()

        # iterate over routes from the API
        for r in cta.get_routes():
            route = Route.objects.create(
                number=r['rt'],
                name=r['rtnm'],
            )

            # error handling for routes w/o patterns (skip to next route)
            try:

                # iterate over patterns for the route from the API
                for p in cta.get_patterns(rt=r['rt']):
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

            except cta.BusTrackerException:
                pass

        self.stdout.write('data import complete')
