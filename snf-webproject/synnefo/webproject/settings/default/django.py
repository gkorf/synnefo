import sys
_module = sys.modules[__name__]

from synnefo.lib.settings.setup import Default
import importlib
m = importlib.import_module('django.conf.global_settings')

settings = {}
for name in dir(m):
    settings[name] = Default(
        default_value=getattr(m, name),
        description="Django setting '%s'; see Django documentation" % name,
        export=False,
        category="snf-webproject",
        )

_module.__dict__.update(settings)
del settings
del name
del _module
