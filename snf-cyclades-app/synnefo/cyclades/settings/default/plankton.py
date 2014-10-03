from synnefo.lib.settings.setup import Mandatory, Default

# Plankton configuration
########################

BACKEND_DB_CONNECTION = Mandatory(
    example_value=(
        "sqlite:////usr/share/synnefo/pithos/backend.db or "
        "postgresql://user:password@host:port/db_name"),
    description="URI pointing to the Pithos database.",
    category="snf-cyclades-app-plankton",
)

PLANKTON_PITHOS_BACKEND_POOL_SIZE = Default(
    default_value=8,
    example_value=8,
    description="Number of concurrent connections to be provided by objpool.",
    export=False,
)

ALLOWED_DISK_FORMATS = Default(
    default_value=("diskdump", "extdump", "ntfsdump"),
    description=(
        "The allowed image formats. These are the only formats "
        "supported by Synnefo."),
    export=False,
)

DEFAULT_DISK_FORMAT = Default(
    default_value="diskdump",
    example_value="diskdump",
    description="The default image format used by Synnefo.",
    export=False,
)

ALLOWED_CONTAINER_FORMATS = Default(
    default_value=("aki", "ari", "ami", "bare", "ovf"),
    description="The allowed image container formats.",
    export=False,
)

# The owner of the images that will be marked as "system images" by the UI
SYSTEM_IMAGES_OWNER = 'okeanos'

# Archipelago Configuration File
PITHOS_BACKEND_ARCHIPELAGO_CONF = '/etc/archipelago/archipelago.conf'

# Archipelagp xseg pool size
PITHOS_BACKEND_XSEG_POOL_SIZE = 8

# The maximum interval (in seconds) for consequent backend object map checks
PITHOS_BACKEND_MAP_CHECK_INTERVAL = 1

#The maximum allowed number of image metadata
PITHOS_RESOURCE_MAX_METADATA = 32

DEFAULT_CONTAINER_FORMAT = Default(
    default_value="bare",
    description="The default image container format.",
    export=False,
)
