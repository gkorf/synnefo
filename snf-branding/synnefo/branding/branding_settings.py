from synnefo import settings
from synnefo.util.version import get_component_version
import datetime

SERVICE_NAME = settings.BRANDING_SERVICE_NAME
SERVICE_URL = getattr(settings, 'BRANDING_SERVICE_URL',
                      'http://www.synnefo.org/')
COMPANY_NAME = settings.BRANDING_COMPANY_NAME
COMPANY_URL = settings.BRANDING_COMPANY_URL

IMAGE_MEDIA_URL = settings.BRANDING_IMAGE_MEDIA_URL
FAVICON_URL = settings.BRANDING_FAVICON_URL
DASHBOARD_LOGO_URL = settings.BRANDING_DASHBOARD_LOGO_URL
COMPUTE_LOGO_URL = settings.BRANDING_COMPUTE_LOGO_URL
CONSOLE_LOGO_URL = settings.BRANDING_CONSOLE_LOGO_URL
STORAGE_LOGO_URL = settings.BRANDING_STORAGE_LOGO_URL


## Copyright and footer options
######################

copyright_period_default = '2011-%s' % (datetime.datetime.now().year)
copyright_message_default = 'Copyright (c) %s %s' % (copyright_period_default,
                                                     COMPANY_NAME)
SHOW_COPYRIGHT = settings.BRANDING_SHOW_COPYRIGHT
COPYRIGHT_MESSAGE = settings.BRANDING_COPYRIGHT_MESSAGE

SYNNEFO_VERSION = get_component_version('common')

# Footer message appears above Copyright message at the Compute templates
# and the Dashboard UI. Accepts html tags
FOOTER_EXTRA_MESSAGE = getattr(settings, 'BRANDING_FOOTER_EXTRA_MESSAGE', '')

# The location of the css files that contain the font loading css code
FONTS_CSS_URLS = getattr(settings, 'BRANDING_FONTS_CSS_URLS', [
    '//fonts.googleapis.com/css?family=Open+Sans&subset=latin,greek-ext,greek',
    '//fonts.googleapis.com/css?family=Ubuntu&subset=latin,greek'
])
