from synnefo.lib.settings.setup import Default

# Ganeti backends configuration
###############################

CYCLADES_BACKEND_PREFIX_ID = Default(
    default_value="snf-",
    example_value="my_service_name_prefix-",
    description=(
        "When Synnefo creates an instance on a Ganeti backend, it "
        "names the instance by concatenating the CYCLADES_BACKEND_PREFIX_ID with the "
        "instance's ID as appears in the Cyclades DB."),
    category="snf-cyclades-app-backend",
    export=True,
)

# If True, Ganeti will try to allocate new instances only on nodes that are
# not already locked. This might result in slightly unbalanced clusters.
GANETI_USE_OPPORTUNISTIC_LOCKING = True

# If False, Ganeti will not wait for the disk mirror to sync
# (--no-wait-for-sync option in Ganeti). Useful only for DRBD template.
GANETI_DISKS_WAIT_FOR_SYNC = False

GANETI_CREATEINSTANCE_KWARGS = Default(
    default_value={
        "os": "snf-image+default",
        "hvparams": {"kvm": {"serial_console": False},
                     "xen-pvm": {},
                     "xen-hvm": {}},
        "wait_for_sync": False},
    description=(
        "This dictionary defines deployment-specific arguments to be "
        "passed to the RAPI CreateInstance call. At minimum it should contain "
        "the 'os' and 'hvparams' keys.\n\nMore specifically:\na) os:\n   The "
        "OS provider to use (this should be 'snf-image+default')\nb) "
        "hvparams:\n   Hypervisor-specific parameters for each hypervisor,\n"
        "   currently 'kvm', 'xen-pvm' and 'xen-hvm'. Also, 'serial_console' "
        "should be set to False, see #785.\nc) If using Ganeti's DRBD disk "
        "template, you may want to include\n   'wait_for_sync = FALSE', see "
        "#835."),
    category="snf-cyclades-app-backend",
    export=True,
)

GANETI_USE_HOTPLUG = Default(
    default_value=True,
    example_value=True,
    description=(
        "If True, qemu-kvm will hotplug all NICs when connecting VMs "
        "to Networks. This requires qemu-kvm>=1.0."),
    category="snf-cyclades-app-backend",
    export=True,
)

BACKEND_ALLOCATOR_MODULE = Default(
    default_value="synnefo.cyclades.logic.allocators.default_allocator",
    example_value="synnefo.cyclades.logic.allocators.my_allocator",
    description=(
        "Module that implements the strategy for allocating Synnefo "
        "VMs to Ganeti backends."),
    export=False,
)

BACKEND_REFRESH_MIN = Default(
    default_value=15,
    example_value=15,
    description=(
        "Maximum time in minutes, before the allocator collects new "
        "statitistics for all Ganeti backens."),
    export=False,
)

# Maximum number of NICs per Ganeti instance. This value must be less or equal
# than 'max:nic-count' option of Ganeti's ipolicy.
GANETI_MAX_NICS_PER_INSTANCE = 8

# Maximum number of disks per Ganeti instance. This value must be less or equal
# than 'max:disk-count' option of Ganeti's ipolicy.
GANETI_MAX_DISKS_PER_INSTANCE = 8

# The following setting defines a dictionary with key-value parameters to be
# passed to each Ganeti ExtStorage provider. The setting defines a mapping from
# the provider name, e.g. 'archipelago' to a dictionary with the actual
# arbitrary parameters.
GANETI_DISK_PROVIDER_KWARGS = {}

# List of ExtStorage providers that support cloning. For these providers, the
# hashmap of the image is passed as an ExtStorage disk parameter('origin') and,
# since disk will be already filled with data, 'snf-image' performs only
# customization (no data copying).
GANETI_CLONE_PROVIDERS = ['vlmc', 'archipelago']
