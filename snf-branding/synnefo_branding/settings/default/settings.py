from synnefo.settings.setup import Setting, Default
import datetime

# Branding configuration
########################

#
# Service and Company names/urls
#

BRANDING_SERVICE_NAME = Default(
    default_value="Synnefo",
    example_value="My Cloud Service",
    description="Brand name of the cloud service. This will appear on the "
        "Synnefo UI and emails.",
    category="snf-branding-settings",
    export=True,
)

BRANDING_COMPANY_NAME = Default(
    default_value="GRNET",
    example_value="My Company name",
    description="The name of the company behind the service. This will appear "
        "on the UI's footer message, if enabled, and will be included in the "
        "emails sent by the service.",
    category="snf-branding-settings",
    export=True,
)

BRANDING_COMPANY_URL = Default(
    default_value="http://www.grnet.gr/en/",
    example_value="http://my.company.com",
    description="The company's official site URL. This is used on the UI "
        "footer's Copyright message, if enabled.",
    category="snf-branding-settings",
    export=True,
)

#
# Image configuration
#

BRANDING_IMAGE_MEDIA_URL = Default(
    default_value=MEDIA_URL + "branding/images/",
    description="The default path to the folder that contains all branding "
        "images. ",
    dependencies=[MEDIA_URL],
    category="snf-branding-settings",
    export=True,
)

BRANDING_FAVICON_URL = Default(
    deault_value=BRANDING_IMAGE_MEDIA_URL + "favicon.ico",
    description="The service's favicon that will appear on the browser's "
        "address bar.",
    dependencies=[BRANDING_IMAGE_MEDIA_URL],
    category="snf-branding-settings",
    export=True,
)

BRANDING_DASHBOARD_LOGO_URL = Default(
    deault_value=BRANDING_IMAGE_MEDIA_URL + "dashboard_logo.png",
    description="The service logo that appears on all Dashboard (Astakos) "
        "pages.",
    dependencies=[BRANDING_IMAGE_MEDIA_URL],
    category="snf-branding-settings",
    export=True,
)

BRANDING_COMPUTE_LOGO_URL = Default(
    deault_value=BRANDING_IMAGE_MEDIA_URL + "compute_logo.png",
    description="The service logo that appears on all Compute and Network "
        "(Cyclades) pages.",
    dependencies=[BRANDING_IMAGE_MEDIA_URL],
    category="snf-branding-settings",
    export=True,
)

BRANDING_CONSOLE_LOGO_URL = Default(
    deault_value=BRANDING_IMAGE_MEDIA_URL + "console_logo.png",
    description="The service logo that appears on the VM Console page "
        "(in Cyclades).",
    dependencies=[BRANDING_IMAGE_MEDIA_URL],
    category="snf-branding-settings",
    export=True,
)

BRANDING_STORAGE_LOGO_URL = Default(
    deault_value=BRANDING_IMAGE_MEDIA_URL + "storage_logo.png",
    description="The service logo that appears on all Storage (Pithos) "
        "pages.",
    dependencies=[BRANDING_IMAGE_MEDIA_URL],
    category="snf-branding-settings",
    export=True,
)

#
# Copyright configuration
#

BRANDING_SHOW_COPYRIGHT = Default(
    default_value=False,
    description="Whether to show a Copyright message in the UI's footer. ",
    category="snf-branding-settings",
    export=True,
)

copyright_period_default = "2011-%s" % (datetime.datetime.now().year)
copyright_message_default = \
    "Copyright (c) %s %s" % (copyright_period_default, BRANDING_COMPANY_NAME)

BRANDING_COPYRIGHT_MESSAGE = Default(
    default_value=copyright_message_default,
    description="The copyright message that will appear in the UI's footer. "
        "Defaults to 'Copyright (c) 2011-<now> <BRANDING_COMPANY_NAME>'",
    dependencies=[BRANDING_SHOW_COPYRIGHT],
    category="snf-branding-settings",
    export=True,
)
