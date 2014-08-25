# Copyright (C) 2010-2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from synnefo.lib.settings.setup import Default, Mandatory
from synnefo.util.entry_points import extend_list_from_entry_point, \
        extend_dict_from_entry_point


DEBUG = Default(
    default_value=False,
    description="Enable Global Synnefo debug mode.",
    export=False,
    category="snf-webproject-deploy",
)

TEST = Default(
    default_value=False,
    description="Enable Global Synnefo test mode.",
    export=False,
    category="snf-webproject-deploy",
)

# Deployment settings
##################################

TEMPLATE_DEBUG = Default(
    default_value=False,
    description="Enable template debug mode.",
    export=False,
    category="snf-webproject-deploy",
)

SESSION_COOKIE_SECURE = Default(
    default_value=True,
    description=("Use secure cookie for django sessions cookie, "
                 "change this if you don't plan to deploy applications "
                 "using https"),
    category="snf-webproject-deploy",
)

# You should always change this setting.
# Make this unique, and don't share it with anybody.
SECRET_KEY = Mandatory(
    example_value='_a_secret_random_key_',
    description=("A secret key for a particular Django installation. "
                 "Make this unique, and don't share it with anybody."),
    category="snf-webproject-deploy",
)

USE_X_FORWARDED_HOST = Default(
    default_value=True,
    description=("A boolean that specifies whether to use the "
                 "X-Forwarded-Host header in preference to the Host header. "
                 "This should only be enabled if a proxy which sets "
                 "this header is in use."),
    category="snf-webproject-deploy",
)

DEFAULT_EXCEPTION_REPORTER_FILTER = Default(
    default_value=\
        "synnefo.webproject.exception_filter.SynnefoExceptionReporterFilter",
    description="Custom exception filter to 'cleanse' setting variables",
    category="snf-webproject-deploy",
    export=False,
)

HIDDEN_SETTINGS = Default(
    default_value='SECRET|PASSWORD|PROFANITIES_LIST|SIGNATURE|AMQP_HOSTS|'\
        'PRIVATE_KEY|DB_CONNECTION|TOKEN',
    description="Settings that should be 'cleansed'.",
    category="snf-webproject-deploy",
    export=False,
)

HIDDEN_COOKIES = Default(
    default_value=['password', '_pithos2_a', 'token', 'sessionid', 'shibstate',
                   'shibsession', 'CSRF_COOKIE'],
    description="Cookies that should be 'cleansed'.",
    category="snf-webproject-deploy",
    export=False,
)

HIDDEN_HEADERS = Default(
    default_value=['HTTP_X_AUTH_TOKEN', 'HTTP_COOKIE'],
    description="Headers that should be 'cleansed'.",
    category="snf-webproject-deploy",
    export=False,
)

MAIL_MAX_LEN = Default(
    default_value=100 * 1024,  # (100KB)
    description="Mail size limit for unhandled exception",
    category="snf-webproject-deploy",
    export=False,
)

APPEND_SLASH = Default(
    default_value=False,
    description=(
        "When set to True, if the request URL does not match any of the "
        "patterns in the URLconf and it doesn't end in a slash, an HTTP "
        "redirect is issued to the same URL with a slash appended. Note that "
        "the redirect may cause any data submitted in a POST request to be "
        "lost. Due to the REST nature of most of the registered Synnefo "
        "endpoints we prefer to disable this behaviour by default."),
    category="snf-webproject-deploy",
    export=False,
)

_TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media'
)

TEMPLATE_CONTEXT_PROCESSORS = Default(
    default_value=extend_list_from_entry_point(
        _TEMPLATE_CONTEXT_PROCESSORS, 'synnefo', 'web_context_processors'),
    description="Template context processors.",
    category="snf-webproject",
    export=False,
)

_MIDDLEWARE_CLASSES = (
    #'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'synnefo.webproject.middleware.LoggingConfigMiddleware',
)

MIDDLEWARE_CLASSES = Default(
    default_value=extend_list_from_entry_point(
        _MIDDLEWARE_CLASSES, 'synnefo', 'web_middleware'),
    description="Middleware classes",
    category="snf-webproject",
    export=False,
)
