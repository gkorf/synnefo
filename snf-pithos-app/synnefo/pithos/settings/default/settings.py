from synnefo.lib.settings.setup import Default, Auto, Mandatory, SubMandatory
from synnefo.webproject.settings.default import (
    mk_auto_configure_base_host,
    mk_auto_configure_base_path,
    mk_auto_configure_services)

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
    autoconfigure=mk_auto_configure_base_host("PITHOS_BASE_URL"),
    export=False,
    description="The host part of PITHOS_BASE_URL. Cannot be configured.",
    dependencies=["PITHOS_BASE_URL"],
)

PITHOS_BASE_PATH = Auto(
    autoconfigure=mk_auto_configure_base_path("PITHOS_BASE_URL"),
    export=False,
    description="The path part of PITHOS_BASE_URL. Cannot be configured.",
    dependencies=["PITHOS_BASE_URL"],
)

PITHOS_SERVICES = Auto(
    autoconfigure=mk_auto_configure_services("pithos", "PITHOS_BASE_URL"),
    description="Definition of services provided by the Pithos component",
    export=False,
    dependencies=["PITHOS_BASE_URL", "SYNNEFO_COMPONENTS"],
)

PITHOS_SERVICE_TOKEN = Mandatory(
    example_value="asdf+V7Pithos_service_token_heredPG==",
    description=(
        "The token used to access Astakos via its API, e.g. for "
        "retrieving a user's email using a user UUID. This can be obtained "
        "by running 'snf-manage component-list' on the Astakos host."),
    category="snf-pithos-app-settings",
)

ASTAKOS_AUTH_URL = Mandatory(
    example_value='https://accounts.example.synnefo.org/astakos/identity/v2.0',
    description="Astakos auth URL",
    category="",
)

PITHOS_ASTAKOSCLIENT_POOLSIZE = Default(
    default_value=200,
    example_value=200,
    description="Number of concurrent connections to be provided by objpool.",
    export=False,
)

PITHOS_BACKEND_DB_MODULE = Default(
    default_value="synnefo.pithos.backends.lib.sqlalchemy",
    description="The SQLAlchemy module to use.",
    export=False,
)

PITHOS_BACKEND_DB_CONNECTION = Mandatory(
    example_value="sqlite:////tmp/pithos-backend.db",
    description="URI pointing to the Pithos database.",
    category="snf-pithos-app-backend",
)

PITHOS_BACKEND_BLOCK_MODULE = Default(
    default_value="synnefo.pithos.backends.lib.hashfiler",
    description="Backend block module to use.",
    export=False,
)

PITHOS_BACKEND_BLOCK_PATH = Mandatory(
    example_value="/usr/share/synnefo/pithos/data/",
    description=(
        "Full path pointing to the directory holding the actual "
        "Pithos data."),
    category="snf-pithos-app-backend",
)

# FIXME: This should be removed once the code changes accordingly.
PITHOS_BACKEND_BLOCK_UMASK = Default(
    default_value=0o022,
    description="The umask of files written by Pithos under the data path.",
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
)

PITHOS_UPDATE_MD5 = Default(
    default_value=False,
    description="Whether to update object checksums.",
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
    dependencies=['PITHOS_RADOS_STORAGE'],
)

PITHOS_RADOS_POOL_MAPS = SubMandatory(
    example_value="maps",
    description="Name of the RADOS pool to store maps.",
    dependencies=['PITHOS_RADOS_STORAGE'],
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

PITHOS_OAUTH2_CLIENT_CREDENTIALS = Default(
    default_value=(None, None),
    example_value=('pithos-view', 'oa_secret'),
    description="Credentials for the oauth2 client",
    category="snf-pithos-app-settings",
)

PITHOS_UNSAFE_DOMAIN = Default(
    default_value=None,
    example_value="user-content.example.com",
    description=("Set domain to restrict requests of pithos object "
                 "contents serve endpoint or None for no domain restriction"),
    category="snf-pithos-app-settings",
)

PITHOS_BACKEND_ARCHIPELAGO_CONF = Default(
    default_value='/etc/archipelago/archipelago.conf',
    description="Archipelago Configuration File",
    category="snf-pithos-app-settings",
    export=False,
)

PITHOS_BACKEND_XSEG_POOL_SIZE = Default(
    default_value=8,
    description="Archipelagp xseg pool size",
    category="snf-pithos-app-settings",
)

PITHOS_BACKEND_MAP_CHECK_INTERVAL = Default(
    default_value=5,
    description=("The maximum interval (in seconds) for consequent backend "
                 "object map checks"),
    category="snf-pithos-app-settings",
)

PITHOS_BACKEND_MAPFILE_PREFIX = Default(
    default_value='snf_file_',
    description=("The archipelago mapfile prefix (it should not exceed "
                 "15 characters). WARNING: Once set it should not be changed"),
    category="snf-pithos-app-settings",
)

PITHOS_RESOURCE_MAX_METADATA = Default(
    default_value=32,
    description=("The maximum allowed metadata items per domain "
                 "for a Pithos+ resource"),
    category="snf-pithos-app-settings",
)

PITHOS_ACC_MAX_GROUPS = Default(
    default_value=32,
    description="The maximum allowed groups for a Pithos+ account.",
    category="snf-pithos-app-settings",
)

PITHOS_ACC_MAX_GROUP_MEMBERS = Default(
    default_value=32,
    description="The maximum allowed group members per group.",
    category="snf-pithos-app-settings",
)
