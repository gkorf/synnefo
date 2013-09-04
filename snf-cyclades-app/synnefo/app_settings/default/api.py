from synnefo.lib.settings.setup import Default, Auto, Mandatory, SubMandatory
from synnefo.lib.settings.default import (mk_auto_configure_base_host,
                                          mk_auto_configure_base_path)

# API configuration
###################

# Astakos groups that have access to '/admin' views.
ADMIN_STATS_PERMITTED_GROUPS = ["admin-stats"]

# Enable/Disable the snapshots feature altogether at the API level.
# If set to False, Cyclades will not expose the '/snapshots' API URL
# of the 'volume' app.
CYCLADES_SNAPSHOTS_ENABLED = True

#
# Network Configuration
#

# CYCLADES_DEFAULT_SERVER_NETWORKS setting contains a list of networks to
# connect a newly created server to, *if the user has not* specified them
# explicitly in the POST /server API call.
# Each member of the list may be a network UUID, a tuple of network UUIDs,
# "SNF:ANY_PUBLIC_IPV4" [any public network with an IPv4 subnet defined],
# "SNF:ANY_PUBLIC_IPV6 [any public network with only an IPV6 subnet defined],
#  or "SNF:ANY_PUBLIC" [any public network].
#
# Access control and quota policy are enforced, just as if the user had
# specified the value of CYCLADES_DEFAULT_SERVER_NETWORKS in the content
# of the POST /call, after processing of "SNF:*" directives."
CYCLADES_DEFAULT_SERVER_NETWORKS = []

# This setting contains a list of networks which every new server
# will be forced to connect to, regardless of the contents of the POST
# /servers call, or the value of CYCLADES_DEFAULT_SERVER_NETWORKS.
# Its format is identical to that of CYCLADES_DEFAULT_SERVER_NETWORKS.

# WARNING: No access control or quota policy are enforced.
# The server will get all IPv4/IPv6 addresses needed to connect to the
# networks specified in CYCLADES_FORCED_SERVER_NETWORKS, regardless
# of the state of the floating IP pool of the user, and without
# allocating any floating IPs."
CYCLADES_FORCED_SERVER_NETWORKS = []

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

# Firewalling. Firewall tags should contain '%d' to be filled with the NIC
# ID.
GANETI_FIREWALL_ENABLED_TAG = Default(
    default_value="synnefo:network:%s:protected",
    example_value="synnefo:network:%s:protected",
    description=(
        "Tag that finds its way down to kvm-vif-bridge to enable "
        "the application of corresponding firewalling rules on the host."),
    export=False,
)

GANETI_FIREWALL_DISABLED_TAG = Default(
    default_value="synnefo:network:%s:unprotected",
    example_value="synnefo:network:%s:unprotected",
    description=(
        "Tag that finds its way down to kvm-vif-bridge to enable "
        "the application of corresponding firewalling rules on the host."),
    export=False,
)

GANETI_FIREWALL_PROTECTED_TAG = Default(
    default_value="synnefo:network:%s:limited",
    example_value="synnefo:network:%s:limited",
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

# URL templates for the stat graphs.
# The API implementation replaces '%s' with the encrypted backend id.
CPU_BAR_GRAPH_URL = SubMandatory(
    example_value='http://stats.example.synnefo.org/stats/v1.0/cpu-bar/%s',
    description="URL to fetch the CPU Bar graph.",
    depends="STATS_ENABLED",
)

CPU_TIMESERIES_GRAPH_URL = SubMandatory(
    example_value="http://stats.example.synnefo.org/stats/v1.0/cpu-ts/%s",
    description="URL to fetch the CPU Timeseries graph.",
    depends="STATS_ENABLED",
)

NET_BAR_GRAPH_URL = SubMandatory(
    example_value="http://stats.example.synnefo.org/stats/v1.0/net-bar/%s",
    description="URL to fetch the NET Bar graph.",
    depends="STATS_ENABLED",
)

NET_TIMESERIES_GRAPH_URL = SubMandatory(
    example_value="http://stats.example.synnefo.org/stats/v1.0/net-ts/%s",
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

# Encryption key for the instance hostname in the stat graphs URLs. Set it to
# a random string and update the STATS_SECRET_KEY setting in the snf-stats-app
# host (20-snf-stats-app-settings.conf) accordingly.
CYCLADES_STATS_SECRET_KEY = "secret_key"

# Recommended refresh period for server stats
STATS_REFRESH_PERIOD = 60

# Template to use to build the FQDN of VMs. The setting will be formated with
# the id of the VM.
CYCLADES_SERVERS_FQDN = 'snf-%(id)s.vm.example.synnefo.org'

# Description of applied port forwarding rules (DNAT) for Cyclades VMs. This
# setting contains a mapping from the port of each VM to a tuple contaning the
# destination IP/hostname and the new port: (host, port). Instead of a tuple a
# python callable object may be used which must return such a tuple. The caller
# will pass to the callable the following positional arguments, in the
# following order:
# * server_id: The ID of the VM in the DB
# * ip_address: The IPv4 address of the public VM NIC
# * fqdn: The FQDN of the VM
# * user: The UUID of the owner of the VM
#
# Here is an example describing the mapping of the SSH port of all VMs to
# the external address 'gate.example.synnefo.org' and port 60000+server_id.
# e.g. iptables -t nat -A prerouting -d gate.example.synnefo.org \
# --dport (61000 + $(VM_ID)) -j DNAT --to-destination $(VM_IP):22
#CYCLADES_PORT_FORWARDING = {
#    22: lambda ip_address, server_id, fqdn, user:
#               ("gate.example.synnefo.org", 61000 + server_id),
#}
CYCLADES_PORT_FORWARDING = {}

# Extra configuration options required for snf-vncauthproxy (>=1.5)
CYCLADES_VNCAUTHPROXY_OPTS = {
    # These values are required for VNC console support. They should match a
    # user / password configured in the snf-vncauthproxy authentication / users
    # file (/var/lib/vncauthproxy/users).
    'auth_user': 'synnefo',
    'auth_password': 'secret_password',
    # server_address and server_port should reflect the --listen-address and
    # --listen-port options passed to the vncauthproxy daemon
    'server_address': '127.0.0.1',
    'server_port': 24999,
    # Set to True to enable SSL support on the control socket.
    'enable_ssl': False,
    # If you enabled SSL support for snf-vncauthproxy you can optionally
    # provide a path to a CA file and enable strict checkfing for the server
    # certficiate.
    'ca_cert': None,
    'strict': False,
}

# The maximum allowed size(GB) for a Cyclades Volume
CYCLADES_VOLUME_MAX_SIZE = 200

# The maximum allowed metadata items for a Cyclades Volume
CYCLADES_VOLUME_MAX_METADATA = 10

# The maximmum allowed metadata items for a Cyclades Virtual Machine
CYCLADES_VM_MAX_METADATA = 10

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
