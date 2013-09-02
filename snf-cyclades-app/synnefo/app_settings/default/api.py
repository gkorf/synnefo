from synnefo.settings.setup import Default, Auto, Mandatory, SubMandatory
from synnefo.settings.default import (mk_auto_configure_base_host,
                                      mk_auto_configure_base_path)

# API configuration
###################

#
# Network Configuration
#

CYCLADES_BASE_URL = Mandatory(
    example_value="https://compute.example.synnefo.org/cyclades/",
    description=(
        "The complete URL which is forwarded by the front-end web server "
        "to the Cyclades application server (gunicorn). "),
    category="snf-cyclades-app-api",
)

CYCLADES_BASE_HOST = Auto(
    configure_callback=mk_auto_configure_base_host("CYCLADES_BASE_URL"),
    export=False,
    description="The host part of CYCLADES_BASE_URL. Cannot be configured.",
    dependencies=("CYCLADES_BASE_URL",),
)

CYCLADES_BASE_PATH = Auto(
    configure_callback=mk_auto_configure_base_path("CYCLADES_BASE_URL"),
    export=False,
    description="The path part of CYCLADES_BASE_URL. Cannot be configured.",
    dependencies=("CYCLADES_BASE_URL",),
)

DEFAULT_INSTANCE_NETWORKS = Default(
    default_value=["SNF:ANY_PUBLIC"],
    example_value=["SNF:ANY_PUBLIC", "1", "2"],
    description=(
        "List of network IDs as known by Cyclades. All newly created "
        "instances will get a number of NICs each one connected to a network "
        "of this list. If the special network ID 'SNF:ANY_PUBLIC' is used, "
        "Cyclades will automatically choose a public network and connect the "
        "instance to it."),
    category="snf-cyclades-app-api",
    export=True,
)

API_ENABLED_NETWORK_FLAVORS = Default(
    default_value=["MAC_FILTERED"],
    example_value=["MAC_FILTERED", "PHYSICAL_VLAN"],
    description=(
        "The supported types of Private Virtual Networks to be "
        "exported to users via the API. End users will be able to create "
        "Private Networks only of the types included in this list."),
    category="snf-cyclades-app-api",
    export=True,
)

DEFAULT_MAC_FILTERED_BRIDGE = Default(
    default_value="prv0",
    example_value="prv0",
    description=(
        "The name of the bridge that all MAC_FILTERED type networks "
        "will use."),
    category="snf-cyclades-app-api",
    export=True,
)

DEFAULT_ROUTING_TABLE = Default(
    default_value="snf_public",
    example_value="snf_public",
    description=(
        "The host's routing table that will be used by the "
        "IP_LESS_ROUTED type network."),
    category="snf-cyclades-app-api",
    export=True,
)

MAX_CIDR_BLOCK = Default(
    default_value=22,
    example_value=22,
    description="Maximum allowed network size for private networks.",
    export=False,
)

DEFAULT_MAC_PREFIX = Default(
    default_value="aa:00:0",
    example_value="aa:00:0",
    description=(
        "All NICs connected to all types of networks, except the "
        "MAC_FILTERED ones (that use MAC prefix pools), will have this MAC "
        "prefix."),
    export=False,
)

DEFAULT_BRIDGE = Default(
    default_value="br0",
    example_value="br0",
    description="The default bridge to connect all CUSTOM networks.",
    export=False,
)

#
# Firewall configuration
#

GANETI_FIREWALL_ENABLED_TAG = Default(
    default_value="synnefo:network:0:protected",
    example_value="synnefo:network:0:protected",
    description=(
        "Tag that finds its way down to kvm-vif-bridge to enable "
        "the application of corresponding firewalling rules on the host."),
    export=False,
)

GANETI_FIREWALL_DISABLED_TAG = Default(
    default_value="synnefo:network:0:unprotected",
    example_value="synnefo:network:0:unprotected",
    description=(
        "Tag that finds its way down to kvm-vif-bridge to enable "
        "the application of corresponding firewalling rules on the host."),
    export=False,
)

GANETI_FIREWALL_PROTECTED_TAG = Default(
    default_value="synnefo:network:0:limited",
    example_value="synnefo:network:0:limited",
    description=(
        "Tag that finds its way down to kvm-vif-bridge to enable "
        "the application of corresponding firewalling rules on the host."),
    export=False,
)

DEFAULT_FIREWALL_PROFILE = Default(
    default_value="DISABLED",
    example_value="DISABLED",
    description="Default firewall profile to apply, if no tags are defined.",
    export=False,
)

#
# Stat graphs configuration
#

STATS_ENABLED = Default(
    default_value=False,
    example_value=False,
    description=(
        "Whether stat graphs are enabled, so the UI knows whether to "
        "present them or not. Make sure the stats app is working successfully "
        "before enabling this option."),
    category="snf-cyclades-app-api",
    export=True,
)

# The API implementation replaces '%s' with the encrypted backend id.
# FIXME: For now we do not encrypt the backend id.
CPU_BAR_GRAPH_URL = SubMandatory(
    example_value="http://stats.synnefo.org/%s/cpu-bar.png",
    description="URL to fetch the CPU Bar graph.",
    depends="STATS_ENABLED",
)

CPU_TIMESERIES_GRAPH_URL = SubMandatory(
    example_value="http://stats.synnefo.org/%s/cpu-ts.png",
    description="URL to fetch the CPU Timeseries graph.",
    depends="STATS_ENABLED",
)

NET_BAR_GRAPH_URL = SubMandatory(
    example_value="http://stats.synnefo.org/%s/net-bar.png",
    description="URL to fetch the NET Bar graph.",
    depends="STATS_ENABLED",
)

NET_TIMESERIES_GRAPH_URL = SubMandatory(
    example_value="http://stats.synnefo.org/%s/net-ts.png",
    description="URL to fetch the NET Timeseries graph.",
    depends="STATS_ENABLED",
)

STATS_REFRESH_PERIOD = SubMandatory(
    example_value=60,
    description="Refresh period for server stats.",
    depends="STATS_ENABLED",
)

#
# Personality/File injection configuration
#

MAX_PERSONALITY = Default(
    default_value=5,
    example_value=5,
    description=(
        "The maximum nubmer of files that the user can inject into a "
        "newly created instance."),
    export=False,
)

MAX_PERSONALITY_SIZE = Default(
    default_value=10240,
    example_value=10240,
    description=(
        "The maximum allowed size, in bytes, for each personality "
        "file to be injected into a newly created instance."),
    export=False,
)

#
# Misc configuration
#

BACKEND_PER_USER = Default(
    default_value={},
    example_value={'user1@synnefo.org': 2,
                   'user2@synnefo.org': 3},
    description=(
        "Associate a user with a specific Ganeti backend. All VMs of the "
        "users in this dict will get allocated to the specified backends."),
    category="snf-cyclades-app-api",
    export=True,
)

ARCHIPELAGO_BACKENDS = Default(
    default_value=[],
    example_value=["1", "2", "3"],
    description=(
        "Ganeti backends on this list are used to host only "
        "Archipelago-backed VMs. Also, all Archipelago-backed VMs will get "
        "allocated only to backends that are included in this list."),
    category="snf-cyclades-app-api",
    expose=True,
)

CYCLADES_ASTAKOSCLIENT_POOLSIZE = Default(
    default_value=50,
    example_value=50,
    description=(
        "Number of the concurrent Astakos http client connections, "
        "as provided by the connection pool."),
    export=False,
)

SECRET_ENCRYPTION_KEY = Mandatory(
    example_value="Password Encryption Key",
    description=(
        "Key for password encryption-decryption. After changing this "
        "setting, Synnefo will be unable to decrypt all existing Backend "
        "passwords. You will need to store the new password again on all "
        "Backends by using 'snf-manage backend-modify'. The key may be up to "
        "32 bytes. Keys bigger than 32 bytes are not supported."),
    category="snf-cyclades-app-api",
)

CYCLADES_SERVICE_TOKEN = Mandatory(
    example_value="asdf+V7Cyclades_service_token_heredPG==",
    description=(
        "The token used to access Astakos via its API, e.g. for "
        "retrieving a user's email using a user UUID. This can be obtained "
        "by running 'snf-manage component-list' on the Astakos host."),
    category="snf-cyclades-app-api",
)

CYCLADES_PROXY_USER_SERVICES = Default(
    default_value=True,
    example_value=True,
    description=(
        "If True, Cyclades will proxy user specific API calls to "
        "Astakos via self-served endpoints. Set this to False if you deploy "
        "'snf-cyclades-app' and 'snf-astakos-app' on the same machine."),
    category="snf-cyclades-app-api",
    export=True,
)

POLL_LIMIT = Default(
    default_value=3600,
    example_value=3600,
    description=(
        "The API will return HTTP Bad Request if the ?changes-since "
        "parameter refers to a point in time older than POLL_LIMIT seconds."),
    export=False,
)
