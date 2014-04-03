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

BACKEND_BLOCK_PATH = Mandatory(
    example_value="/usr/share/synnefo/pithos/data/",
    description=(
        "Full path pointing to the directory holding the actual "
        "Pithos data."),
    category="snf-cyclades-app-plankton",
)

PITHOS_BACKEND_POOL_SIZE = 8

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

DEFAULT_CONTAINER_FORMAT = Default(
    default_value="bare",
    description="The default image container format.",
    export=False,
)
