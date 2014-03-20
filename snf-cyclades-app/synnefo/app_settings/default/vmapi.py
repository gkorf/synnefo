from synnefo.lib.settings.setup import Setting, Default, Auto


def configure_vmapi_cache_b(setting, value, deps):
    if value is not Setting.NoValue:
        return Setting.NoValue
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
    configure_callback=configure_vmapi_cache_b,
    export=True,
)
