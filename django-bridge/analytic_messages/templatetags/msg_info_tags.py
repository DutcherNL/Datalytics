from datetime import timedelta
from django import template

register = template.Library()

@register.filter
def readable_dt(dt):
    result = ""
    if dt.days > 0:
        result += f"{dt.days} dagen "

    if dt.hours > 0:
        result += f"{dt.hours} uur "

    if dt.minutes > 0:
        if len(result) > 0:
            result += "en "

        result += f"{dt.minutes} minuten"

    return result