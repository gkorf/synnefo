# Copyright 2013 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of GRNET S.A.

from django.conf import settings
from synnefo.settings.setup import get_all_settings
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
    help = "Display synnefo settings"

    option_list = BaseCommand.option_list + (
        make_option(
            "-a", "--all",
            dest="list_all",
            action="store_true",
            default=False,
            help="List all settings"),
        make_option(
            "-d", "--defaults",
            dest="list_defaults",
            action="store_true",
            default=False,
            help="List the setting defaults only"),
        make_option(
            "-c", "--configured",
            dest="list_configured",
            action="store_true",
            default=False,
            help="List only default settings that were changed"),
    )

    def handle(self, *args, **options):
        if args:
            raise CommandError("This command takes no arguments. Only options")

        list_all = options["list_all"]
        list_defaults = options["list_defaults"]
        list_configured = options["list_configured"]

        summ = list_all + list_defaults + list_configured
        if summ == 0:
            # no options
            list_configured = True
        elif summ > 1:
            raise CommandError("Only one option can be specified at a time")

        configured = settings._CONFIGURED
        defaults = settings._DEFAULTS
        mandatory = settings._MANDATORY

        if list_all:
            for name, value in sorted(get_all_settings(settings)):
                line = "%s = %r" % (name, value)
                if name in defaults:
                    line += " -- def. "
                    if name in configured:
                        line += repr(defaults[name].default_value)
                print line

        elif list_defaults:
            for name, value in sorted(defaults.items()):
                print "%s = %r -- def." % (name, value.default_value)
        elif list_configured:
            names = mandatory.keys()
            names.sort()
            for name in names:
                line = "%s = %r" % (name, getattr(settings, name))
                line += ' -- ex. ' + repr(mandatory[name].example_value)
                print line

            print " "

            names = configured.keys()
            names.sort()
            for name in names:
                line = "%s = %r" % (name, getattr(settings, name))
                line += " -- def. " + repr(defaults[name].default_value)
                print line
        else:
            raise AssertionError()
