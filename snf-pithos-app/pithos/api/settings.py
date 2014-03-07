#coding=utf8
from django.conf import settings
from synnefo.lib import parse_base_url, join_urls
from synnefo.lib.services import get_service_prefix

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

ASTAKOS_ACCOUNTS_PREFIX = get_service_prefix(synnefo_services, 'astakos_account')
ASTAKOS_VIEWS_PREFIX = get_service_prefix(synnefo_services, 'astakos_ui')
ASTAKOS_KEYSTONE_PREFIX = get_service_prefix(synnefo_services, 'astakos_identity')

BASE_ASTAKOS_PROXY_PATH = getattr(settings, 'PITHOS_BASE_ASTAKOS_PROXY_PATH',
                                  ASTAKOS_BASE_PATH)
BASE_ASTAKOS_PROXY_PATH = join_urls(BASE_PATH, BASE_ASTAKOS_PROXY_PATH)
BASE_ASTAKOS_PROXY_PATH = BASE_ASTAKOS_PROXY_PATH.strip('/')


ASTAKOSCLIENT_POOLSIZE = getattr(settings, 'PITHOS_ASTAKOSCLIENT_POOLSIZE', 200)

COOKIE_NAME = getattr(settings, 'PITHOS_ASTAKOS_COOKIE_NAME', '_pithos2_a')

# SQLAlchemy (choose SQLite/MySQL/PostgreSQL).
BACKEND_DB_MODULE = getattr(
    settings, 'PITHOS_BACKEND_DB_MODULE', 'pithos.backends.lib.sqlalchemy')
BACKEND_DB_CONNECTION = getattr(settings, 'PITHOS_BACKEND_DB_CONNECTION',
                                'sqlite:////tmp/pithos-backend.db')

# Block storage.
BACKEND_BLOCK_MODULE = getattr(
    settings, 'PITHOS_BACKEND_BLOCK_MODULE', 'pithos.backends.lib.hashfiler')
BACKEND_BLOCK_PATH = getattr(
    settings, 'PITHOS_BACKEND_BLOCK_PATH', '/tmp/pithos-data/')
BACKEND_BLOCK_UMASK = getattr(settings, 'PITHOS_BACKEND_BLOCK_UMASK', 0o022)

# Queue for billing.
BACKEND_QUEUE_MODULE = getattr(settings, 'PITHOS_BACKEND_QUEUE_MODULE',
                               None)  # Example: 'pithos.backends.lib.rabbitmq'
BACKEND_QUEUE_HOSTS = getattr(settings, 'PITHOS_BACKEND_QUEUE_HOSTS', None) # Example: "['amqp://guest:guest@localhost:5672']"
BACKEND_QUEUE_EXCHANGE = getattr(settings, 'PITHOS_BACKEND_QUEUE_EXCHANGE', 'pithos')

# Default setting for new accounts.
BACKEND_ACCOUNT_QUOTA = getattr(
    settings, 'PITHOS_BACKEND_ACCOUNT_QUOTA', 50 * 1024 * 1024 * 1024)
BACKEND_CONTAINER_QUOTA = getattr(
    settings, 'PITHOS_BACKEND_CONTAINER_QUOTA', 0)
BACKEND_VERSIONING = getattr(settings, 'PITHOS_BACKEND_VERSIONING', 'auto')
BACKEND_FREE_VERSIONING = getattr(settings, 'PITHOS_BACKEND_FREE_VERSIONING', True)

# Enable backend pooling
BACKEND_POOL_ENABLED = getattr(settings, 'PITHOS_BACKEND_POOL_ENABLED', True)

# Default backend pool size
BACKEND_POOL_SIZE = getattr(settings, 'PITHOS_BACKEND_POOL_SIZE', 5)

# Update object checksums.
UPDATE_MD5 = getattr(settings, 'PITHOS_UPDATE_MD5', False)

# Service Token acquired by identity provider.
SERVICE_TOKEN = getattr(settings, 'PITHOS_SERVICE_TOKEN', '')

RADOS_STORAGE = getattr(settings, 'PITHOS_RADOS_STORAGE', False)
RADOS_POOL_BLOCKS= getattr(settings, 'PITHOS_RADOS_POOL_BLOCKS', 'blocks')
RADOS_POOL_MAPS = getattr(settings, 'PITHOS_RADOS_POOL_MAPS', 'maps')

# This enables a ui compatibility layer for the introduction of UUIDs in
# identity management.  WARNING: Setting to True will break your installation.
TRANSLATE_UUIDS = getattr(settings, 'PITHOS_TRANSLATE_UUIDS', False)

# Set PROXY_USER_SERVICES to True to have snf-pithos-app handle all Astakos
# user-visible services (feedback, login, etc.) by proxying them to a running
# Astakos.
# Set to False if snf astakos-app is running on the same machine, so it handles
# the requests on its own.
PROXY_USER_SERVICES = getattr(settings, 'PITHOS_PROXY_USER_SERVICES', True)

# Set how many random bytes to use for constructing the URL of Pithos public files
PUBLIC_URL_SECURITY =  getattr(settings, 'PITHOS_PUBLIC_URL_SECURITY', 16)
# Set the alphabet to use for constructing the URL of Pithos public files
PUBLIC_URL_ALPHABET =  getattr(
    settings,
    'PITHOS_PUBLIC_URL_ALPHABET',
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
)

# The maximum number or items returned by the listing api methods
API_LIST_LIMIT = getattr(settings, 'PITHOS_API_LIST_LIMIT', 10000)

# The backend block size
BACKEND_BLOCK_SIZE = getattr(
    settings, 'PITHOS_BACKEND_BLOCK_SIZE', 4 * 1024 * 1024)

# The backend block hash algorithm
BACKEND_HASH_ALGORITHM = getattr(
    settings, 'PITHOS_BACKEND_HASH_ALGORITHM', 'sha256')
