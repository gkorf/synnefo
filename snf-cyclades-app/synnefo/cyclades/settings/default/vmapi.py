from synnefo.lib.settings.setup import Default, Auto
from synnefo.lib.settings.util import auto_configure_default_from_dep

VMAPI_CACHE_BACKEND = Auto(
    description="VMAPI cache backend",
    dependencies=["CACHE_BACKEND"],
    category="snf-cyclades-app-vmapi",
    autoconfigure=auto_configure_default_from_dep,
    export=True,
)

VMAPI_CACHE_KEY_PREFIX = Default(
    default_value="vmapi",
    description="VMAPI cache key prefix",
    category="snf-cyclades-app-vmapi",
)

VMAPI_RESET_PARAMS = Default(
    default_value=True,
    description="VMAPI reset params",
    category="snf-cyclades-app-vmapi",
)

VMAPI_BASE_HOST = Auto(
    description="Vmapi base host",
    category="snf-cyclades-app-vmapi",
    dependencies=["CYCLADES_BASE_HOST"],
    autoconfigure=auto_configure_default_from_dep,
)
