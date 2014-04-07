# Copyright 2013-2014 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.

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

ASTAKOS_AUTH_URL = settings.ASTAKOS_AUTH_URL
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
