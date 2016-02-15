"""
Django settings for flamingo project.
:Created: 15 August 2015
:Author: Lucas Connors

"""

import os

from cbsettings import switcher

from flamingo.settings.base import BaseSettings
from flamingo.settings.prod import ProdSettings


flamingo_env = os.environ.get('FLAMINGO_ENV', 'DEV')
switcher.register(BaseSettings, flamingo_env == 'DEV')
switcher.register(ProdSettings, flamingo_env == 'PROD')
