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

import logging

from django.conf import settings
from astakosclient import AstakosClient
from synnefo.lib import join_urls
from synnefo.lib.services import get_service_prefix

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------
# Process Cyclades settings

SERVICE_TOKEN = settings.CYCLADES_SERVICE_TOKEN

BASE_URL = settings.CYCLADES_BASE_URL
BASE_HOST = settings.CYCLADES_BASE_HOST
BASE_PATH = settings.CYCLADES_BASE_PATH

synnefo_services = settings.SYNNEFO_SERVICES
COMPUTE_PREFIX = get_service_prefix(synnefo_services, 'cyclades_compute')
NETWORK_PREFIX = get_service_prefix(synnefo_services, 'cyclades_network')
VMAPI_PREFIX = get_service_prefix(synnefo_services, 'cyclades_vmapi')
PLANKTON_PREFIX = get_service_prefix(synnefo_services, 'cyclades_plankton')
HELPDESK_PREFIX = get_service_prefix(synnefo_services, 'cyclades_helpdesk')
UI_PREFIX = get_service_prefix(synnefo_services, 'cyclades_ui')
USERDATA_PREFIX = get_service_prefix(synnefo_services, 'cyclades_userdata')
ADMIN_PREFIX = get_service_prefix(synnefo_services, 'cyclades_admin')
VOLUME_PREFIX = get_service_prefix(synnefo_services, 'cyclades_volume')

COMPUTE_ROOT_URL = join_urls(BASE_URL, COMPUTE_PREFIX)


# --------------------------------------------------------------------
# Process Astakos settings

ASTAKOS_AUTH_URL = getattr(
    settings, 'ASTAKOS_AUTH_URL',
    'https://accounts.example.synnefo.org/astakos/identity/v2.0')


# --------------------------------------
# Define a LazyAstakosUrl
# This is used to define ASTAKOS_ACCOUNT_URL and
# ASTAKOS_UI_URL and should never be used as is.
class LazyAstakosUrl(object):
    def __init__(self, endpoints_name):
        self.endpoints_name = endpoints_name

    def __str__(self):
        if not hasattr(self, 'str'):
            try:
                astakos_client = \
                    AstakosClient(SERVICE_TOKEN, ASTAKOS_AUTH_URL)
                self.str = getattr(astakos_client, self.endpoints_name)
            except Exception as excpt:
                logger.exception(
                    "Could not retrieve endpoints from Astakos url %s: %s",
                    ASTAKOS_AUTH_URL, excpt)
                return ""
        return self.str

# --------------------------------------
# Define ASTAKOS_UI_URL and ASTAKOS_ACCOUNT_URL as LazyAstakosUrl
# These are used to define the proxy paths.
# These have to be resolved lazily (by the proxy function) so
# they should not be used as is.
ASTAKOS_ACCOUNT_URL = LazyAstakosUrl('account_url')
ASTAKOS_UI_URL = LazyAstakosUrl('ui_url')

ASTAKOS_BASE_URL = settings.ASTAKOS_BASE_URL
ASTAKOS_BASE_HOST = settings.ASTAKOS_BASE_HOST
ASTAKOS_BASE_PATH = settings.ASTAKOS_BASE_PATH

ASTAKOS_ACCOUNTS_PREFIX = get_service_prefix(synnefo_services,
                                             'astakos_account')
ASTAKOS_VIEWS_PREFIX = get_service_prefix(synnefo_services, 'astakos_ui')
ASTAKOS_KEYSTONE_PREFIX = get_service_prefix(synnefo_services,
                                             'astakos_identity')


# Proxy Astakos settings

BASE_ASTAKOS_PROXY_PATH = getattr(settings,
                                  'CYCLADES_BASE_ASTAKOS_PROXY_PATH',
                                  ASTAKOS_BASE_PATH)
BASE_ASTAKOS_PROXY_PATH = join_urls(BASE_PATH, BASE_ASTAKOS_PROXY_PATH)
BASE_ASTAKOS_PROXY_PATH = BASE_ASTAKOS_PROXY_PATH.strip('/')

PROXY_USER_SERVICES = settings.CYCLADES_PROXY_USER_SERVICES
