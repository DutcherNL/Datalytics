from django.views.generic import ListView, TemplateView
from django.template.loader import get_template, TemplateDoesNotExist

from .models import ClimateMessage
from .feedback import data_info

class MessageTableView(ListView):
    template_name = "message_table.html"
    model = ClimateMessage
    context_object_name = 'messages'


class MessageOverview(ListView):
    template_name = "messages.html"
    model = ClimateMessage
    context_object_name = 'messages'


class MessageInfoView(TemplateView):
    template_name = "display_message.html"
    # template_name_appendix = "message_pages/"

    def setup(self, request, *args, **kwargs):
        super(MessageInfoView, self).setup(request, *args, **kwargs)

        self.message = ClimateMessage.objects.get(id=kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(MessageInfoView, self).get_context_data()
        context['message'] = self.get_message_content(self.message)
        return context

    def get_message_content(self, message):
        try:
            template = get_template(message, using='MessageBackend')
        except TemplateDoesNotExist as e:
            msg = 'message details not found'

            return msg

        return template.render()