import requests
import math
from PIL import Image, ImageDraw

from django.core.management.base import BaseCommand
from django.db.models import Q, Sum, Count, Max

from sde.models import System, SystemJump
from core.models import JumpsRecord
from core.colormap import getVirdis


class Command(BaseCommand):
    help = "Generates a map based on aggregates of all data"

    def handle(self, *args, **options):
        jumps = SystemJump.objects.annotate(
            origin_jumps=Sum('origin__jumps__jumps'),
            dest_jumps=Sum('destination__jumps__jumps')
        ).prefetch_related(
            'origin',
            'destination'
        )

        colour_scale = jumps.aggregate(
            origin=Max('origin_jumps'),
            dest=Max('dest_jumps')
        )
        colour_scale = math.sqrt(256 / max(colour_scale['origin'], colour_scale['dest']))
        virdis = getVirdis()

        # Draw image
        im = Image.new("RGB", (4800, 4096), "#000000")
        draw = ImageDraw.Draw(im)

        for jump in jumps:
            fill = int(
                math.sqrt(
                    max(jump.origin_jumps, jump.dest_jumps) * colour_scale
                )
            )
            draw.line(
                (
                    jump.origin.x * 0.000000000000004 + 2680,
                    (jump.origin.z * -1) * 0.000000000000004 + 2000,
                    jump.destination.x * 0.000000000000004 + 2680,
                    (jump.destination.z * -1) * 0.000000000000004 + 2000
                ),
                fill=virdis[fill],
                width=int(fill / 32)
            )
        del draw

        im.rotate(180)
        im.save("test.png")