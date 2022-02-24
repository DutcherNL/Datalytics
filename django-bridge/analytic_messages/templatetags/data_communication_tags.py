from django import template
from analytic_messages.feedback import data_info, CodeDataCommunication

register = template.Library()

@register.filter
def communicate_title(code):
    return data_info.get_readable(code, CodeDataCommunication.TITLE)

@register.filter
def communicate_short_text(code):
    return data_info.get_readable(code, CodeDataCommunication.SHORT_TEXT)


@register.inclusion_tag("room_state_snippet.html", takes_context=False)
def render_room_state(room):
    return {
        'room': room
    }

@register.inclusion_tag("messages/snippet_message_block.html", takes_context=False)
def render_message(message):
    return {
        'message': message,
        'is_dismissible': not message.is_still_active(),
    }

@register.filter
def get_measurement_danger_class(measurement):
    if measurement.danger_level == 0:
        return ''
    if measurement.danger_level == 1:
        return 'text-warning'
    if measurement.danger_level == 2:
        return 'text-danger'
    return ''