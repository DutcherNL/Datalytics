from django import template
from analytic_messages.feedback import data_info, CodeDataCommunication

register = template.Library()

@register.inclusion_tag("room_state_snippet.html", takes_context=False)
def render_room_state(room):
    return {
        'room': room
    }

@register.inclusion_tag("messages/snippet_message_type_collection.html", takes_context=False)
def render_messages_by_type(messages):
    ordered_messages = {}
    for messsage in messages:
        message_list = ordered_messages.get(messsage.code, [])
        message_list.append(messsage)
        ordered_messages[messsage.code] = message_list

    return {
        'ordered_messages': ordered_messages
    }
