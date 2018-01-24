import math
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.db.models import Q, Sum, Count, Max, F
from django.utils.timezone import make_aware

from sde.models import System, SystemJump
from core.models import JumpsRecord, Sequence
from core.map import render_map


class Command(BaseCommand):
    help = "Generates hourly maps"

    def handle(self, *args, **options):
        # Get date range
        sequences = Sequence.objects.all()


        for i, sequence in enumerate(sequences):
            #filename = "map-%s.png" % target.strftime('%Y%m%d-%H%M')
            filename = "map%05d.png" % i
            print(
                "Rendering file %s from %s datapoints..." % (
                    filename,
                    jumps.count()
                )
            )
            render_map(
                sequence.jumps,
                filename,
                scale=3,
                text=target.strftime('%Y/%m/%d %H:00')
            )
