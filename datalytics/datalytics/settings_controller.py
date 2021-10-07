import importlib

from datalytics import default_settings
# from datalytics import settings as local_settings

"""
This section initiates certain settings in a more retrievable manner based on the actual settings
"""

local_settings = 'datalytics.settings'
local_settings_lib = importlib.import_module(local_settings)

def get_setting(name):
    if hasattr(local_settings_lib, name):
        return getattr(local_settings_lib, name)
    else:
        return getattr(default_settings, name)



##################
################## ALERT STORAGE
##################

alert_storage = importlib.import_module(get_setting('STORAGE'))
try:
    alert_storage = alert_storage.interface
except AttributeError as e:
    raise KeyError(
        "The defined location for the warning storage interface was not found. Make sure the location initialises your class "
        "object with the variable name 'interface'."
    )