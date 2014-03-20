# Copyright 2012-2014 GRNET S.A. All rights reserved.
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

#coding=utf8
import logging

from settings import settings
from synnefo.lib import join_urls
from synnefo.lib.services import get_service_prefix
from astakosclient import AstakosClient

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------
# Process Pithos settings

# Service Token acquired by identity provider.
SERVICE_TOKEN = getattr(settings, 'PITHOS_SERVICE_TOKEN', '')

BASE_URL = settings.PITHOS_BASE_URL
BASE_HOST = settings.PITHOS_BASE_HOST
BASE_PATH = settings.PITHOS_BASE_PATH

ASTAKOS_BASE_URL = settings.ASTAKOS_BASE_URL
ASTAKOS_BASE_HOST = settings.ASTAKOS_BASE_HOST,
ASTAKOS_BASE_PATH = settings.ASTAKOS_BASE_PATH

synnefo_services = settings.SYNNEFO_SERVICES

PITHOS_PREFIX = get_service_prefix(synnefo_services, 'pithos_object-store')
PUBLIC_PREFIX = get_service_prefix(synnefo_services, 'pithos_public')
UI_PREFIX = get_service_prefix(synnefo_services, 'pithos_ui')
VIEW_PREFIX = get_service_prefix(synnefo_services, 'pithos_view')

ASTAKOS_ACCOUNTS_PREFIX = get_service_prefix(synnefo_services,
                                             'astakos_account')
ASTAKOS_VIEWS_PREFIX = get_service_prefix(synnefo_services, 'astakos_ui')


# --------------------------------------------------------------------
# Process Astakos settings

ASTAKOS_AUTH_URL = getattr(
    settings, 'ASTAKOS_AUTH_URL',
    'https://accounts.example.synnefo.org/astakos/identity/v2.0')

ASTAKOSCLIENT_POOLSIZE = \
    getattr(settings, 'PITHOS_ASTAKOSCLIENT_POOLSIZE', 200)


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
# Define ASTAKOS_ACCOUNT_URL and ASTAKOS_UR_URL as LazyAstakosUrl
# These are used to define the proxy paths.
# These have to be resolved lazily (by the proxy function) so
# they should not be used as is.
ASTAKOS_ACCOUNT_URL = LazyAstakosUrl('account_url')
ASTAKOS_UI_URL = LazyAstakosUrl('ui_url')

# --------------------------------------
# Define Astakos prefixes
ASTAKOS_PROXY_PREFIX = getattr(settings, 'PITHOS_PROXY_PREFIX', '_astakos')
ASTAKOS_AUTH_PREFIX = join_urls('/', ASTAKOS_PROXY_PREFIX, 'identity')
ASTAKOS_ACCOUNT_PREFIX = join_urls('/', ASTAKOS_PROXY_PREFIX, 'account')
ASTAKOS_UI_PREFIX = join_urls('/', ASTAKOS_PROXY_PREFIX, 'ui')

# --------------------------------------
# Define Astakos proxy paths
ASTAKOS_AUTH_PROXY_PATH = join_urls(BASE_PATH, ASTAKOS_AUTH_PREFIX)
ASTAKOS_ACCOUNT_PROXY_PATH = join_urls(BASE_PATH, ASTAKOS_ACCOUNT_PREFIX)
ASTAKOS_UI_PROXY_PATH = join_urls(BASE_PATH, ASTAKOS_UI_PREFIX)

# Astakos login URL to redirect if the user information is missing
LOGIN_URL = join_urls(ASTAKOS_UI_PROXY_PATH, 'login')

ASTAKOS_KEYSTONE_PREFIX = get_service_prefix(synnefo_services, 'astakos_identity')

BASE_ASTAKOS_PROXY_PATH = getattr(settings, 'PITHOS_BASE_ASTAKOS_PROXY_PATH',
                                  ASTAKOS_BASE_PATH)
BASE_ASTAKOS_PROXY_PATH = join_urls(BASE_PATH, BASE_ASTAKOS_PROXY_PATH)
BASE_ASTAKOS_PROXY_PATH = BASE_ASTAKOS_PROXY_PATH.strip('/')


SERVICE_TOKEN = settings.PITHOS_SERVICE_TOKEN

COOKIE_NAME = settings.PITHOS_ASTAKOS_COOKIE_NAME

ASTAKOSCLIENT_POOLSIZE = settings.PITHOS_ASTAKOSCLIENT_POOLSIZE
BACKEND_POOL_ENABLED = settings.PITHOS_BACKEND_POOL_ENABLED
BACKEND_POOL_SIZE = settings.PITHOS_BACKEND_POOL_SIZE

BACKEND_DB_MODULE = settings.PITHOS_BACKEND_DB_MODULE
BACKEND_BLOCK_MODULE = settings.PITHOS_BACKEND_BLOCK_MODULE

BACKEND_DB_CONNECTION = settings.PITHOS_BACKEND_DB_CONNECTION
BACKEND_BLOCK_PATH = settings.PITHOS_BACKEND_BLOCK_PATH
BACKEND_BLOCK_SIZE = settings.PITHOS_BACKEND_BLOCK_SIZE
BACKEND_HASH_ALGORITHM = settings.PITHOS_BACKEND_HASH_ALGORITHM

UPDATE_MD5 = settings.PITHOS_UPDATE_MD5

BACKEND_VERSIONING = settings.PITHOS_BACKEND_VERSIONING
BACKEND_FREE_VERSIONING = settings.PITHOS_BACKEND_FREE_VERSIONING

RADOS_STORAGE = settings.PITHOS_RADOS_STORAGE
RADOS_POOL_BLOCKS = settings.PITHOS_RADOS_POOL_BLOCKS
RADOS_POOL_MAPS = settings.PITHOS_RADOS_POOL_MAPS

PROXY_USER_SERVICES = settings.PITHOS_PROXY_USER_SERVICES

PUBLIC_URL_SECURITY = settings.PITHOS_PUBLIC_URL_SECURITY
PUBLIC_URL_ALPHABET = settings.PITHOS_PUBLIC_URL_ALPHABET

API_LIST_LIMIT = settings.PITHOS_API_LIST_LIMIT

#
# Obsolete settings, these should go away along with the relevant code.
#

BACKEND_BLOCK_UMASK = settings.PITHOS_BACKEND_BLOCK_UMASK

BACKEND_QUEUE_MODULE = settings.PITHOS_BACKEND_QUEUE_MODULE
BACKEND_QUEUE_HOSTS = settings.PITHOS_BACKEND_QUEUE_HOSTS
BACKEND_QUEUE_EXCHANGE = settings.PITHOS_BACKEND_QUEUE_EXCHANGE

BACKEND_ACCOUNT_QUOTA = settings.PITHOS_BACKEND_ACCOUNT_QUOTA
BACKEND_CONTAINER_QUOTA = settings.PITHOS_BACKEND_CONTAINER_QUOTA

TRANSLATE_UUIDS = settings.PITHOS_TRANSLATE_UUIDS

# --------------------------------------------------------------------
# Backend settings

# Set the credentials (client identifier, client secret) issued for
# authenticating the views with astakos during the resource access token
# generation procedure
OAUTH2_CLIENT_CREDENTIALS = getattr(settings,
                                    'PITHOS_OAUTH2_CLIENT_CREDENTIALS',
                                    (None, None))

# Set domain to restrict requests of pithos object contents serve endpoint or
# None for no domain restriction
UNSAFE_DOMAIN = getattr(settings, 'PITHOS_UNSAFE_DOMAIN', None)

# Archipelago Configuration File
BACKEND_ARCHIPELAGO_CONF = getattr(settings, 'PITHOS_BACKEND_ARCHIPELAGO_CONF',
                                   '/etc/archipelago/archipelago.conf')

# Archipelagp xseg pool size
BACKEND_XSEG_POOL_SIZE = getattr(settings, 'PITHOS_BACKEND_XSEG_POOL_SIZE', 8)

# The maximum interval (in seconds) for consequent backend object map checks
BACKEND_MAP_CHECK_INTERVAL = getattr(settings,
                                     'PITHOS_BACKEND_MAP_CHECK_INTERVAL', 5)
