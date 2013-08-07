from django.conf import settings
from synnefo.util.version import get_component_version
import datetime

SERVICE_NAME = settings.BRANDING_SERVICE_NAME
COMPANY_NAME = settings.BRANDING_COMPANY_NAME
COMPANY_URL = settings.BRANDING_COMPANY_URL

IMAGE_MEDIA_URL = settings.BRANDING_IMAGE_MEDIA_URL
FAVICON_URL = settings.BRANDING_FAVICON_URL
DASHBOARD_LOGO_URL = settings.BRANDING_DASHBOARD_LOGO_URL
COMPUTE_LOGO_URL = settings.BRANDING_COMPUTE_LOGO_URL
CONSOLE_LOGO_URL = settings.BRANDING_CONSOLE_LOGO_URL

## Images
######################

# The default path to the folder that contains all branding images
IMAGE_MEDIA_URL = getattr(settings, 'BRANDING_IMAGE_MEDIA_URL',
                          settings.MEDIA_URL+'branding/images/')

# The service favicon
FAVICON_URL = getattr(settings, 'BRANDING_FAVICON_URL',
                      IMAGE_MEDIA_URL+'favicon.ico')
# Logo used in Dashboard pages (Astakos)
DASHBOARD_LOGO_URL = getattr(settings, 'BRANDING_DASHBOARD_LOGO_URL',
                             IMAGE_MEDIA_URL+'dashboard_logo.png')
# Logo used in Compute pages (Cyclades)
COMPUTE_LOGO_URL = getattr(settings, 'BRANDING_COMPUTE_LOGO_URL',
                           IMAGE_MEDIA_URL+'compute_logo.png')
# Logo used in Console page for VM (Cyclades)
CONSOLE_LOGO_URL = getattr(settings, 'BRANDING_CONSOLE_LOGO_URL',
                           IMAGE_MEDIA_URL+'console_logo.png')
# Logo used in Storage pages (Pithos)
STORAGE_LOGO_URL = getattr(settings, 'BRANDING_STORAGE_LOGO_URL',
                           IMAGE_MEDIA_URL+'storage_logo.png')

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
