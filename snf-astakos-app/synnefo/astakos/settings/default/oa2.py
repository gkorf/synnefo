from synnefo.lib.settings.setup import Default

OAUTH2_USER_MODEL = Default(
    default_value="auth.User",
    description="Oath2 user model",
    category="snf-astakos-oa2",
    export=False,
)

OAUTH2_ENDPOINT_PREFIX = Default(
    default_value="oauth2/",
    description="Oauth2 Endpoint prefix",
    category="snf-astakos-oa2",
)

OAUTH2_TOKEN_ENDPOINT = Default(
    default_value="token/",
    description="Oauth2 token endpoint",
    category="snf-astakos-oa2",
)

OAUTH2_AUTHORIZATION_ENDPOINT = Default(
    default_value="auth/",
    description="Oauth2 authorization endpoint",
    category="snf-astakos-oa2",
)

OAUTH2_AUTHORIZATION_CODE_LENGTH = Default(
    default_value=60,
    description="Set the length of newly created authorization codes.",
    category="snf-astakos-oa2",
)

OAUTH2_TOKEN_LENGTH = Default(
    default_value=30,
    description="Set the length of newly created access tokens.",
    category="snf-astakos-oa2",
)

OAUTH2_TOKEN_EXPIRES = Default(
    default_value=20,
    description="Set the expiration time of newly created access tokens.",
    category="snf-astakos-oa2",
)

OAUTH2_MAXIMUM_ALLOWED_REDIRECT_URI_LENGTH = Default(
    default_value=5000,
    description="Set the maximum allowed redirection endpoint URI length.",
    category="snf-astakos-oa2",
)
