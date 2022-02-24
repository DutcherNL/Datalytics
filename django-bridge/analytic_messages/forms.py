from django.forms import Form, ValidationError

from analytic_messages.models import ClimateMessage, MessageViewing



class MessageDismissForm(Form):

    def __init__(self, *args, message=None, **kwargs):
        self.message = message
        super(MessageDismissForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.message is None:
            raise ValidationError("Message is missing")

        try:
            if self.message.viewing.is_viewed:
                raise ValidationError("Message is already marked as read")
        except MessageViewing.DoesNotExist:
            pass

        return self.cleaned_data

    def save(self):
        try:
            viewer = self.message.viewing
        except MessageViewing.DoesNotExist:
            viewer = MessageViewing.objects.create(
                message = self.message
            )

        viewer.is_viewed = True
        viewer.save()