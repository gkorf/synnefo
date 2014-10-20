from synnefo.lib.settings.setup import NoValue, Default, Auto
import datetime

# Branding configuration
########################

#
# Service and Company names/urls
#

BRANDING_SERVICE_NAME = Default(
    default_value="Synnefo",
    example_value="My Cloud Service",
    description=(
        "Brand name of the cloud service. This will appear on the "
        "Synnefo UI and emails."),
    category="snf-branding-settings",
    export=True,
)

BRANDING_COMPANY_NAME = Default(
    default_value="GRNET",
    example_value="My Company name",
    description=(
        "The name of the company behind the service. This will appear "
        "on the UI's footer message, if enabled, and will be included in the "
        "emails sent by the service."),
    category="snf-branding-settings",
    export=True,
)

BRANDING_COMPANY_URL = Default(
    default_value="http://www.grnet.gr/en/",
    example_value="http://my.company.com",
    description=(
        "The company's official site URL. This is used on the UI "
        "footer's Copyright message, if enabled."),
    category="snf-branding-settings",
    export=True,
)

#
# Image configuration
#


def _auto_configure_branding_image_media_url(deps):
    return deps['MEDIA_URL'] + "branding/images/"


def auto_configure_append_value(value):
    def auto_configure_append(deps):
        return deps.values()[0] + value
    return auto_configure_append

BRANDING_IMAGE_MEDIA_URL = Auto(
    description=(
        "The default path to the folder that contains all branding images. "),
    category="snf-branding-settings",
    export=True,
    dependencies=["MEDIA_URL"],
    autoconfigure=_auto_configure_branding_image_media_url,
)

BRANDING_FAVICON_URL = Auto(
    description=(
        "The service's favicon that will appear on the browser's "
        "address bar."),
    dependencies=['BRANDING_IMAGE_MEDIA_URL'],
    category="snf-branding-settings",
    export=True,
    autoconfigure=auto_configure_append_value("favicon.ico"),
)

BRANDING_DASHBOARD_LOGO_URL = Auto(
    description=(
        "The service logo that appears on all Dashboard (Astakos) pages."),
    dependencies=['BRANDING_IMAGE_MEDIA_URL'],
    category="snf-branding-settings",
    export=True,
    autoconfigure=auto_configure_append_value("dashboard_logo.png"),
)

BRANDING_COMPUTE_LOGO_URL = Auto(
    description=(
        "The service logo that appears on all Compute and Network "
        "(Cyclades) pages."),
    dependencies=['BRANDING_IMAGE_MEDIA_URL'],
    category="snf-branding-settings",
    export=True,
    autoconfigure=auto_configure_append_value("compute_logo.png"),
)

BRANDING_CONSOLE_LOGO_URL = Auto(
    description=(
        "The service logo that appears on the VM Console page "
        "(in Cyclades)."),
    dependencies=['BRANDING_IMAGE_MEDIA_URL'],
    category="snf-branding-settings",
    export=True,
    autoconfigure=auto_configure_append_value("console_logo.png"),
)

BRANDING_STORAGE_LOGO_URL = Auto(
    description=(
        "The service logo that appears on all Storage (Pithos) pages."),
    dependencies=['BRANDING_IMAGE_MEDIA_URL'],
    category="snf-branding-settings",
    export=True,
    autoconfigure=auto_configure_append_value("storage_logo.png"),
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


def _auto_configure_copyright_message(deps):
    # Auto-configure a default one
    copyright_period_default = "2011-%s" % (datetime.datetime.now().year)
    copyright_message_default = "Copyright (c) %s %s" % (
        copyright_period_default, deps['BRANDING_COMPANY_NAME'])
    return copyright_message_default


BRANDING_COPYRIGHT_MESSAGE = Auto(
    description=(
        "The copyright message that will appear in the UI's footer. "
        "Defaults to 'Copyright (c) 2011-<now> <BRANDING_COMPANY_NAME>'"),
    dependencies=['BRANDING_SHOW_COPYRIGHT', 'BRANDING_COMPANY_NAME'],
    category="snf-branding-settings",
    export=True,
    autoconfigure=_auto_configure_copyright_message,
)
