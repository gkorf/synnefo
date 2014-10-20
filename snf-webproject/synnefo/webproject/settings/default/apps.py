# -*- coding: utf-8 -*-

from synnefo.lib.settings.setup import Default, Auto
from synnefo.util.entry_points import extend_list_from_entry_point, \
        extend_dict_from_entry_point

# Provide common django settings and extend them from entry_point hooks
_INSTALLED_APPS = (
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.messages',
    'south',
    'synnefo.webproject'
)

def mk_installed_apps(deps):
    return extend_list_from_entry_point(
        _INSTALLED_APPS, 'synnefo', 'web_apps')


INSTALLED_APPS = Auto(
    autoconfigure=mk_installed_apps,
    allow_override=False,
    description="installed apps",
    category="snf-webproject",
    export=False,
)

# Core Django project settings
##################################

SESSION_ENGINE = Default(
    default_value="django.contrib.sessions.backends.cached_db",
    description="Controls where Django stores session data",
    category="snf-webproject",
    export=False,
)

TEMPLATE_LOADERS = Default(
    default_value=(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        ),
    description=("List of callables that know how to import "
                 "templates from various sources."),
    category="snf-webproject",
    export=False,
)

# This is a django project setting, do not change this unless you know
# what you're doing
ROOT_URLCONF = Default(
    default_value='synnefo.webproject.urls',
    description=("This is a django project setting, do not change this "
                 "unless you know what you're doing."),
    category="snf-webproject",
    export=False,
)

TEMPLATE_DIRS = Default(
    default_value=(
        '/etc/synnefo/templates/',
        ),
    description="Additional template dirs.",
    category="snf-webproject",
    export=False,
)

LANGUAGES = Default(
    default_value=(
        ('en', 'English'),
        ),
    description="Languages setting.",
    category="snf-webproject",
    export=False,
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = Default(
    default_value='UTC',
    description=("Local time zone for this installation. "
                 "Warning: The API depends on the TIME_ZONE being UTC."),
    category="snf-webproject",
    export=False,
)
