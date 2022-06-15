from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone



class Room(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'rooms'

    def __str__(self):
        return f'{self.name}'


class MeasurementTypes:

    class Temp:
        code = 'TEMP'
        name = 'Temperature'
        unit = '°C'
        decimals = 1

    class Humidity:
        code = 'HMD'
        name = 'Humidity'
        unit = '%'
        decimals = 0

    class CO2:
        code = 'CO2'
        name = 'CO2 concentration'
        unit = 'ppm CO2'
        decimals = 0

    types = [Temp, Humidity, CO2]

    @classmethod
    def get_types(cls):
        return [(data_type.code, data_type.name) for data_type in cls.types]

    @classmethod
    def get_data_type(cls, measuremnt_type):
        for data_type in cls.types:
            if measuremnt_type == data_type.code:
                return data_type
        return None


class Measurement(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=8)
    dt_last_update = models.DateTimeField(null=True)
    type = models.CharField(max_length=4, choices=MeasurementTypes.get_types())
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    danger_level = models.IntegerField(choices=[
        (0, 'safe'),
        (1, 'warning'),
        (2, 'danger'),
    ])

    class Meta:
        db_table = 'room_measurement'

    def get_unit(self):
        return MeasurementTypes.get_data_type(self.type).unit

    def __str__(self):
        value = round(self.value, MeasurementTypes.get_data_type(self.type).decimals)
        return f'{value}{self.get_unit()}'


class MessageManager(models.Manager):
    active_time_delta = timedelta(days=1)

    def filter_active(self):
        threshold_time = timezone.now() - self.active_time_delta
        print(threshold_time)
        a = self.filter(dt_last_update__lt=threshold_time)
        print(a)
        return a

    def filter_inactive(self):
        threshold_time = timezone.now() - self.active_time_delta
        return self.filter(dt_last_update__gt=threshold_time)


class ClimateMessage(models.Model):
    code = models.CharField(max_length=120, default="", blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages', null=True)
    dt_start = models.DateTimeField(null=True)
    dt_last_update = models.DateTimeField(null=True)
    duration = models.CharField(max_length=120, default="", blank=True, null=True)
    avg_value = models.CharField(max_length=120, default="", blank=True, null=True)

    objects = MessageManager()

    class Meta:
        db_table = 'messages'
        ordering = ['-dt_start']

    def is_still_active(self):
        recent_delta = timedelta(hours=3)

        return self.dt_last_update + recent_delta >= timezone.now()


class MessageViewing(models.Model):
    message = models.OneToOneField(ClimateMessage, on_delete=models.CASCADE, related_name='viewing')
    is_viewed = models.BooleanField(default=False)

    class Meta:
        db_table = 'message_viewings'