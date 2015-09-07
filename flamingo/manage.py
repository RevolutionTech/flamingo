#!/usr/bin/env python
import os
import sys

import cbsettings


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_FACTORY", "flamingo.settings")
    cbsettings.configure('flamingo.settings.switcher')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
