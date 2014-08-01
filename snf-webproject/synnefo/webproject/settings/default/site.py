# -*- coding: utf-8 -*-
#
# Site-specific Django conf
##################################

from synnefo.lib.settings.setup import Default, Auto
from synnefo.util.entry_points import extend_list_from_entry_point, \
        extend_dict_from_entry_point

LANGUAGE_CODE = Default(
    default_value='en-us',
    description=("Language code for this installation. "
                 "All choices can be found here: "
                 "http://www.i18nguy.com/unicode/language-identifiers.html"),
    category="snf-webproject-site",
)

USE_I18N = Default(
    default_value=True,
    description=("If you set this to False, Django will make some "
                 "optimizations so as not to load the internationalization "
                 "machinery."),
    category="snf-webproject-site",
)

USE_L10N = Default(
    default_value=True,
    description=("If you set this to False, Django will not format dates, "
                 "numbers and calendars according to the current locale."),
    category="snf-webproject-site",
)

MEDIA_ROOT = Default(
    default_value='/usr/share/synnefo/static/',
    example_value="/home/media/media.lawrence.com/",
    description="Absolute path to the directory that holds media.",
    category="snf-webproject-site",
)

MEDIA_URL = Default(
    default_value='/static/',
    example_value="http://example.com/media/",
    description=("URL that handles the media served from MEDIA_ROOT. "
                 "Make sure to use a trailing slash if there is a path "
                 "component (optional in other cases)."),
    category="snf-webproject-site",
)


_STATIC_FILES = {'synnefo.webproject': ''}

def mk_static_files(deps):
    return extend_dict_from_entry_point(
        _STATIC_FILES, 'synnefo', 'web_static')

STATIC_FILES = Auto(
    autoconfigure=mk_static_files,
    description="Static files",
    category="snf-webproject",
    export=False,
)
