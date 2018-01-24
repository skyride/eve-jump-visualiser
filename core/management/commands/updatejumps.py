import requests

from django.core.management.base import BaseCommand

from sde.models import System
from core.models import JumpsRecord, Sequence


class Command(BaseCommand):
    help = "Scrapes jump data from the API"

    def handle(self, *args, **options):
        # Get data from API
        results = requests.get("https://esi.tech.ccp.is/v1/universe/system_jumps/?datasource=tranquility")
        results = results.json()

        # Convert to dictionary
        jumps = {}
        for jump in results:
            jumps[jump['system_id']] = jump['ship_jumps']

        sequence = Sequence()

        # Build db objects
        db_jumps = []
        total_jumps = 0
        for system in System.objects.filter(id__lt=31000000).all():
            jump = JumpsRecord(
                sequence=sequence,
                system=system
            )
            if system.id in jumps:
                jump.jumps = jumps[system.id]

            total_jumps = total_jumps + jump.jumps
            db_jumps.append(jump)

        # Bulk create the objects
        JumpsRecord.objects.bulk_create(db_jumps)
        print (
            "Data for %s systems added, %s total jumps" % (
                len(results),
                total_jumps
            )
        )