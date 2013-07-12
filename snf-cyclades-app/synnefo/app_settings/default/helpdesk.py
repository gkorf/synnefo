from synnefo.lib.settings.setup import Default
from synnefo.lib.settings.util import auto_configure_default_from_dep

# Helpdesk app configuration
############################

#Enable the helpdesk application
HELPDESK_ENABLED = Default(
    default_value=True,
    example_value=True,
    description="If true, enable the helpdesk application.",
    export=False,
)

HELPDESK_AUTH_COOKIE_NAME = Default(
    default_value=None,
    example_value="cookie_name_here",
    description=(
        "The cookie name that stores the token. By default it has the "
        "same value with UI_AUTH_COOKIE_NAME."),
    dependencies=['UI_AUTH_COOKIE_NAME'],
    configure_callback=auto_configure_default_from_dep,
    export=False,
)

# Astakos groups which have access to helpdesk views
HELPDESK_PERMITTED_GROUPS = Default(
    default_value=["helpdesk"],
    example_value=["helpdesk", "group1", "group2"],
    description=(
        "Astakos groups that have access to the Helpdesk application's "
        "views."),
    export=False,
)
