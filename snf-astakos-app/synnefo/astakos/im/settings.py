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

from synnefo import settings
from synnefo.lib import join_urls
from synnefo.lib.services import get_service_prefix


BASE_URL = settings.ASTAKOS_BASE_URL
BASE_HOST = settings.ASTAKOS_BASE_HOST
BASE_PATH = settings.ASTAKOS_BASE_PATH

synnefo_services = settings.SYNNEFO_SERVICES
astakos_services = settings.SYNNEFO_COMPONENTS['astakos']

ACCOUNTS_PREFIX = get_service_prefix(synnefo_services, 'astakos_account')
VIEWS_PREFIX = get_service_prefix(synnefo_services, 'astakos_ui')
KEYSTONE_PREFIX = get_service_prefix(synnefo_services, 'astakos_identity')
WEBLOGIN_PREFIX = get_service_prefix(synnefo_services, 'astakos_weblogin')
ADMIN_PREFIX = get_service_prefix(synnefo_services, 'astakos_admin')

SERVICE_NAME = settings.BRANDING_SERVICE_NAME

# Set service name
SITENAME = getattr(settings, 'ASTAKOS_SITENAME',
                   SERVICE_NAME)

# These get annotated by snf-webproject
ADMINS = settings.ADMINS
MANAGERS = settings.MANAGERS
HELPDESK = settings.HELPDESK
CONTACT_EMAIL = settings.CONTACT_EMAIL
SERVER_EMAIL = settings.SERVER_EMAIL
SECRET_KEY = settings.SECRET_KEY
SESSION_ENGINE = settings.SESSION_ENGINE

# Set the astakos main functions logging severity (None to disable)
from logging import INFO
LOGGING_LEVEL = getattr(settings, 'ASTAKOS_LOGGING_LEVEL', INFO)

default_activation_redirect_url = join_urls('/', BASE_PATH, VIEWS_PREFIX,
                                            "landing")
ACTIVATION_REDIRECT_URL = getattr(settings, 'ASTAKOS_ACTIVATION_REDIRECT_URL',
                                  default_activation_redirect_url)

# URL to redirect the user after successful login when no next parameter is set
default_success_url = join_urls('/', BASE_PATH, VIEWS_PREFIX, "landing")
LOGIN_SUCCESS_URL = getattr(settings, 'ASTAKOS_LOGIN_SUCCESS_URL',
                            default_success_url)

#
# Local defaults
#

AUTH_TOKEN_DURATION = settings.ASTAKOS_AUTH_TOKEN_DURATION

IM_MODULES = settings.ASTAKOS_IM_MODULES

COOKIE_DOMAIN = settings.ASTAKOS_COOKIE_DOMAIN
COOKIE_NAME = settings.ASTAKOS_COOKIE_NAME
COOKIE_SECURE = settings.ASTAKOS_COOKIE_SECURE

MODERATION_ENABLED = settings.ASTAKOS_MODERATION_ENABLED
RE_USER_EMAIL_PATTERNS = settings.ASTAKOS_RE_USER_EMAIL_PATTERNS

RECAPTCHA_ENABLED = settings.ASTAKOS_RECAPTCHA_ENABLED
RECAPTCHA_PUBLIC_KEY = settings.ASTAKOS_RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = settings.ASTAKOS_RECAPTCHA_PRIVATE_KEY
RECAPTCHA_OPTIONS = settings.ASTAKOS_RECAPTCHA_OPTIONS
RECAPTCHA_USE_SSL = settings.ASTAKOS_RECAPTCHA_USE_SSL

LOGIN_MESSAGES = settings.ASTAKOS_LOGIN_MESSAGES
SIGNUP_MESSAGES = settings.ASTAKOS_SIGNUP_MESSAGES
PROFILE_MESSAGES = settings.ASTAKOS_PROFILE_MESSAGES
GLOBAL_MESSAGES = settings.ASTAKOS_GLOBAL_MESSAGES
PROFILE_EXTRA_LINKS = settings.ASTAKOS_PROFILE_EXTRA_LINKS

EMAILCHANGE_ENABLED = settings.ASTAKOS_EMAILCHANGE_ENABLED
EMAILCHANGE_ACTIVATION_DAYS = settings.ASTAKOS_EMAILCHANGE_ACTIVATION_DAYS
SKIP_EMAIL_VERIFICATION = settings.ASTAKOS_SKIP_EMAIL_VERIFICATION

PAGINATE_BY = settings.ASTAKOS_PAGINATE_BY
PAGINATE_BY_ALL = settings.ASTAKOS_PAGINATE_BY_ALL

PROJECTS_VISIBLE = settings.ASTAKOS_PROJECTS_VISIBLE
PROJECT_ADMINS = settings.ASTAKOS_PROJECT_ADMINS

SHIBBOLETH_REQUIRE_NAME_INFO = settings.ASTAKOS_SHIBBOLETH_REQUIRE_NAME_INFO

# Migrate eppn identifiers to remote id
SHIBBOLETH_MIGRATE_EPPN = getattr(settings, 'ASTAKOS_SHIBBOLETH_MIGRATE_EPPN',
                                  False)

# Migrate eppn identifiers to remote id
SHIBBOLETH_MIGRATE_EPPN = getattr(settings, 'ASTAKOS_SHIBBOLETH_MIGRATE_EPPN',
                                  False)

TWITTER_TOKEN = settings.ASTAKOS_TWITTER_TOKEN
TWITTER_SECRET = settings.ASTAKOS_TWITTER_SECRET
TWITTER_AUTH_FORCE_LOGIN = settings.ASTAKOS_TWITTER_AUTH_FORCE_LOGIN

GOOGLE_CLIENT_ID = settings.ASTAKOS_GOOGLE_CLIENT_ID
GOOGLE_SECRET = settings.ASTAKOS_GOOGLE_SECRET

LINKEDIN_TOKEN = settings.ASTAKOS_LINKEDIN_TOKEN
LINKEDIN_SECRET = settings.ASTAKOS_LINKEDIN_SECRET

COMPONENTS_META = settings.ASTAKOS_COMPONENTS_META
RESOURCES_META = settings.ASTAKOS_RESOURCES_META

API_CLIENT_URL = settings.ASTAKOS_API_CLIENT_URL
KAMAKI_CONFIG_CLOUD_NAME = settings.ASTAKOS_KAMAKI_CONFIG_CLOUD_NAME

RATELIMIT_RETRIES_ALLOWED = settings.ASTAKOS_RATELIMIT_RETRIES_ALLOWED

NEWPASSWD_INVALIDATE_TOKEN = settings.ASTAKOS_NEWPASSWD_INVALIDATE_TOKEN

USAGE_UPDATE_INTERVAL = settings.ASTAKOS_USAGE_UPDATE_INTERVAL

REDIRECT_ALLOWED_SCHEMES = settings.ASTAKOS_REDIRECT_ALLOWED_SCHEMES

LOGOUT_NEXT = settings.ASTAKOS_LOGOUT_NEXT

IM_STATIC_URL = settings.ASTAKOS_IM_STATIC_URL

#
# Obsolete settings, should go away along with the relevant code.
#

INVITATIONS_ENABLED = settings.ASTAKOS_INVITATIONS_ENABLED
DEFAULT_USER_LEVEL = settings.ASTAKOS_DEFAULT_USER_LEVEL
INVITATIONS_PER_LEVEL = settings.ASTAKOS_INVITATIONS_PER_LEVEL

FORCE_PROFILE_UPDATE = settings.ASTAKOS_FORCE_PROFILE_UPDATE

REDIRECT_ALLOWED_SCHEMES = getattr(settings,
                                   'ASTAKOS_REDIRECT_ALLOWED_SCHEMES',
                                   ('pithos', 'pithosdev'))

ADMIN_STATS_PERMITTED_GROUPS = getattr(settings,
                                       'ASTAKOS_ADMIN_STATS_PERMITTED_GROUPS',
                                       ['admin-stats'])

ENDPOINT_CACHE_TIMEOUT = getattr(settings,
                                 'ASTAKOS_ENDPOINT_CACHE_TIMEOUT',
                                 60)

RESOURCE_CACHE_TIMEOUT = getattr(settings,
                                 'ASTAKOS_RESOURCE_CACHE_TIMEOUT',
                                 60)

ADMIN_API_ENABLED = getattr(settings, 'ASTAKOS_ADMIN_API_ENABLED', False)

_default_project_members_limit_choices = (
    ('Unlimited', 'Unlimited'),
    ('5', '5'),
    ('15', '15'),
    ('50', '50'),
    ('100', '100')
)

PROJECT_MEMBERS_LIMIT_CHOICES = getattr(settings,
                                 'ASTAKOS_PROJECT_MEMBERS_LIMIT_CHOICES',
                                 _default_project_members_limit_choices)

ADMIN_API_PERMITTED_GROUPS = getattr(settings,
                                     'ASTAKOS_ADMIN_API_PERMITTED_GROUPS',
                                     ['admin-api'])

TRANSLATE_UUIDS = settings.ASTAKOS_TRANSLATE_UUIDS