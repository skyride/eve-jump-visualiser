import math

from django.core.management.base import BaseCommand
from django.db.models import Q, Sum, Count, Max

from sde.models import System, SystemJump
from core.models import JumpsRecord
from core.map import render_map


class Command(BaseCommand):
    help = "Generates a map based on aggregates of all data"

    def handle(self, *args, **options):
        jumps = SystemJump.objects.annotate(
            origin_jumps=Sum('origin__jumps__jumps'),
            dest_jumps=Sum('destination__jumps__jumps')
        )

        render_map(jumps, "test.png", scale=3)