from datetime import datetime, timedelta


class AlertMessage:
    code = None
    id = None
    room_id = None
    dt_start = None
    dt_last_update = None
    avg_value = None
    is_active = True

    def __init__(self, code, room, dt_start, dt_last_update, avg_value, id=None):
        self.code = code
        self.room = room
        self.dt_start: datetime = dt_start
        self.dt_last_update: datetime = dt_last_update
        self.avg_value = avg_value
        self.id = id

    def update_avg(self, value, timestamp):
        """ Update the average value, correctly scaled over the time """
        # Make sure there is actual time difference in the old version to prevent devide by 0
        # Otherwise just handle two datapoints
        if self.dt_last_update == self.dt_start:
            self.avg_value = (value + self.avg_value) / 2
            self.dt_last_update = timestamp
        else:
            """
            t_old   elapsed seconds up to now
            t_new   elapased seconds since last update
            avg     old average value
            v       new value added
            
            new average value = (t_old * avg + v * t_new) / (t_old + t_new)
            new average value = (avg + v * t_new / t_old) / (1 + t_new / t_old)
            """
            t_old = self.dt_last_update - self.dt_start
            t_new:timedelta = timestamp - self.dt_last_update
            t_factor = t_new / t_old

            self.avg_value = (self.avg_value + value * t_factor) / (1 + t_factor)
            self.dt_last_update = timestamp


