# Copyright 2011-2013 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.

import os
from sys import modules, stderr
_module = modules[__name__]

# set synnefo package __file__ to fix django related bug
import synnefo
synnefo.__file__ = os.path.join(synnefo.__path__[0], '__init__.py')

# import default settings
from synnefo.settings.default import *
from .setup import Setting
synnefo_settings = {}
# insert global default synnefo settings
from .default import *
for name in dir(_module):
    if not Setting.is_valid_setting_name(name):
        continue
    synnefo_settings[name] = getattr(_module, name)

# autodetect default settings provided by synnefo applications
from synnefo.util.entry_points import get_entry_points
for e in get_entry_points('synnefo', 'default_settings'):
    m = e.load()
    print "loading", m
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
for _name in dir(_module):
    if _name.startswith('_') or _name.isupper():
        continue
    delattr(_module, _name)
del _name
del _module
