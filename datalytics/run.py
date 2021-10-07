from datalytics import settings_controller

from datalytics.messaging.models import AlertMessage


def main():
    interface = settings_controller.alert_storage

    interface.add_message(AlertMessage(
        code='test',
        id=1,
        duration='500',
        avg_value=26.2,
    ), fail_silently=True)

    interface.add_message(AlertMessage(
        code='test',
        id=2,
        duration='500',
        avg_value=26.2,
    ), fail_silently=True)

    interface.update_message(AlertMessage(
        code='test',
        id=2,
        duration='750',
        avg_value=26.2,
    ))


if __name__ == '__main__':
    main()