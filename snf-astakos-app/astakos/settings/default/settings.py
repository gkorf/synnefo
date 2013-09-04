from synnefo.lib.settings.setup import (Setting, Default, Auto,
                                        Mandatory, SubMandatory)
from synnefo.lib.settings.default import (mk_auto_configure_base_host,
                                          mk_auto_configure_base_path,
                                          mk_auto_configure_services)

#
# Astakos configuration
#

ASTAKOS_BASE_URL = Mandatory(
    example_value="https://accounts.example.synnefo.org/astakos/",
    description=(
        "The complete URL which is forwarded by the front-end web server "
        "to the Astakos application server (gunicorn). "),
    category="snf-astakos-app-settings",
)

ASTAKOS_BASE_HOST = Auto(
    configure_callback=mk_auto_configure_base_host("ASTAKOS_BASE_URL"),
    export=False,
    description="The host part of ASTAKOS_BASE_URL. Cannot be configured.",
    dependencies=["ASTAKOS_BASE_URL"],
)

ASTAKOS_BASE_PATH = Auto(
    configure_callback=mk_auto_configure_base_path("ASTAKOS_BASE_URL"),
    export=False,
    description="The path part of ASTAKOS_BASE_URL. Cannot be configured.",
    dependencies=["ASTAKOS_BASE_URL"],
)

ASTAKOS_SERVICES = Auto(
    configure_callback=mk_auto_configure_services("astakos",
                                                  "ASTAKOS_BASE_URL"),
    description="Definition of services provided by the Astakos component",
    export=False,
    dependencies=["ASTAKOS_BASE_URL", "SYNNEFO_COMPONENTS"],
)

ASTAKOS_AUTH_TOKEN_DURATION = Default(
    default_value=30*24,
    description=(
        "Expiration time for newly created authentication tokens. "
        "Time is counted in hours."),
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_IM_MODULES = Default(
    default_value=["local"],
    example_value=["local", "twitter", "google", "linkedin", "shibboleth"],
    description="Identity management enabled methods.",
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_COOKIE_DOMAIN = Mandatory(
    example_value=".example.synnefo.org",
    description=(
        "The domain at which the Astakos authentication cookie will be "
        "published. Warning: all websites under this domain can access the "
        "and its secret authorization data."),
    category="snf-astakos-app-settings",
)

ASTAKOS_COOKIE_NAME = Default(
    default_value="_pithos2_a",
    example_value="my_service_cookie_name_here",
    description="The astakos cookie name.",
    export=False,
)

ASTAKOS_COOKIE_SECURE = Default(
    default_value=True,
    description=(
        "Whether to require an encrypted connection to transmit the cookie."),
    export=False,
)

#
# User moderation configuration
#

ASTAKOS_MODERATION_ENABLED = Default(
    default_value=True,
    description=(
        "Whether to moderate newly created users. If set to False all "
        "users that have signed up and verified their email address will get "
        "automatically accepted/activated. "),
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_RE_USER_EMAIL_PATTERNS = Default(
    default_value=[],
    description=(
        "If a new user's email matches any regex in this list, the "
        "user will get automatically accepted/activated."),
    dependencies=['ASTAKOS_MODERATION_ENABLED'],
    category="snf-astakos-app-settings",
    export=True,
)

#
# reCAPTCHA configuration
#

ASTAKOS_RECAPTCHA_ENABLED = Default(
    default_value=False,
    description="Whether to enable reCAPTCHA during sign up. ",
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_RECAPTCHA_PUBLIC_KEY = SubMandatory(
    example_value="recaptcha_public_key_here",
    description="The reCAPTCHA public key.",
    dependencies=['ASTAKOS_RECAPTCHA_ENABLED'],
)

ASTAKOS_RECAPTCHA_PRIVATE_KEY = SubMandatory(
    example_value="recaptcha_private_key_here",
    description="The reCAPTCHA private key.",
    dependencies=['ASTAKOS_RECAPTCHA_ENABLED'],
)

ASTAKOS_RECAPTCHA_OPTIONS = Default(
    default_value={
        "theme": "custom",
        "custom_theme_widget": "okeanos_recaptcha"
    },
    description=(
        "Additional reCAPTCHA options. "
        "We define a custom theme here. "),
    dependencies=['ASTAKOS_RECAPTCHA_ENABLED'],
    export=False,
)

ASTAKOS_RECAPTCHA_USE_SSL = Default(
    default_value=True,
    description="Whether to use SSL.",
    dependencies=['ASTAKOS_RECAPTCHA_ENABLED'],
    export=False,
)

#
# UI messages configuration
#

ASTAKOS_LOGIN_MESSAGES = Default(
    default_value=[],
    example_value=[{
        "warning": "This will be displayed on the top of the login page. "
    }],
    description=(
        "Type and body of the message to get displayed on the login "
        "page header. Types are color coded on the UI, valid keys are: "
        "'warning', 'success', 'error', 'info'"),
    export=False,
)

ASTAKOS_SIGNUP_MESSAGES = Default(
    default_value=[],
    example_value=[{
        "warning": "This will be displayed on the top of the signup page. "
    }],
    description=(
        "Type and body of the message to get displayed on the signup "
        "page header. Types are color coded on the UI, valid keys are: "
        "'warning', 'success', 'error', 'info'"),
    export=False,
)

ASTAKOS_PROFILE_MESSAGES = Default(
    default_value=[],
    example_value=[{
        "warning": "This will be displayed on the top of the profile page. "
    }],
    description=(
        "Type and body of the message to get displayed on the profile "
        "page header. Types are color coded on the UI, valid keys are: "
        "'warning', 'success', 'error', 'info'"),
    export=False,
)

ASTAKOS_GLOBAL_MESSAGES = Default(
    default_value=[],
    example_value=[{
        "warning": "This will be displayed on the top of every page. "
    }],
    description=(
        "Type and body of the message to get displayed on every "
        "page header. Types are color coded on the UI, valid keys are: "
        "'warning', 'success', 'error', 'info'"),
    export=False,
)

ASTAKOS_PROFILE_EXTRA_LINKS = Default(
    default_value={},
    example_value={
        "https://landingpage.example.synnefo.org": "Back to <service_name>"
    },
    description="Additional link to get displayed on the profile page.",
    export=False,
)

#
# Email change/verify configuration
#

ASTAKOS_EMAILCHANGE_ENABLED = Default(
    default_value=False,
    description=(
        "Whether the user can change his/her email on the profile page. "),
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_EMAILCHANGE_ACTIVATION_DAYS = Default(
    default_value=10,
    description=(
        "Expiration time in days of email change requests. The user "
        "should verify his/her new email inside this period for it to switch "
        "to the new value."),
    dependencies=['ASTAKOS_EMAILCHANGE_ENABLED'],
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_SKIP_EMAIL_VERIFICATION = Default(
    default_value=False,
    description=(
        "If False, Astakos will verify the email of a newly created "
        "user, by sending him/her a verification email which will contain a "
        "verification URL."),
    export=False,
)

#
# UI pagination configuration
#

ASTAKOS_PAGINATE_BY = Default(
    default_value=50,
    description="How many objects should be displayed per page.",
    export=False,
)

ASTAKOS_PAGINATE_BY_ALL = Default(
    default_value=50,
    description=(
        "How many objects should be displayed per page in the "
        "'show all' projects' page."),
    export=False,
)

#
# Projects configuration
#

ASTAKOS_PROJECTS_VISIBLE = Default(
    default_value=False,
    description="Whether to show Projects under the Astakos menu on the UI. ",
    category="snf-astakos-app-settings",
    export=True,
)

ASTAKOS_PROJECT_ADMINS = Default(
    default_value=[],
    description=(
        "Users that can approve or deny project applications. List of "
        "user UUIDs."),
    category="snf-astakos-app-settings",
    export=True,
)

#
# Auth methods configuration
#

ASTAKOS_SHIBBOLETH_REQUIRE_NAME_INFO = Default(
    default_value=False,
    description=(
        "If True, require shibboleth IdP's to provide attributes that "
        "contain account name information. If no such attributes provided, "
        "users of that IdP won't be able to use their shibboleth credentials "
        "to create or login to their astakos account."),
    export=False,
)

# FIXME: Mandatory with condition
ASTAKOS_TWITTER_TOKEN = Default(
    default_value="",
    description="OAuth2 twitter token.",
    category="snf-astakos-app-authmethods",
    export=True,
)

# FIXME: Mandatory with condition
ASTAKOS_TWITTER_SECRET = Default(
    default_value="",
    description="0Auth2 twitter secret.",
    category="snf-astakos-app-authmethods",
    export=True,
)

ASTAKOS_TWITTER_AUTH_FORCE_LOGIN = Default(
    default_value=False,
    description=(
        "If True, prevent Twitter automatic authentication for users who "
        "try to login using their Twitter account. This means that Twitter "
        "will always prompt users to login to their account even if an "
        "existing Twitter session exists."),
    export=False,
)

# FIXME: Mandatory with condition
ASTAKOS_GOOGLE_CLIENT_ID = Default(
    default_value="",
    description="OAuth google client id.",
    category="snf-astakos-app-authmethods",
    export=True,
)

# FIXME: Mandatory with condition
ASTAKOS_GOOGLE_SECRET = Default(
    default_value="",
    description="OAuth google sercret.",
    category="snf-astakos-app-authmethods",
    export=True,
)

# FIXME: Mandatory with condition
ASTAKOS_LINKEDIN_TOKEN = Default(
    default_value="",
    description="OAuth linkedin token.",
    category="snf-astakos-app-authmethods",
    export=True,
)

# FIXME: Mandatory with condition
ASTAKOS_LINKEDIN_SECRET = Default(
    default_value="",
    description="OAuth linkedin secret.",
    category="snf-astakos-app-authmethods",
    export=True,
)

#
# UI presentation configuration
#

ASTAKOS_COMPONENTS_META = Default(
    default_value={},
    example_value={
        "synnefo": {
            "url": "http://example.synnefo.org",
            "order": 1,
            "dashboard": {
                "order": 4,
                "show": True,
                "description": 'Synnefo homepage',
                "icon": "/static/branding/images/synnefo-logo.png"
            },
            "cloudbar": {
                "show": True,
                "icon": "https://example.synnefo.org/static/branding/images/cloudbar_home.png"
            }
        },
        "cyclades": {
            "order": 2,
            "dashboard": {
                "order": 1,
                },
        },
        "pithos": {
            "order": 3,
            "dashboard": {
                "order": 2,
            },
        }
    },
    description=(
        "A way to extend the components presentation metadata on the UI."),
    export=False,
)

ASTAKOS_RESOURCES_META = Default(
    default_value={},
    description=(
        "A way to extend the services presentation metadata on the UI."),
    export=False,
)

#
# API access page links
#

ASTAKOS_API_CLIENT_URL = Default(
    default_value="https://pypi.python.org/pypi/kamaki",
    description=(
        "URL to the official kamaki package. Displayed in the API "
        "access tab."),
    export=False,
)

ASTAKOS_KAMAKI_CONFIG_CLOUD_NAME = Default(
    default_value=None,
    description=(
        "Override the cloud name in the suggested downloadable "
        "'.kamakirc' in the API access tab."),
    export=False,
)

#
# Misc configuration
#

ASTAKOS_RATELIMIT_RETRIES_ALLOWED = Default(
    default_value=3,
    description=(
        "The number of unsuccessful login requests per minute a user "
        "can issue."),
    export=False,
)

ASTAKOS_NEWPASSWD_INVALIDATE_TOKEN = Default(
    default_value=True,
    description="Enforce token renewal on password change/reset.",
    export=False,
)

ASTAKOS_USAGE_UPDATE_INTERVAL = Default(
    default_value=5000,
    description=(
        "Refresh the user's available quota in the Usage tab every "
        "that many milliseconds."),
    export=False,
)


ASTAKOS_REDIRECT_ALLOWED_SCHEMES = Default(
    default_value=("pithos", "pithosdev"),
    description=(
        "Allowed schemes to be passed at the 'next' parameter during "
        "Astakos redirects."),
    export=False,
)

ASTAKOS_LOGOUT_NEXT = Default(
    default_value="",
    example_value="http://landingpage.example.synnefo.org/welcome",
    description="URL that the user will get redirected to after logging out. ",
    export=False,
)


def _auto_configure_im_static_url(setting, value, deps):
    if value is not Setting.NoValue:
        # acknowledge user-provided setting
        return Setting.NoValue
    # User did not provide setting, create one out of MEDIA_URL
    value = deps['MEDIA_URL'].rstrip('/') + "/im/"
    return value


ASTAKOS_IM_STATIC_URL = Default(
    default_value=None,
    description="Base URL for Astakos static files.",
    configure_callback=_auto_configure_im_static_url,
    dependencies=['MEDIA_URL'],
    export=False,
)

#
# FIXME: Document the following
#

# The following settings will replace the default django settings
AUTHENTICATION_BACKENDS = (
    'astakos.im.auth_backends.EmailBackend',
    'astakos.im.auth_backends.TokenBackend')

CUSTOM_USER_MODEL = 'astakos.im.AstakosUser'

#SOUTH_TESTS_MIGRATE = False

BROKER_URL = ''

# INTERNAL_IPS = ('127.0.0.1',)


#
# Obsolete settings
#

# FIXME: Invitations mechanism will be re-written if needed. Those have to go
# for now along with the relevant code.
ASTAKOS_INVITATIONS_ENABLED = Default(
    default_value=False,
    description="Whether to enable the invitations mechanism.",
    export=False,
)

ASTAKOS_DEFAULT_USER_LEVEL = Default(
    default_value=4,
    description="The user's default invitation level.",
    export=False,
)

ASTAKOS_INVITATIONS_PER_LEVEL = Default(
    default_value={
        0: 100,
        1: 2,
        2: 0,
        3: 0,
        4: 0
    },
    description=(
        "Dict that maps how many are the available invitations for "
        "each invitation level. "),
    export=False,
)

# FIXME: This is not needed any more, has to go along with relevant code.
ASTAKOS_FORCE_PROFILE_UPDATE = Default(
    default_value=False,
    description=(
        "Force the user to update his/her profile page on the first "
        "successful login."),
    export=False,
)

# FIXME: This was needed for transitional reasons, now needs to go away along
# with the corresponding code.
# This enables a ui compatibility layer for the introduction of UUIDs in
# identity management.  WARNING: Setting to True will break your installation.
ASTAKOS_TRANSLATE_UUIDS = Default(
    default_value=False,
    description="Transitional setting to allow UUID translations.",
    export=False,
)
