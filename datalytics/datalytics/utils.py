import importlib

from datalytics import default_settings


local_settings = 'datalytics.settings'
local_settings_lib = importlib.import_module(local_settings)


def get_setting(name):
    if hasattr(local_settings_lib, name):
        return getattr(local_settings_lib, name)
    else:
        return getattr(default_settings, name)