from django import template
from analytic_messages.feedback import data_info, CodeDataCommunication

register = template.Library()

@register.filter
def communicate_title(code):
    return data_info.get_readable(code, CodeDataCommunication.TITLE)

@register.filter
def communicate_short_text(code):
    return data_info.get_readable(code, CodeDataCommunication.SHORT_TEXT)