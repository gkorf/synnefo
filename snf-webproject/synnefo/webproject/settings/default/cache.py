from synnefo.lib.settings.setup import Default

CACHE_BACKEND = Default(
    default_value='locmem://',
    example_value='locmem://',
    description="cache backend",
    category="snf-cyclades-app-api",
)
