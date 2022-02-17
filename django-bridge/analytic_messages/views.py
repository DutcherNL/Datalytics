from datetime import timedelta

from django.views.generic import ListView, TemplateView
from django.template.loader import get_template, TemplateDoesNotExist
from django.utils import timezone

from .models import ClimateMessage, Room
from .feedback import data_info

class MessageTableView(ListView):
    template_name = "message_table.html"
    model = ClimateMessage
    context_object_name = 'messages'


class MessageOverview(ListView):
    template_name = "messages.html"
    model = ClimateMessage
    context_object_name = 'messages'

    def get_queryset(self):
        return super(MessageOverview, self).get_queryset().exclude(code="test")

    def get_context_data(self, *args, object_list=None, **kwargs):
        threshold = timezone.now() - timedelta(days=14)
        context = super(MessageOverview, self).get_context_data(*args, object_list=object_list, **kwargs)
        context.update({
            'old_messages': context[self.context_object_name].filter(dt_last_update__lte=threshold),
            'new_messages': context[self.context_object_name].filter(dt_last_update__gt=threshold),
        })
        context['rooms'] = Room.objects.all()

        context['rooms_old'] = [
            {
                'name': 'living_room',
                'messages': context[self.context_object_name]
            },
            {
                'name':  'bathroom',
                'messages': [],
            },
        ]

        return context


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