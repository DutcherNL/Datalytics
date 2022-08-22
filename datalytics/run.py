import sys
import os
import csv
from datetime import datetime

# from datalytics import settings_controller
from datalytics.interface import AnalyserFront

# from datalytics.messaging.models import AlertMessage

analyser = AnalyserFront()


def main(*args):

    if "--mock-build" in args:
        # interface = settings_controller.alert_storage

        analyser.add_room(
            "BASIC", "Living room",
            ["TEMP"]
        )
        room = analyser.get_room("Living room")
        # room.update_sensor('TEMP', 21, None)

    if "--upload-csv" in args:
        try:
            index = args.index("--upload-csv")
            file_location = args[index+1]
            room_id = args[index+2]
        except IndexError:
            print("When running upload csv, please define the path of the csv file followed by the id of the room "
                  "it measures in")

        if room_id == "new":
            # Insert code to add a room
            analyser.add_room(
                "BASIC", "New test room",
                ["TEMP"]
            )

        room = analyser.get_room(room_id=room_id)

        upload_csv(file_path=file_location, room=room)

    if "--add-room" in args:
        try:
            index = args.index("--add-room")
            room_type = args[index+1]
            room_name = args[index+2]
        except IndexError:
            print("When adding a room, please define the room type followed by the room name")

        if analyser.get_room(name=room_name):
            print("There already exists a room with this name. Make sure the name is unique")
        else:
            analyser.add_room(room_type=room_type, name=room_name)
            print(f"{room_name} has been added to the availlable rooms")

    if "--add-measurement" in args:
        try:
            index = args.index("--add-measurement")
            room_id = args[index+1]
            measurement_type = args[index+2]
            value = float(args[index+3])
        except IndexError:
            print("When adding a measurement, please follow with the following data: <room_id> <measurement_type> <value>")

        room = analyser.get_room(room_id=room_id)
        if room:
            room.update_sensor(sensor_type=measurement_type, value=value, timestamp=None)
            print(f"{room.name} has been updated with the new value {value}")
        else:
            print(f"There is no room with the id {room_id}.")

#     interface = settings_controller.alert_storage
#
#     interface.add_message(AlertMessage(
#         code='test',
#         id=1,
#         duration='500',
#         avg_value=26.2,
#     ), fail_silently=True)


def upload_csv(file_path, room):
    if not os.path.exists(file_path):
        print(f"There is no file at the given path: \n {file_path} \n \n Make sure you have the right location."
              f"Also check your navigational dashes, it might differ depending on your opereating system.")
        return

    dt_translate_index = 0
    # opening the CSV file
    with open(file_path, mode ='r') as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)

        # displaying the contents of the CSV file
        for line in csvFile:
            dt, dt_translate_index = translate_dt(line['datetime'], dt_translate_index)
            line.pop('datetime')

            for key, value in line.items():
                value = float(value)
                room.update_sensor(sensor_type=key, value=value, timestamp=dt)



dt_translate_options = [
    '%d/%m/%y %H:%M:%S',
    '%d/%m/%y %H:%M',
    '%d/%m/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M',
]

def translate_dt(dt, index):
    if index >= len(dt_translate_options):
        raise KeyError("The datetime was not defined in any computer readable manner")
    try:
        return datetime.strptime(dt, dt_translate_options[index]), index
    except ValueError:
        return translate_dt(dt, index + 1)


if __name__ == '__main__':
    main(*sys.argv[1:])