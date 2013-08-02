from synnefo.settings.setup import Setting, Mandatory, Default

# Ganeti backends configuration
###############################

BACKEND_PREFIX_ID = Default(
    default_value="snf-",
    example_value="my_service_name_prefix-",
    description="When Synnefo creates an instance on a Ganeti backend, it "
        "names the instance by concatenating the BACKEND_PREFIX_ID with the "
        "instance's ID as appears in the Cyclades DB.",
    category="snf-cyclades-app-backend",
    export=True,
)

GANETI_CREATEINSTANCE_KWARGS = Default(
    default_value={
        "os": "snf-image+default",
        "hvparams": {"kvm": {"serial_console": False},
                     "xen-pvm": {},
                     "xen-hvm": {}},
        "wait_for_sync": False},
    description="This dictionary defines deployment-specific arguments to be "
        "passed to the RAPI CreateInstance call. At minimum it should contain "
        "the 'os' and 'hvparams' keys.\n\nMore specifically:\na) os:\n   The "
        "OS provider to use (this should be 'snf-image+default')\nb) "
        "hvparams:\n   Hypervisor-specific parameters for each hypervisor,\n   "
        "currently 'kvm', 'xen-pvm' and 'xen-hvm'. Also, 'serial_console' "
        "should be set to False, see #785.\nc) If using Ganeti's DRBD disk "
        "template, you may want to include\n   'wait_for_sync = FALSE', see "
        "#835.",
    category="snf-cyclades-app-backend",
    export=True,
)

GANETI_USE_HOTPLUG = Default(
    default_value=False,
    example_value=False,
    description="If True, qemu-kvm will hotplug all NICs when connecting VMs "
        "to Networks. This requires qemu-kvm>=1.0.",
    category="snf-cyclades-app-backend",
    export=True,
)

BACKEND_ALLOCATOR_MODULE = Default(
    default_value="synnefo.logic.allocators.default_allocator",
    example_value="synnefo.logic.allocators.my_allocator",
    description="Module that implements the strategy for allocating Synnefo "
        "VMs to Ganeti backends.",
    export=False,
)

BACKEND_REFRESH_MIN = Default(
    default_value=15,
    example_value=15,
    description="Maximum time in minutes, before the allocator collects new "
        "statitistics for all Ganeti backens.",
    export=False,
)
