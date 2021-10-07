from django.db import models


class ClimateMessage(models.Model):
    code = models.CharField(max_length=120, default="", blank=True, null=True)
    duration = models.CharField(max_length=120, default="", blank=True, null=True)
    avg_value = models.CharField(max_length=120, default="", blank=True, null=True)


    class Meta:
        db_table = 'messages'