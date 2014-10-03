from synnefo.lib.settings.setup import Mandatory, Default

# Userdata configuration
########################

USERDATA_SSH_KEY_LENGTH = Default(
    default_value=2048,
    example_value=2048,
    description="Length in bits of the automatically generated SSH key.",
    export=False,
)

# NOT USED
# Generated SSH key exponent
USERDATA_SSH_KEY_EXPONENT = 65537


USERDATA_MAX_SSH_KEYS_PER_USER = Default(
    default_value=10,
    example_value=10,
    description="Maximum number of SSH keys a user is allowed to have.",
    export=False,
)

# Maximum allowed length of submitted ssh key content
USERDATA_SSH_KEY_MAX_CONTENT_LENGTH = 30000
