# Copyright 2013 GRNET S.A. All rights reserved.
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

from django.conf import settings
from synnefo.lib import join_urls
from synnefo.lib.services import get_service_prefix

# Process Cyclades settings

BASE_URL = settings.CYCLADES_BASE_URL
BASE_HOST = settings.CYCLADES_BASE_HOST
BASE_PATH = settings.CYCLADES_BASE_PATH

synnefo_services = settings.SYNNEFO_SERVICES
COMPUTE_PREFIX = get_service_prefix(synnefo_services, 'cyclades_compute')
VMAPI_PREFIX = get_service_prefix(synnefo_services, 'cyclades_vmapi')
PLANKTON_PREFIX = get_service_prefix(synnefo_services, 'cyclades_plankton')
HELPDESK_PREFIX = get_service_prefix(synnefo_services, 'cyclades_helpdesk')
UI_PREFIX = get_service_prefix(synnefo_services, 'cyclades_ui')
USERDATA_PREFIX = get_service_prefix(synnefo_services, 'cyclades_userdata')
ADMIN_PREFIX = get_service_prefix(synnefo_services, 'cyclades_admin')

COMPUTE_ROOT_URL = join_urls(BASE_URL, COMPUTE_PREFIX)


# Process Astakos settings

ASTAKOS_BASE_URL = settings.ASTAKOS_BASE_URL
ASTAKOS_BASE_HOST = settings.ASTAKOS_BASE_HOST
ASTAKOS_BASE_PATH = settings.ASTAKOS_BASE_PATH

ASTAKOS_ACCOUNTS_PREFIX = get_service_prefix(synnefo_services, 'astakos_account')
ASTAKOS_VIEWS_PREFIX = get_service_prefix(synnefo_services, 'astakos_ui')
ASTAKOS_KEYSTONE_PREFIX = get_service_prefix(synnefo_services, 'astakos_identity')


# Proxy Astakos settings

BASE_ASTAKOS_PROXY_PATH = getattr(settings,
                                  'CYCLADES_BASE_ASTAKOS_PROXY_PATH',
                                  ASTAKOS_BASE_PATH)
BASE_ASTAKOS_PROXY_PATH = join_urls(BASE_PATH, BASE_ASTAKOS_PROXY_PATH)
BASE_ASTAKOS_PROXY_PATH = BASE_ASTAKOS_PROXY_PATH.strip('/')

PROXY_USER_SERVICES = settings.CYCLADES_PROXY_USER_SERVICES
