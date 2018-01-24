import math
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, Sum, Count, Max, F

from sde.models import System, SystemJump
from core.models import JumpsRecord
from core.map import render_map


class Command(BaseCommand):
    help = "Generates hourly maps"

    def handle(self, *args, **options):
        # Get date range
        jump = SystemJump.objects.first()
        target = jump.origin.jumps.first().date - timedelta(seconds=10)

        run = True
        i = 0
        while run:
            i = i + 1
            jumps = SystemJump.objects.filter(
                origin__jumps__date__range=[
                    target,
                    target + timedelta(minutes=60)
                ]
            ).annotate(
                origin_jumps=Sum('origin__jumps__jumps'),
                dest_jumps=Sum('destination__jumps__jumps')
            )

            if jumps.count() > 0:
                filename = "map-%s.png" % target.strftime('%Y%m%d-%H%M')
                filename = "map%05d.png" % i
                print(
                    "Rendering file %s from %s datapoints..." % (
                        filename,
                        jumps.count()
                    )
                )
                render_map(jumps, filename, scale=3)
                target = target + timedelta(hours=1)
            else:
                print("No datapoints found for target %s" % target)
                target = target + timedelta(hours=1)
