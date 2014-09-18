import sys
import os.path

os.chdir(os.path.dirname(sys.argv[0]))

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

defaults = {}
for package in packages:
    try:
        f = open(os.path.join(package, 'default_settings.conf'))
    except:
        print "No conf for package %s" % package
        continue
    default_settings = f.readline()[:-1]
    defaults[default_settings] = package

from synnefo.lib.settings import setup
import importlib

for mod in defaults.keys():
    m = importlib.import_module(mod)
    setup.initialize_module(m)
setup.preconfigure_settings()

modules_dict = setup.Catalogs['modules']


def write_package_settings(package, display_settings_list):
        category_depths = {}
        for name, setting in display_settings_list:
            if not setting.export:
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
                print("Writing {f}".format(f=filepath))
                conffile = open(filepath, "w")
                old_filepath = filepath
            setting_list.sort()
            for name, setting in setting_list:
                conffile.write(setting.present_as_comment(runtime=False))
                conffile.write('\n\n')

for module, settings in modules_dict.iteritems():
    write_package_settings(defaults[module], sorted(settings.iteritems()))
