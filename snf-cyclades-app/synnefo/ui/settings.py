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
