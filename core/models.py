from django.db import models

from sde.models import System


class Jumps(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    system = models.ForeignKey(System)
    jumps = models.IntegerField(default=0)