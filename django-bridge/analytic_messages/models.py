from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone


class ClimateMessage(models.Model):
    code = models.CharField(max_length=120, default="", blank=True, null=True)
    dt_start = models.DateTimeField(null=True)
    dt_last_update = models.DateTimeField(null=True)
    duration = models.CharField(max_length=120, default="", blank=True, null=True)
    avg_value = models.CharField(max_length=120, default="", blank=True, null=True)


    class Meta:
        db_table = 'messages'
        ordering = ['-dt_start']

    def is_still_active(self):
        recent_delta = timedelta(hours=3)

        return self.dt_last_update + recent_delta >= timezone.now()