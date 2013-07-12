from synnefo.settings.setup import Setting, Mandatory, Default, Constant

ASTAKOS_COOKIE_DOMAIN = Mandatory(
    example_value=".example.synnefo.org",
    description=(
        "The domain at which the astakos authentication cookie will be "
        "published. Warning: all websites under this domain can access the "
        "cookie and its secret authorization data."),
    category="misc",
)

ASTAKOS_COOKIE_NAME = Constant(
    default_value='_pithos2_a',
    description="The astakos cookie name.",
)

ASTAKOS_COOKIE_SECURE = Constant(
    default_value=True,
    description=("Whether to require an encrypted connection "
                 "to transmit the cookie."),
)

# The following settings will replace the default django settings
AUTHENTICATION_BACKENDS = (
    'astakos.im.auth_backends.EmailBackend',
    'astakos.im.auth_backends.TokenBackend')

CUSTOM_USER_MODEL = 'astakos.im.AstakosUser'

#SOUTH_TESTS_MIGRATE = False

BROKER_URL = ''

# INTERNAL_IPS = ('127.0.0.1',)
