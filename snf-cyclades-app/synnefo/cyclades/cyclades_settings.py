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

from synnefo import settings
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
cyclades_services = settings.CYCLADES_SERVICES
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

CYCLADES_ASTAKOS_AUTH_URL = settings.CYCLADES_ASTAKOS_AUTH_URL
ASTAKOS_ACCOUNT_URL = settings.ASTAKOS_ACCOUNT_URL
ASTAKOS_UI_URL = settings.ASTAKOS_UI_URL

ASTAKOS_BASE_URL = settings.ASTAKOS_BASE_URL
ASTAKOS_BASE_HOST = settings.ASTAKOS_BASE_HOST
ASTAKOS_BASE_PATH = settings.ASTAKOS_BASE_PATH

ASTAKOS_PROXY_PREFIX = settings.CYCLADES_PROXY_PREFIX
ASTAKOS_AUTH_PREFIX = join_urls('/', ASTAKOS_PROXY_PREFIX, 'identity')
ASTAKOS_ACCOUNT_PREFIX = join_urls('/', ASTAKOS_PROXY_PREFIX, 'account')
ASTAKOS_UI_PREFIX = join_urls('/', ASTAKOS_PROXY_PREFIX, 'ui')
ASTAKOS_AUTH_PROXY_PATH = join_urls(BASE_PATH, ASTAKOS_AUTH_PREFIX)
ASTAKOS_ACCOUNT_PROXY_PATH = join_urls(BASE_PATH, ASTAKOS_ACCOUNT_PREFIX)
ASTAKOS_UI_PROXY_PATH = join_urls(BASE_PATH, ASTAKOS_UI_PREFIX)


ASTAKOS_ACCOUNTS_PREFIX = get_service_prefix(synnefo_services,
                                             'astakos_account')
ASTAKOS_VIEWS_PREFIX = get_service_prefix(synnefo_services, 'astakos_ui')

# Proxy Astakos settings

BASE_ASTAKOS_PROXY_PATH = getattr(settings,
                                  'CYCLADES_BASE_ASTAKOS_PROXY_PATH',
                                  ASTAKOS_BASE_PATH)
BASE_ASTAKOS_PROXY_PATH = join_urls(BASE_PATH, BASE_ASTAKOS_PROXY_PATH)
BASE_ASTAKOS_PROXY_PATH = BASE_ASTAKOS_PROXY_PATH.strip('/')

PROXY_USER_SERVICES = settings.CYCLADES_PROXY_USER_SERVICES
