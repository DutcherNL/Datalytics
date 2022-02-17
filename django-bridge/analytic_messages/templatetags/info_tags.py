from django import template
from analytic_messages.feedback import data_info, CodeDataCommunication

register = template.Library()

@register.inclusion_tag("room_state_snippet.html", takes_context=False)
def render_room_state(room):
    return {
        'room': room
    }