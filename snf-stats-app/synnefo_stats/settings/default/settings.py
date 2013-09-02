from synnefo.settings.setup import Default, Mandatory, Auto
from synnefo.settings.setup.defaults import (mk_auto_configure_base_host,
                                             mk_auto_configure_base_path)

STATS_BASE_URL = Mandatory(
    example_value="https://stats.example.synnefo.org/stats/",
    description=(
        "The complete URL which is forwarded by the front-end web server "
        "to the Astakos application server (gunicorn). "),
)

STATS_BASE_HOST = Auto(
    configure_callback=mk_auto_configure_base_host("STATS_BASE_URL"),
    export=False,
    description="The host part of STATS_BASE_URL. Cannot be configured.",
    dependencies=("STATS_BASE_URL",),
)

STATS_BASE_PATH = Auto(
    configure_callback=mk_auto_configure_base_path("STATS_BASE_URL"),
    export=False,
    description="The path part of STATS_BASE_URL. Cannot be configured.",
    dependencies=("STATS_BASE_URL",),
)

#
# Image properties
#

STATS_IMAGE_WIDTH = Default(
    default_value=210,
    description="",
    export=False,
)

STATS_WIDTH = Default(
    default_value=68,
    description="",
    export=False,
)

STATS_HEIGHT = Default(
    default_value=10,
    description="",
    export=False,
)

#
# Path settings
#

STATS_RRD_PREFIX = Default(
    default_value="/var/lib/collectd/rrd/",
    description="",
    export=False,
)

STATS_GRAPH_PREFIX = Default(
    default_value="/var/cache/snf-stats-app/",
    description="",
    export=False,
)

#
# Font settings
#

STATS_FONT = Default(
    default_value="/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",
    description="Font to be used in the stats diagrams.",
    export=False,
)

#
# Bar settings
#

STATS_BAR_BORDER_COLOR = Default(
    default_value=(0x5c, 0xa1, 0xc0),
    description="",
    export=False,
)

STATS_BAR_BG_COLOR = Default(
    default_value=(0xea, 0xea, 0xea),
    description="",
    export=False,
)
