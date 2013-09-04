from synnefo.lib.settings.setup import Setting, Mandatory, Default

# Userdata configuration
########################

USERDATA_SSH_KEY_LENGTH = Default(
    default_value=2048,
    example_value=2048,
    description="Length in bits of the automatically generated SSH key.",
    export=False,
)

USERDATA_MAX_SSH_KEYS_PER_USER = Default(
    default_value=10,
    example_value=10,
    description="Maximum number of SSH keys a user is allowed to have.",
    export=False,
)
