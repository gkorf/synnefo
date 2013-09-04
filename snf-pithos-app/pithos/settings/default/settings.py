from synnefo.lib.settings.setup import Default, Auto, Mandatory, SubMandatory
from synnefo.lib.settings.default import (mk_auto_configure_base_host,
                                          mk_auto_configure_base_path)

# Pithos configuration
######################

PITHOS_BASE_URL = Mandatory(
    example_value="https://store.example.synnefo.org/pithos/",
    description=(
        "The complete URL which is forwarded by the front-end web server "
        "to the Pithos application server (gunicorn). "),
    category="snf-pithos-app-settings",
)

PITHOS_BASE_HOST = Auto(
    configure_callback=mk_auto_configure_base_host("PITHOS_BASE_URL"),
    export=False,
    description="The host part of PITHOS_BASE_URL. Cannot be configured.",
    dependencies=("PITHOS_BASE_URL",),
)

PITHOS_BASE_PATH = Auto(
    configure_callback=mk_auto_configure_base_path("PITHOS_BASE_URL"),
    export=False,
    description="The path part of PITHOS_BASE_URL. Cannot be configured.",
    dependencies=("PITHOS_BASE_URL",),
)

PITHOS_SERVICE_TOKEN = Mandatory(
    example_value="asdf+V7Pithos_service_token_heredPG==",
    description=(
        "The token used to access Astakos via its API, e.g. for "
        "retrieving a user's email using a user UUID. This can be obtained "
        "by running 'snf-manage component-list' on the Astakos host."),
    category="snf-pithos-app-settings",
)

PITHOS_ASTAKOS_COOKIE_NAME = Default(
    default_value="_pithos2_a",
    example_value="my_service_cookie_name_here",
    description="Cookie name associated with Astakos.",
    export=False,
)

#
# Pools configuration
#

PITHOS_ASTAKOSCLIENT_POOLSIZE = Default(
    default_value=200,
    example_value=200,
    description="Number of concurrent connections to be provided by objpool.",
    export=False,
)

PITHOS_BACKEND_POOL_ENABLED = Default(
    default_value=True,
    description="Whether to use objpool to pool pithos-backend instances.",
    category="snf-pithos-app-settings",
    export=True,
)

PITHOS_BACKEND_POOL_SIZE = Default(
    default_value=5,
    description="Size of the pool used for pithos-backend instances.",
    category="snf-pithos-app-settings",
    export=True,
    dependencies=[PITHOS_BACKEND_POOL_ENABLED],
)

PITHOS_BACKEND_DB_MODULE = Default(
    default_value="pithos.backends.lib.sqlalchemy",
    description="The SQLAlchemy module to use.",
    export=False,
)

PITHOS_BACKEND_BLOCK_MODULE = Default(
    default_value="pithos.backends.lib.hashfiler",
    description="Backend block module to use.",
    export=False,
)

PITHOS_BACKEND_DB_CONNECTION = Mandatory(
    example_value="sqlite:////tmp/pithos-backend.db",
    description="URI pointing to the Pithos database.",
    category="snf-pithos-app-backend",
)

PITHOS_BACKEND_BLOCK_PATH = Mandatory(
    example_value="/usr/share/synnefo/pithos/data/",
    description=(
        "Full path pointing to the directory holding the actual "
        "Pithos data."),
    category="snf-pithos-app-backend",
)

PITHOS_BACKEND_BLOCK_SIZE = Default(
    default_value=4*1024*1024,
    description="Size of blocks stored by the backend.",
    export=False,
)

PITHOS_BACKEND_HASH_ALGORITHM = Default(
    default_value="sha256",
    description="The backend block hashing algorithm.",
    export=False,
)

PITHOS_UPDATE_MD5 = Default(
    default_value=False,
    description="Whether to update object checksums.",
    export=False,
)

#
# File versioning configuration
#

PITHOS_BACKEND_VERSIONING = Default(
    default_value="auto",
    example_value="none",
    description=(
        "Whether child containers will create versions for object "
        "updates. Values can be either 'auto' to inherit the parent "
        "container's value, or 'none' to not create versions."),
    export=False,
)

PITHOS_BACKEND_FREE_VERSIONING = Default(
    default_value=True,
    description=(
        "If True only the last version of the file counts in for the "
        "user's quota usage. If False all versions will consume quotas."),
    export=False,
)

#
# RADOS configuration
#

PITHOS_RADOS_STORAGE = Default(
    default_value=False,
    description="Whether to write objects to a RADOS backend too.",
    category="snf-pithos-app-settings",
    export=True,
)

PITHOS_RADOS_POOL_BLOCKS = SubMandatory(
    example_value="blocks",
    description="Name of the RADOS pool to store data blocks.",
    depends=PITHOS_RADOS_STORAGE,
)

PITHOS_RADOS_POOL_MAPS = SubMandatory(
    example_value="maps",
    description="Name of the RADOS pool to store maps.",
    depends=PITHOS_RADOS_STORAGE,
)

#
# Misc
#

PITHOS_PROXY_USER_SERVICES = Default(
    default_value=True,
    description=(
        "If True, snf-pithos-app will handle all Astakos user-visible "
        "services (e.g.: feedback, login) by proxying them to Astakos. Set to "
        "if snf-astakos-app and snf-pithos-app run on the same machine, so "
        "Astakos handles the requests on its own."),
    export=True,
)

PITHOS_PUBLIC_URL_SECURITY = Default(
    default_value=16,
    description=(
        "How many random bytes to use for constructing the URL of "
        "Pithos public files."),
    export=False,
)

PITHOS_PUBLIC_URL_ALPHABET = Default(
    default_value=(
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    description=(
        "Alphabet to use for constructing the URL of Pithos public files."),
    export=False,
)

PITHOS_API_LIST_LIMIT = Default(
    default_value=10000,
    description=(
        "The maximum nubmer of items returned by the listing methods "
        "of the API."),
    export=False,
)

#
# Obsolete settings
#

# FIXME: This should be removed once the code changes accordingly.
PITHOS_BACKEND_BLOCK_UMASK = Default(
    default_value=0o022,
    description="The umask of files written by Pithos under the data path.",
    export=False,
)

# FIXME: Billing settings should go away along with the corresponding code.
PITHOS_BACKEND_QUEUE_MODULE = Default(
    default_value=None,
    example_vlaue="pithos.backends.lib.rabbitmq",
    description="Module to handle billing notifications.",
    export=False,
)

# FIXME: Billing settings should go away along with the corresponding code.
PITHOS_BACKEND_QUEUE_HOSTS = Default(
    default_value=None,
    example_value="['amqp://guest:guest@localhost:5672']",
    description="AMQP endpoint for billing.",
    export=False,
)

PITHOS_BACKEND_QUEUE_EXCHANGE = Default(
    default_value="pithos",
    description="RabbitMQ exchange to push billing messages.",
    export=False,
)

# FIXME: This should go away along with the relevant code.
PITHOS_BACKEND_ACCOUNT_QUOTA = Default(
    default_value=50*1024*1024*1024,
    description="Quota for a new account.",
    export=False,
)

# FIXME: This should go away along with the relevant code.
PITHOS_BACKEND_CONTAINER_QUOTA = Default(
    default_value=0,
    description=(
        "Quota limit for every newly created container. '0' means "
        "unlimited."),
    export=False,
)

# FIXME: This was needed for transitional reasons, now needs to go away along
# with the corresponding code.
# This enables a ui compatibility layer for the introduction of UUIDs in
# identity management.  WARNING: Setting to True will break your installation.
PITHOS_TRANSLATE_UUIDS = Default(
    default_value=False,
    description="Transitional setting to allow UUID translations.",
    export=False,
)
