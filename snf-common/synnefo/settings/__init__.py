# Copyright (C) 2010-2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from sys import modules, stderr
_module = modules[__name__]

# set synnefo package __file__ to fix django related bug
import synnefo
synnefo.__file__ = os.path.join(synnefo.__path__[0], '__init__.py')

# import default settings
from synnefo.settings.default import *
from synnefo.lib.settings.setup import Setting
synnefo_settings = {}
# insert global default synnefo settings
from synnefo.lib.settings.default import *
for name in dir(_module):
    if not Setting.is_valid_setting_name(name):
        continue
    synnefo_settings[name] = getattr(_module, name)

# autodetect default settings provided by synnefo applications
from synnefo.util.entry_points import get_entry_points
for e in get_entry_points('synnefo', 'default_settings'):
    m = e.load()
    for name in dir(m):
        if name.startswith('__'):
            continue
        synnefo_settings[name] = getattr(m, name)

# set strict to True to require annotation of all settings
Setting.initialize_settings(synnefo_settings, strict=False)
_module.__dict__.update(Setting.Catalogs['defaults'])

# extend default settings with settings provided within *.conf user files
# located in directory specified in the SYNNEFO_SETTINGS_DIR
# environment variable
import re
system_conf_re = re.compile('^([0-9]\+-)?system.conf$')

SYNNEFO_SETTINGS_DIR = os.environ.get('SYNNEFO_SETTINGS_DIR', "/etc/synnefo/")
if os.path.exists(SYNNEFO_SETTINGS_DIR):
    try:
        entries = [os.path.join(SYNNEFO_SETTINGS_DIR, x) for x in
                   os.listdir(SYNNEFO_SETTINGS_DIR)]
        conffiles = [f for f in entries if os.path.isfile(f) and
                     f.endswith(".conf")]
    except Exception as e:
        print >> stderr, "Failed to list *.conf files under %s" % \
            SYNNEFO_SETTINGS_DIR
        raise SystemExit(1)
    conffiles.sort()
    for f in conffiles:
        if system_conf_re.match(f):
            allow_known = False
            allow_unknown = True
        else:
            allow_known = True
            allow_unknown = False

        # FIXME: Hack until all settings have been annotated properly
        allow_unknown = True
        allow_override = True

        try:
            path = os.path.abspath(f)
            old_settings = Setting.Catalogs['defaults']
            new_settings = Setting.load_settings_from_file(path, old_settings)

            Setting.load_configuration(new_settings,
                                       source=path,
                                       allow_known=allow_known,
                                       allow_unknown=allow_unknown,
                                       allow_override=allow_override)
        except Exception as e:
            print >> stderr, "Failed to read settings file: %s [%r]" % \
                (path, e)
            raise SystemExit(1)

Setting.configure_settings()
_module.__dict__.update(Setting.Catalogs['runtime'])

from os import environ
# The tracing code is enabled by an environmental variable and not a synnefo
# setting, on purpose, so that you can easily control whether it'll get loaded
# or not, based on context (eg enable it for gunicorn but not for eventd).
if environ.get('SYNNEFO_TRACE'):
    from synnefo.lib import trace
    trace.set_signal_trap()

# cleanup module namespace
# WARNING: this may prevent synnefo.settings to have sub-modules,
#          e.g. synnefo.settings.test
for _name in dir(_module):
    if _name.startswith('_') or _name.isupper():
        continue
    delattr(_module, _name)
del _name
del _module
