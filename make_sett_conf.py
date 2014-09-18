import sys
from os.path import isdir, exists

packages = [
    "snf-admin-app",
    "snf-astakos-app",
    "snf-branding",
    "snf-common",
    "snf-cyclades-app",
    "snf-cyclades-gtools",
    "snf-django-lib",
    "snf-pithos-app",
    "snf-pithos-backend",
    "snf-stats-app",
    "snf-tools",
    "snf-webproject",
]

for package in packages:
    sys.path.append(package)

defaults = {
    "synnefo_admin.app_settings.default": "snf-admin-app",
    "astakos.settings.default": "snf-astakos-app",
    "synnefo_branding.settings.default": "snf-branding",
    "synnefo.common_settings.default": "snf-common",
    "synnefo.app_settings.default": "snf-cyclades-app",
    "synnefo.ganeti.default": "snf-cyclades-gtools",
    "pithos.settings.default": "snf-pithos-app",
    "synnefo_stats.settings.default": "snf-stats-app",
    "synnefo.webproject.settings.default": "snf-webproject",
}

from synnefo.lib.settings import setup
import importlib

for mod in defaults.keys():
    m = importlib.import_module(mod)
    synnefo_settings = {}
    for name in dir(m):
        if not setup.is_valid_setting_name(name):
            continue
        synnefo_settings[name] = getattr(m, name)
    setup.initialize_settings(synnefo_settings,
                              source=m.__name__, strict=False)
setup.preconfigure_settings()

modules_dict = setup.Catalogs['modules']

settings_dict = setup.Catalogs['settings']
display_settings_list = sorted(settings_dict.iteritems())
path = "myconfs"

def f(package, display_settings_list):
        if not isdir(path):
            m = "Cannot find directory '{path}'".format(path=path)
            raise CommandError(m)

        category_depths = {}
        for name, setting in display_settings_list:
            if setting.export == False:
                continue
            key = (setting.configured_depth, setting.category)
            if key not in category_depths:
                category_depths[key] = []
            category_depths[key].append((name, setting))

        old_filepath = None
        conffile = None
        filepath = None
        for (depth, category), setting_list in \
                sorted(category_depths.iteritems()):
            depth *= 10
            filepath = '{package}/conf/{depth:02}-{category}.conf'
            filepath = filepath.format(package=package,
                                       depth=depth,
                                       category=category)
            if filepath != old_filepath:
                if conffile:
                    conffile.close()
                # if exists(filepath):
                #     m = "File {f} already exists! aborting."
                #     m = m.format(f=filepath)
                #     raise BaseException(m)
                print("Writing {f}".format(f=filepath))
                conffile = open(filepath, "w")
                old_filepath = filepath
            setting_list.sort()
            for name, setting in setting_list:
                conffile.write(setting.present_as_comment(runtime=False))
                conffile.write('\n\n')

for module, settings in modules_dict.iteritems():
    f(defaults[module], sorted(settings.iteritems()))
