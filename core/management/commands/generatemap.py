import math
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, Sum, Count, Max

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
        while run:
            print(target)
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
                print(
                    "Rendering file %s from %s datapoints..." % (
                        filename,
                        jumps.count()
                    )
                )
                render_map(jumps, filename, scale=3)
                target = target + timedelta(hours=1)
            else:
                target = target + timedelta(hours=1)