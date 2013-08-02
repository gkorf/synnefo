# -*- coding: utf-8 -*-

from synnefo.settings.setup import Mandatory, Default

# UI configuration
##################

# A list of suggested server tags (server metadata keys)
DEFAULT_KEYWORDS = ["OS", "Role", "Location", "Owner"]

UI_MEDIA_URL = Default(
    default_value=MEDIA_URL + "ui/static/snf/",
    description="Base URL for UI static files.",
    dependencies=[MEDIA_URL],
    export=False,
)

UI_AUTH_COOKIE_NAME = Default(
    default_value="_pithos2_a",
    example_value="my_service_cookie_name_here",
    description="Cookie name to retrieve authentication data from.",
    export=False,
)

UI_SYSTEM_IMAGES_OWNERS = Default(
    default_value={},
    example_value={
        "admin@example.synnefo.org": "system",
        "images@example.synnefo.org": "system"
    },
    description="Dict of Image owner IDs and their associated name to be "
        "displayed on Images list. If a user appears in this dict, his/her "
        "images will appear under the 'System' images tab on the VM creation "
        "wizard.",
    category="snf-cyclades-app-ui",
    export=True,
)

VM_CREATE_SUGGESTED_FLAVORS = Default(
    default_value={
        "small": {
            "cpu": 1,
            "ram": 1024,
            "disk": 20,
            "disk_template": "drbd"
        },
        "medium": {
            "cpu": 2,
            "ram": 2048,
            "disk": 30,
            "disk_template": "drbd"
        },
        "large": {
            "cpu": 4,
            "ram": 4096,
            "disk": 40,
            "disk_template": "drbd"
        }
    },
    description="Flavor options that the wizard suggests to the user as "
        "predefined CPU/RAM/Disk combinations.",
    category="snf-cyclades-app-ui",
    export=True,
)

UI_FLAVORS_DISK_TEMPLATES_INFO = Default(
    default_value={
        "drbd": {
            "name": "Standard",
            "description": "Highly available persistent storage (DRBD)."
        }
    },
    example_value={
        "drbd": {
            "name": "Standard",
            "description": "Highly available persistent storage (DRBD)."
        },
        "plain": {
            "name": "Local",
            "description": "Fast, not high available local storage (LVM)."
        },
        "rbd": {
            "name": "RBD",
            "description": "VM disks residing inside a RADOS cluster."
        },
        "file": {
            "name": "File",
            "description": "VM disks are files on a local filesystem."
        },
        "ext_archipelago": {
            "name": "Archipelago",
            "description": "Volumes residing on our custom storage layer "
                           "Archipelago, supporting fast VM spawning using "
                           "cloning."
        }
    },
    description="Name/Description of the available disk templates for flavors. "
        "Dict key is the 'disk_template' value as stored in the Cyclades DB. ",
    category="snf-cyclades-app-ui",
    export=True,
)

VM_CREATE_NAME_TPL = Default(
    default_value="My {0} server",
    example_value="My {0} server",
    description="Default suggested name for a new VM. '{0}' gets replaced by "
        "the image's OS value.",
    category="snf-cyclades-app-ui",
    export=True,
)

UI_VM_HOSTNAME_FORMAT = Mandatory(
    example_value="snf-%(id)s.vm.example.synnefo.org",
    description="Template to use to build the VM's hostname.",
    category="snf-cyclades-app-ui",
)

VM_CREATE_SUGGESTED_ROLES = Default(
    default_value=["Database server", "File server", "Mail server",
                   "Web server", "Proxy"],
    description="Suggested VM roles to be displayed by the create wizard to "
        "the user. If selected by the user, they will be added as metadata to "
        "the newly created VM, with 'Role' as the key.",
    category="snf-cyclades-app-ui",
    export=True,
)

IMAGE_ICONS = Default(
    default_value=["rhel", "ubuntu", "debian", "windows", "gentoo",
                   "archlinux", "centos", "fedora", "freebsd", "netbsd",
                   "openbsd", "slackware", "sles", "opensuse", "kubuntu"],
    description="List of supported icons for OS Images.",
    export=False,
)

VM_IMAGE_COMMON_METADATA = Default(
    default_value=["OS", "loginname", "logindomain", "users", "remote"],
    description="List of metadata keys to clone from the image to the virtual "
        "machine during its creation.",
    export=False,
)

#
# UI Network view configuration
#

UI_NETWORK_AVAILABLE_NETWORK_TYPES = Default(
    default_value={"MAC_FILTERED": "mac-filtering"},
    description="Available network types to choose from, when creating a new "
        "private virtual network. If only one is set, no options will be "
        "displayed and all networks will have that type.",
    category="snf-cyclades-app-ui",
    export=True,
)

UI_NETWORK_AVAILABLE_SUBNETS = Default(
    default_value=['10.0.0.0/24', '192.168.0.0/24'],
    description="Suggested CIDRs to choose from, when creating a private "
        "virtual network with DHCP enabled.",
    category="snf-cyclades-app-ui",
    export=True,
)

UI_AUTOMATIC_NETWORK_RANGE_FORMAT = Default(
    default_value="192.168.%d.0/24",
    description="UI will use this setting to find an available network subnet, "
        "if user requests automatic subnet allocation.",
    category="snf-cyclades-app-ui",
    export=True,
)

UI_NETWORK_ALLOW_DUPLICATE_VM_NICS = Default(
    default_value=False,
    description="Whether to allow a VM to connect twice in the same network.",
    export=False,
)

UI_NETWORK_STRICT_DESTROY = Default(
    default_value=True,
    description="If True, display the 'Destroy' action on private networks "
        "only if all VMs are disconnected from it.",
    export=False,
)

UI_GROUP_PUBLIC_NETWORKS = Default(
    default_value=True,
    description="Whether or not to group all public networks to a single one.",
    export=False,
)

UI_GROUPED_PUBLIC_NETWORK_NAME = Default(
    default_value="Internet",
    description="The name of the network that groups all public ones.",
    dependencies=[UI_GROUP_PUBLIC_NETWORKS],
    export=False,
)

#
# Interval between API calls configuration
#

UI_UPDATE_INTERVAL = Default(
    default_value=5000,
    example_value=5000,
    description="Interval in milliseconds after which the UI should fetch API "
        "changes.",
    category="snf-cyclades-app-ui",
    export=True,
)

UI_UPDATE_INTERVAL_INCREASE = Default(
    default_value=UI_UPDATE_INTERVAL/4,
    description="Increase the interval by that many milliseconds, as time goes "
        "by and no action on the UI occurs.",
    export=False,
)

UI_UPDATE_INTERVAL_INCREASE_AFTER_CALLS_COUNT = Default(
    default_value=4,
    description="After so many recurrent calls, increase the interval.",
    export=False,
)

UI_UPDATE_INTERVAL_MAX = Default(
    default_value=UI_UPDATE_INTERVAL*3,
    description="Maximum time in milliseconds that an interval can last.",
    export=False,
)

UI_UPDATE_INTERVAL_FAST = Default(
    default_value=UI_UPDATE_INTERVAL/2,
    description="Interval will drop to so many milliseconds, when specific "
        "actions happen on the UI, to increase responsiveness.",
    export=False,
)

UI_CHANGES_SINCE_ALIGNMENT = Default(
    default_value=0,
    description="Milliseconds to remove from the previous server response time "
        "used in consecutive API calls (aligning the 'changes-since' "
        "attribute).",
    export=False,
)

TIMEOUT = Default(
    default_value=10*1000,
    example_value=10*1000,
    description="UI requests to the API layer will time out after that many "
        "milliseconds.",
    export=False,
)

#
# UI behavior configuration
#

UI_DELAY_ON_BLUR = Default(
    default_value=False,
    description="Whether to increase the time of recurrent requests "
        "(networks/vms update), if window loses its focus.",
    export=False,
)

UI_UPDATE_HIDDEN_VIEWS = Default(
    default_value=False,
    description="Whether not visible VM views will update their content, if VM "
        "changes.",
    export=False,
)

UI_SKIP_TIMEOUTS = Default(
    default_value=1,
    description="After how many timeouts of recurrent Ajax requests to display "
        "the timeout error overlay.",
    export=False,
)

UI_HANDLE_WINDOW_EXCEPTIONS = Default(
    default_value=True,
    description="Whether the UI should display error overlays for all "
        "Javascript exceptions.",
    export=False,
)

#
# Misc configuration
#

# Override default connect prompt messages. The setting gets appended to the
# ui default values so you only need to modify parameters you need to alter.
#
# Indicative format:
# {
#    '<browser os1>': {
#        '<vm os family1>': ['top message....', 'bottom message'],
#        '<vm os family 2>': ['top message....', 'bottom message'],
#        'ssh_message': 'ssh %(user)s@%(hostname)s'
# }
#
# you may use the following parameters to format ssh_message:
#
# * server_id: the database pk of the vm
# * ip_address: the ipv4 address of the public vm nic
# * hostname: vm hostname
# * user: vm username
#
# you may assign a callable python object to the ssh_message, if so the above
# parameters get passed as arguments to the provided object.

UI_CONNECT_PROMPT_MESSAGES = Default(
    default_value={},
    description="Connect prompt messages.",
    export=False,
)

UI_EXTRA_RDP_CONTENT = Default(
    default_value=None,
    description="Extend RDP file content. May be a string with format "
        "parameters similar to those used in 'UI_CONNECT_PROMPT_MESSAGES' "
        "`ssh_message` or a callable object.",
    export=False,
)

# FIXME: This should go away; we always fetch from Glance.
UI_ENABLE_GLANCE = Default(
    default_value=True,
    description="Whether or not the UI should display images from the Glance "
        "API set in UI_GLANCE_API_URL. If False, the UI will request images "
        "from the Compute API.",
    export=False,
)

# FIXME: This setting can be calculated since v0.14 and should go away.
UI_SUPPORT_SSH_OS_LIST = Default(
    default_value=["debian", "fedora", "okeanos", "ubuntu", "kubuntu",
                   "centos", "archlinux", "sles", "opensuse", "rhel"],
    description="List of OS names that support SSH public key assignment.",
    export=False,
)

# FIXME: This setting can be calculated since v0.14 and should go away.
UI_OS_DEFAULT_USER_MAP = Default(
    default_value={
        "debian": "root",
        "fedora": "root",
        "okeanos": "root",
        "ubuntu": "root",
        "kubuntu": "root",
        "centos": "root",
        "archlinux": "root",
        "sles": "root",
        "opensuse": "root",
        "rhel": "root",
        "windows": "Administrator"
    },
    description="OS/Username map to identify default user name for specified "
        "OS.",
    export=False,
)
