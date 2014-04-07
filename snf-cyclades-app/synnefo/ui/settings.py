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
#

import logging
import synnefo.cyclades_settings as cyclades

from django.conf import settings

from synnefo.lib import join_urls
from synnefo.lib.services import get_public_endpoint as endpoint


logger = logging.getLogger(__name__)
synnefo_services = settings.SYNNEFO_SERVICES

BASE_PATH = settings.CYCLADES_BASE_PATH
if not BASE_PATH.startswith("/"):
    BASE_PATH = "/" + BASE_PATH

VOLUME_URL = endpoint(synnefo_services, 'volume', 'v2.0').rstrip('/')
GLANCE_URL = endpoint(synnefo_services, 'image', 'v1.0').rstrip('/')
COMPUTE_URL = endpoint(synnefo_services, 'compute', 'v2.0').rstrip('/')
NETWORK_URL = endpoint(synnefo_services, 'network', 'v2.0').rstrip('/')
USERDATA_URL = endpoint(synnefo_services, 'cyclades_userdata', '').rstrip('/')

ACCOUNT_URL = join_urls('/', cyclades.ASTAKOS_ACCOUNT_PROXY_PATH)

USER_CATALOG_URL = join_urls(ACCOUNT_URL, 'user_catalogs')
FEEDBACK_URL = join_urls(ACCOUNT_URL, 'feedback')

LOGIN_URL = join_urls('/', cyclades.ASTAKOS_UI_PROXY_PATH, 'login')
LOGOUT_REDIRECT = LOGIN_URL
