"""
Django settings for flamingo project.
:Created: 15 August 2015
:Author: Lucas Connors

"""

import os

from cbsettings import switcher


SETTINGS_DIR = os.path.dirname(__file__)

dev_settings_exists = os.path.isfile(os.path.join(SETTINGS_DIR, 'dev.py'))
prod_settings_exists = os.path.isfile(os.path.join(SETTINGS_DIR, 'prod.py'))

from flamingo.settings.base import BaseSettings
switcher.register(BaseSettings, 'TRAVIS' in os.environ)

if dev_settings_exists:
    from flamingo.settings.dev import DevSettings
    switcher.register(DevSettings, dev_settings_exists and not prod_settings_exists)

if prod_settings_exists:
    from flamingo.settings.prod import ProdSettings
    switcher.register(ProdSettings, prod_settings_exists)
