from synnefo.lib.settings.setup import Mandatory, Default

CLOUDBAR_LOCATION = Mandatory(
    example_value="https://accounts.example.synnefo.org/static/im/cloudbar/",
    description="URL to find the Cloudbar contents.",
    category="snf-cyclades-app-cloudbar",
)

CLOUDBAR_SERVICES_URL = Mandatory(
    example_value="https://accounts.example.synnefo.org/ui/get_services",
    description="URL to find the Cloudbar's services content.",
    category="snf-cyclades-app-cloudbar",
)

CLOUDBAR_MENU_URL = Mandatory(
    example_value="https://accounts.example.synnefo.org/ui/get_menu",
    description="URL to find the Cloudbar's menu content.",
    category="snf-cyclades-app-cloudbar",
)

CLOUDBAR_COOKIE_NAME = Default(
    default_value="_pithos2_a",
    example_value="my_service_cookie_name_here",
    description="Name of the cloudbar service's cookie.",
    export=False,
)

CLOUDBAR_ACTIVE = Default(
    default_value=True,
    example_value=True,
    description="Enable or disable the cloudbar.",
    export=False,
)
