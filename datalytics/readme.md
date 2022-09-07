# Datalytics

This folder contains all the code for datalytics

## Getting started with development

1. Install the latest version of Python 3. If you are on Windows, you can download Python from [python.org].
If you are not, check if you already have a recent version by running `python3 --version`. As of writing,
Python 3.7 or higher is recent enough, but this may change in the future.
1. Create a new virtual environment. On Windows, this can be done by running `py -3 -m venv venv`. On other operating systems this is done by running `python3 -m venv venv`. This ensures that this project's dependencies don't conflict with other Python applications on your system.
1. Activate your virtual environment by running `venv\Scripts\activate` if you are on Windows. Otherwise run `source venv/bin/activate`. If this is successful, your terminal line will start with `(venv)`. We assume that any commands ran beyond this point are ran inside a virtualenv for this project. This step needs to be done for each terminal you are using for this project, so if you later return to continue working on the program, you need to rerun this command.
1. Install the dependencies: `pip install -r requirements.txt`. These dependencies include common dependencies (such as _Django_) 

## Using the software

The software in the current format automatically ends when completed running. When including in continuously running,
simply initiate an instance of the datalytics.interface.AnalyserFront class. Otherwise run `python run.py` followed by
any of the parameters defined below

### `--mock-build`
Adds a basic room with the name 'living room' as well as temperature sensor with latest value of 21°C
Used to populate an empty database

### `--add-room <room_type> <room_name>`
Adds a room of the given type with the given name

### `--add-measurement <room_id> <measurement_type> <value>`
Adds a measurement for a given sensor with the given room_id (or room name), type of measurement and the value of the 
measurement

### `--upload-csv <file_path> <room_id>`
Uploads an entire csv file at the given file path location as if it was data for the room with the given room id (or name)
Add `-force` to force updates of analysis even though the measurement is older than the latest known measurement. Warning:
this may result in unintended behaviour.

## `--test`

Runs the defined testcases