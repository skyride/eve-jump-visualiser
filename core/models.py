from django.db import models

from sde.models import System


class Sequence(models.Model):
    date = models.DateTimeField(db_index=True)

    def __str__(self):
        return "id=%s date=%s" % (
            self.id,
            self.date.strftime('%Y/%m/%d %H:%M')
        )


class JumpsRecord(models.Model):
    sequence = models.ForeignKey(Sequence, related_name="records", null=True, default=None)
    system = models.ForeignKey(System, related_name="jumps")
    jumps = models.IntegerField(default=0)