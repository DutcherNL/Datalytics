# Datalytics visual representation

This folder contains the code for visually representing the alerts generated with datalytics.

## Getting started with development

1. Install the latest version of Python 3. If you are on Windows, you can download Python from [python.org].
If you are not, check if you already have a recent version by running `python3 --version`. As of writing,
Python 3.7 or higher is recent enough, but this may change in the future.
1. Create a new virtual environment. On Windows, this can be done by running `py -3 -m venv venv`. On other operating systems this is done by running `python3 -m venv venv`. This ensures that this project's dependencies don't conflict with other Python applications on your system.
1. Activate your virtual environment by running `venv\Scripts\activate` if you are on Windows. Otherwise run `source venv/bin/activate`. If this is successful, your terminal line will start with `(venv)`. We assume that any commands ran beyond this point are ran inside a virtualenv for this project. This step needs to be done for each terminal you are using for this project, so if you later return to continue working on the program, you need to rerun this command.
1. Install the dependencies: `pip install -r requirements.txt`. These dependencies include common dependencies (such as _Django_) 
1. Setup the database by running `python manage.py migrate`. This ensures your database can store the items we expect to store in it.
1. Start the server: `python manage.py runserver`. This starts a web server, which you can access using your webbrowser and going to `localhost:8000`.

## Testing

To run the tests, use `python manage.py test`