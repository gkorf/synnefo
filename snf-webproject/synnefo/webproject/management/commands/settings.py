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

from synnefo.settings.setup import Setting
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from os.path import isdir
from pprint import pformat
from textwrap import wrap

NoValue = Setting.NoValue
available_categories = sorted(Setting.Catalogs['categories'].keys())
available_types = sorted(Setting.Catalogs['types'].keys())


class Command(BaseCommand):
    help = """Display synnefo settings

    Example:
    settings --select type=mandatory,configured
    settings --select hidden --select type=default,
    """

    option_list = BaseCommand.option_list + (
        make_option(
            "-s", "--select",
            type='string',
            dest="selection_strings",
            action="append",
            metavar='[!]selection,...',
            help=("List settings that match any comma-separated criteria:"
                  "  all\n"
                  "  type=<setting type>\n"
                  "  category=<setting category>\n"
                  "  hidden\n"
                  "  configured\n"
                  "  <SETTING_NAME>\n"
                  "\n"
                  "Available types: {types}\n"
                  "Available categories: {categories}\n"
                  "\n"
                  "Multiple --select options yield the intersection "
                  "of their results\n"
                  "Prepending '!' negates the selection criterion\n"
                  ).format(types=available_types,
                           categories=available_categories)),
        make_option(
            "-o", "--sort-order",
            type='string',
            dest="sort_order",
            action="store",
            default='lexical',
            help=("Order settings. Available orderings: "
                  "['lexical', 'source', "
                  "'category-lexical', 'category-source']")),
        make_option(
            "-d", "--defaults",
            dest="display_defaults",
            action="store_true",
            default=False,
            help=("Include setting default value.")),

        make_option(
            "-t", "--status",
            dest="display_status",
            action="store_true",
            default=False,
            help=("Display internal setting status.")),
        make_option(
            "-1", "--oneline",
            dest="display_multiline",
            action="store_false",
            default=True,
            help=("Display setting in multiple lines")),
        make_option(
            "-l", "--details",
            dest="display_details",
            action="store_true",
            default=False,
            help=("Display full setting details")),
        make_option(
            "-p", "--printout",
            dest="printout",
            action="store_true",
            default=False,
            help=("Create a printout of settings as comment blocks.")),
        make_option(
            "-f", "--printout-files",
            dest="printout_files",
            action="store",
            metavar="SETTINGS-DIRECTORY",
            help=("Create a printout of settings grouped "
                  "in files by category.")),
    )

    def mk_filter_all(self, param):
        if param != '':
            m = "Invalid filter parameter '{0}'".format(param)
            raise AssertionError(m)

        def filter_all(setting):
            return True
        return filter_all

    def mk_filter_category(self, category):
        if category not in Setting.Catalogs['categories']:
            m = "Unknown category '{0}'".format(category)
            raise CommandError(m)

        def filter_category(setting):
            return setting.category == category
        return filter_category

    def mk_filter_type(self, setting_type):
        if setting_type not in Setting.Catalogs['types']:
            m = "Unknown type '{0}'".format(setting_type)
            raise CommandError(m)

        def filter_type(setting):
            return setting.setting_type == setting_type
        return filter_type

    def mk_filter_hidden(self, hidden):
        if hidden != '':
            m = "Invalid hidden filter parameter '{0}'".format(hidden)
            raise AssertionError(m)

        def filter_hidden(setting):
            return not setting.export
        return filter_hidden

    def mk_filter_configured(self, configured):
        if configured != '':
            m = "Invalid configured filter parameter '{0}'".format(configured)
            raise AssertionError(m)

        def filter_configured(setting):
            return setting.configured_value is not NoValue
        return filter_configured

    def mk_filter_setting(self, setting_name):
        if not Setting.is_valid_setting_name(setting_name):
            m = "Invalid setting name '{0}'".format(setting_name)
            raise AssertionError(m)

        def filter_setting(setting):
            return setting.setting_name == setting_name
        return filter_setting

    def mk_negate(self, filter_method):
        def negated_filter(*args, **kwargs):
            return not filter_method(*args, **kwargs)
        return negated_filter

    _mk_filters = {
        'all': 'mk_filter_all',
        'category': 'mk_filter_category',
        'type': 'mk_filter_type',
        'configured': 'mk_filter_configured',
        'hidden': 'mk_filter_hidden',
        'setting': 'mk_filter_setting',
    }

    def parse_selection_filters(self, string):
        filters = []
        for term in string.split(','):
            key, sep, value = term.partition('=')
            if key.startswith('!'):
                negate = True
                key = key[1:]
            else:
                negate = False

            if key not in self._mk_filters:
                if not Setting.is_valid_setting_name(key):
                    return None
                value = key
                key = 'setting'

            mk_filter_method = getattr(self, self._mk_filters[key])
            if not mk_filter_method:
                m = "Unknown filter '{0}'".format(key)
                raise CommandError(m)

            filter_method = mk_filter_method(value)
            if negate:
                filter_method = self.mk_negate(filter_method)
            filters.append(filter_method)
        return filters

    def sort_lexical(display_settings):
        return sorted(display_settings.iteritems())

    def sort_source(display_settings):
        registry = Setting.Catalogs['registry']
        sortable = []
        for name, setting in display_settings.iteritems():
            sortable.append((registry[name], name, setting))
        sortable.sort()
        return [(t[1], t[2]) for t in sortable]

    def sort_category_lexical(display_settings):
        sortable = []
        for name, setting in display_settings.iteritems():
            sortable.append((setting.category, name, setting))
        sortable.sort()
        return [(t[1], t[2]) for t in sortable]

    def sort_category_source(display_settings):
        registry = Setting.Catalogs['registry']
        sortable = []
        for name, setting in display_settings.iteritems():
            sortable.append((setting.category, registry[name], setting))
        sortable.sort()
        return [(t[1], t[2]) for t in sortable]

    sort_methods = {
        'lexical': sort_lexical,
        'source': sort_source,
        'category-lexical': sort_category_lexical,
        'category-source': sort_category_source,
    }

    def display_console(self, display_settings_list, options):
        for name, setting in display_settings_list:
            format_str = "{name} = {value}"
            flags = []

            if setting.runtime_value == setting.default_value:
                flags.append('default')

            if setting.configured_value is not NoValue:
                flags.append('configured')
                if setting.runtime_value != setting.configured_value:
                    flags.append('runtime')

            value = setting.runtime_value
            default_value = setting.default_value
            example_value = setting.example_value
            dependencies = setting.dependencies
            description = setting.description
            sep = " # "
            eol = ""

            if options['display_multiline']:
                value = pformat(value)
                default_value = pformat(default_value)
                example_value = pformat(example_value)
                dependencies = pformat(dependencies)
                sep = "\n  # "
                description = (sep + '  ').join(wrap(description, 70))
                eol = "\n"

            format_args = {'name': name,
                           'value': value,
                           'example': example_value,
                           'default': default_value,
                           'description': description,
                           'dependencies': dependencies,
                           'serial': setting.serial,
                           'configured_depth': setting.configured_depth,
                           'configured_source': setting.configured_source,
                           'configure_callback': setting.configure_callback,
                           'flags': ','.join(flags)}

            sep = "\n  # " if options['display_multiline'] else " # "
            eol = "\n" if options['display_multiline'] else ""

            if options['display_details'] or options['display_defaults']:
                format_str += sep + "Default: {default}"

            if options['display_details'] or options['display_status']:
                format_str += sep + "Flags: {flags}"

            if options['display_details']:
                format_str += sep + "Description: {description}"
                format_str += sep + "Dependencies: {dependencies}"
                format_str += sep + "Depth: {configured_depth}"
                format_str += sep + "Serial: {serial}"
                format_str += sep + "Callback: {configure_callback}"
                format_str += sep + "Source: {configured_source}"

            line = format_str.format(**format_args) + eol
            print line

    def display_printout(self, display_settings_list):
        for name, setting in display_settings_list:
            comment = setting.present_as_comment() + '\n'
            print comment

    def printout_files(self, display_settings_list, path):
        if not isdir(path):
            m = "Cannot find directory '{path}'".format(path=path)
            raise CommandError(m)

        category_depths = {}
        for name, setting in Setting.Catalogs['settings'].iteritems():
            category = setting.category
            if (category not in category_depths or
                    setting.configured_depth > category_depths[category]):
                category_depths[category] = setting.configured_depth

        old_filepath = None
        conffile = None
        filepath = None
        for name, setting in display_settings_list:
            category = setting.category
            category_depth = 10 * category_depths[category]
            filepath = '{path}/{depth}-{category}.conf'
            filepath = filepath.format(path=path,
                                       depth=category_depth,
                                       category=category)
            if filepath != old_filepath:
                if conffile:
                    conffile.close()
                conffile = open(filepath, "a")
                old_filepath = filepath
            conffile.write(setting.present_as_comment())
            conffile.write('\n')

    def handle(self, *args, **options):
        if args:
            raise CommandError("This command takes no arguments. Only options")

        selection_strings = options["selection_strings"]
        if not selection_strings:
            selection_strings = ['configured']

        and_filters = [self.parse_selection_filters(s)
                       for s in selection_strings]

        settings_dict = Setting.Catalogs['settings']
        display_settings = {}
        for name, setting in settings_dict.items():
            if all(any(or_filter(setting) for or_filter in and_filter)
                   for and_filter in and_filters):
                display_settings[name] = setting

        sort_order = options['sort_order']
        if sort_order not in self.sort_methods:
            m = "Unknown sort method '{0}'".format(sort_order)
            raise CommandError(m)

        sort_method = self.sort_methods[sort_order]
        display_settings_list = sort_method(display_settings)

        if options['printout']:
            self.display_printout(display_settings_list)
        elif options['printout_files']:
            self.printout_files(display_settings_list,
                                options['printout_files'])
        else:
            self.display_console(display_settings_list, options)
