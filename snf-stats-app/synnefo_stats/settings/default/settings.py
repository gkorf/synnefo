from synnefo.settings.setup import Setting, Default, Mandatory

#
# Image properties
#

STATS_IMAGE_WIDTH = Default(
    default_value=210,
    description="",
    export=False,
)

STATS_WIDTH = Default(
    default=68,
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
