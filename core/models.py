from django.db import models

from sde.models import System


class JumpsRecord(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    system = models.ForeignKey(System, related_name="jumps")
    jumps = models.IntegerField(default=0)