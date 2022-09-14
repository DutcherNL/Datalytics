import importlib
import os

from datalytics import default_settings
# from datalytics import settings as local_settings

"""
This section initiates certain settings in a more retrievable manner based on the actual settings
"""


local_settings = os.environ.get('DATALYTICS_SETTINGS', 'datalytics.settings')
local_settings_lib = importlib.import_module(local_settings)

def get_setting(name):
    if hasattr(local_settings_lib, name):
        return getattr(local_settings_lib, name)
    else:
        return getattr(default_settings, name)



##################
################## ALERT STORAGE
##################

# alert_storage = importlib.import_module(get_setting('STORAGE'))
# try:
#     alert_storage = alert_storage.interface
# except AttributeError as e:
#     raise KeyError(
#         "The defined location for the warning storage interface was not found. Make sure the location initialises your class "
#         "object with the variable name 'interface'."
#     )


class Settings:

    def __init__(self):
        self._lib = {}
        self._loaded_lib = {}

    def __getattr__(self, item: str):
        """ Returns attribute from the settings. """
        if item in self._lib.keys():
            return self._lib[item]
        else:
            self._lib[item] = get_setting(item.upper())
            return self._lib[item]

    def load(self, item: str):
        """ Load the library of a certain element """
        if item in self._loaded_lib.keys():
            return self._loaded_lib[item]
        else:
            self._loaded_lib[item] = importlib.import_module(getattr(self, item))
            return self._loaded_lib[item]




settings = Settings()