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

"""
Extented django management module

Most of the code is shared from django.core.management module
to allow us extend the default django ManagementUtility object
used to provide command line interface of the django project
included in snf-webproject package.

The extended class provides the following:

- additional argument for the configuration of the SYNNEFO_SETTINGS_DIR
  environmental variable (--settings-dir).
- a fix for management utility to handle custom commands defined in
  applications living in namespaced packages (django ticket #14087)
- override of --version command to display the snf-webproject version
"""

from django.core import management
from synnefo.util.version import get_component_version
from synnefo.lib.dictconfig import dictConfig
from synnefo.lib.settings.setup import SettingsError

import sys
import locale
import os
import imp


def find_modules(name, path=None):
    """Find all modules with name 'name'

    Unlike find_module in the imp package this returns a list of all
    matched modules.
    """

    results = []
    if path is None:
        path = sys.path
    for p in path:
        importer = sys.path_importer_cache.get(p, None)
        if importer is None:
            find_module = imp.find_module
        else:
            find_module = importer.find_module

        try:
            result = find_module(name, [p])
            if result is not None:
                results.append(result)
        except ImportError:
            if sys.modules.get(name, None):
                modpath = sys.modules[name].__path__
                if isinstance(modpath, basestring) \
                   and not ('', modpath) in results:
                    results.append(('', sys.modules[name].__path__))
                else:
                    for mp in modpath:
                        if not ('', mp) in results:
                            results.append(('', mp))
            pass

    if not results:
        raise ImportError("No module named %.200s" % name)

    return results


def find_management_module(app_name):
    """
    Determines the path to the management module for the given app_name,
    without actually importing the application or the management module.

    Raises ImportError if the management module cannot be found for any reason.
    """
    parts = app_name.split('.')
    parts.append('management')
    parts.reverse()
    part = parts.pop()
    paths = None

    # When using manage.py, the project module is added to the path,
    # loaded, then removed from the path. This means that
    # testproject.testapp.models can be loaded in future, even if
    # testproject isn't in the path. When looking for the management
    # module, we need look for the case where the project name is part
    # of the app_name but the project directory itself isn't on the path.
    try:
        modules = find_modules(part, paths)
        paths = [m[1] for m in modules]
    except ImportError:
        if os.path.basename(os.getcwd()) != part:
            raise

    while parts:
        part = parts.pop()
        modules = find_modules(part, paths)
        paths = [m[1] for m in modules]
    return paths[0]


def configure_logging(settings):
    try:
        dictConfig(settings.SNF_MANAGE_LOGGING_SETUP)
    except AttributeError:
        import logging
        logging.basicConfig()
        log = logging.getLogger()
        log.warning("SNF_MANAGE_LOGGING_SETUP setting missing.")


class EncodedStream(object):
    def __init__(self, stream):
        try:
            std_encoding = stream.encoding
        except AttributeError:
            std_encoding = None
        self.encoding = std_encoding or locale.getpreferredencoding()
        self.original_stream = stream

    def write(self, string):
        if isinstance(string, unicode):
            string = string.encode(self.encoding, errors="replace")
        self.original_stream.write(string)

    def __getattr__(self, name):
        return getattr(self.original_stream, name)


class SynnefoManagementUtility(management.ManagementUtility):
    def __init__(self, argv=None):
        # Monkey patch module detection and version printing
        management.find_management_module = find_management_module
        management.get_version = get_component_version
        super(SynnefoManagementUtility, self).__init__(argv=argv)
        self.patch_streams()

    def patch_streams(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # Encode stdout. This check is required because of the way python
        # checks if something is tty:
        # https://bugzilla.redhat.com/show_bug.cgi?id=841152
        if subcommand not in ['test'] and 'shell' not in subcommand:
            sys.stdout = EncodedStream(sys.stdout)
            sys.stderr = EncodedStream(sys.stderr)

    def main_help_text(self):
        usage = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." %
            self.prog_name,
            "",
            "Available subcommands:",
            ]
        commands = sorted(management.get_commands().keys())
        usage += commands
        return '\n'.join(usage)


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = \
        os.environ.get('DJANGO_SETTINGS_MODULE', 'synnefo.settings')
    from django.conf import settings
    try:
        # Force the evaluation of settings to early detect errors.
        settings.DEBUG
    except SettingsError as e:
        print >> sys.stderr, e
        exit()
    configure_logging(settings)
    mu = SynnefoManagementUtility(sys.argv)
    mu.execute()

if __name__ == "__main__":
    main()
