from synnefo.lib.settings.setup import NoValue, Default, Auto


def configure_vmapi_cache_b(deps):
    return deps["CACHE_BACKEND"]

CACHE_BACKEND = Default(
    default_value='locmem://',
    example_value='locmem://',
    description="cache backend",
    category="snf-cyclades-app-api",
    export=True,
)


VMAPI_CACHE_BACKEND = Auto(
    description="VMAPI cache backend",
    dependencies=["CACHE_BACKEND"],
    category="snf-cyclades-app-vmapi",
    autoconfigure=configure_vmapi_cache_b,
    export=True,
)
