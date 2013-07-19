# Copyright 2013 GRNET S.A. All rights reserved.
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

from collections import defaultdict
from pprint import pformat
from textwrap import wrap
from itertools import chain
from os import environ


class Setting(object):
    """Setting is the parent class of all setting annotations.

    Setting.initialize_settings() will register a dictionary
    of setting names to Setting instances, process all
    annotations.

    Setting.load_configuration() will load user-specific
    configurations to the defaults.
    A setting set in this stage will be flagged 'configured'.
    Those that are not set in this stage will be flagged 'default'.

    Setting.configure_settings() will post-process all settings,
    maintaining the various registries and calling configuration
    callbacks for auto-generation or validation.

    A setting has the following attributes:

    ** CONFIGURATION ATTRIBUTES **

    default_value:
        The default value to be assigned if not given any by the
        administrator in the config files. To omit a default value
        assign Setting.NoValue to it.

    example_value:
        A value to serve as an informative guide for those who
        want to configure the setting. The default_value might not
        be that informative.

    description:
        Setting description for administrators and developers.

    category:
        An all-lowercase category name for grouping settings together.

    dependencies:
        A list of setting names and categories whose values will be
        given as input to configure_callback.

    configure_callback:
        A function that accepts three arguments, a Setting instance,
        the corresponding setting value given by the configuration
        files, and a dictionary with all setting dependencies declared.
        If the setting value has not be set by a config file,
        then its value (second argument) will be Setting.NoValue.

        If no value was provided by a config file, the callback must
        return the final setting value which will be assigned to it.
        If a value was provided, the callback must return
        Setting.NoValue to acknowledge it.

    export:
        If export is false then the setting will be marked not to be
        advertised in user-friendly lists or files.

    ** STATE ATTRIBUTES **

    setting_name:
        This is the name this setting annotation was given to.
        Initialized as None. Settings.initialize_settings will set it.

    configured_value:
        This is the value given by a configuration file.
        If it does not exist, then the setting was not set by
        the administrator.

        Initialized as Setting.NoValue.
        Settings.load_configuration will set it.

    configured_source:
        This is the source (e.g. configuration file path) where the
        setting was configured. It is None if the setting has not
        been configured.

    configured_depth:
        The depth of the setting in the dependency tree (forest).

    runtime_value:
        This is the final setting value after all configuration
        processing. Its existence indicates that all processing
        for this setting has been completed.

        Initialized as Setting.NoValue.
        Settings.configure_one_setting will set it upon completion.

    serial:
        The setting's serial index in the 'registry' catalog.
        Represents the chronological order of execution of its annotation.

    dependents:
        A list of the names of the settings that depend on this one.

    fail_exception:
        If the configuration of a setting has failed, this holds
        the exception raised, marking it as failed to prevent
        further attempts, and to be able to re-raise the error.
        Initialized as None.

    Subclasses may expose any subset of the above, as well as additional
    attributes of their own.

    Setting will construct certain setting catalogs during runtime
    initialization, later accessible via a 'Catalogs' class attribute
    dictionary:

        catalog = Setting.Catalogs['catalog_name']

    The catalogs are:

    1. Catalog 'settings'

       A catalog of all setting annotations collected at initialization.
       This is useful to access setting annotations at runtime,
       for example a setting's default value:

       settings = Setting.Catalogs['settings']
       settings['SOCKET_CONNECT_RETRIES'].default_value

    2. Catalog 'types'

       A catalog of the different types of settings.
       At each Setting instantiation, the (sub)class attribute
       'setting_type' will be used as the setting type name in the
       catalog.  Each entry in the catalog is a dictionary of setting
       names and setting annotation instances. For example:
       
       setting_types = Setting.Catalogs['types']
       setting_types['mandatory']['SETTING_NAME'] == setting_instance

    3. Catalog 'categories'

       A catalog of the different setting categories.
       At each Setting instantiation, the instance attribute 'category'
       will be used to group settings in categories. For example:

       categories = Setting.Catalogs['categories']
       categories['django']['SETTING_NAME'] == setting_instance

    4. Catalog 'defaults'

       A catalog of all settings that have been initialized and their
       default, pre-configuration values. This catalog is useful as
       input to the configuration from files.

    5. Catalog 'configured'

       A catalog of all settings that were configured by the
       administrator in the configuration files. Very relevant
       to the administrator as it effectively represents the
       deployment-specific configuration, without noise from
       all settings left default.
       Each setting is registered in the catalog just before
       the configure_callback is called.
       The catalog values are final setting values, not instances.

       configured = Setting.Catalogs['configured']
       print '\n'.join(("%s = %s" % it) for it in configured.items())

    5. Catalog 'runtime'

        A catalog of all finalized settings and their runtime values.
        This is output of the setting configuration process and
        where setting values must be read from at runtime.

    """

    class SettingsError(Exception):
        pass

    NoValue = type('NoValue', (), {})

    setting_type = 'setting'
    _serial = 0

    Catalogs = {
        'registry': {},
        'settings': {},
        'types': defaultdict(dict),
        'categories': defaultdict(dict),
        'defaults': {},
        'configured': {},
        'runtime': {},
    }

    default_value = None
    example_value = None
    description = 'This setting is missing documentation'
    category = 'misc'
    dependencies = ()
    dependents = ()
    export = True

    serial = None
    configured_value = NoValue
    configured_source = None
    configured_depth = 0
    runtime_value = NoValue
    fail_exception = None

    def __repr__(self):
        flags = []
        if self.configured_value is not Setting.NoValue:
            flags.append("configured")
            value = self.configured_value
        else:
            flags.append("default")
            value = self.default_value

        if self.runtime_value is not Setting.NoValue:
            flags.append("finalized")

        if self.fail_exception is not None:
            flags.append("failed({0})".format(self.fail_exception))
        r = "<{setting_type}[{flags}]: {value}>" 
        r = r.format(setting_type=self.setting_type,
                     value=repr(value),
                     flags=','.join(flags))
        return r

    __str__ = __repr__

    def present_as_comment(self):
        header = "# {name}: type {type}, category '{categ}'"
        header = header.format(name=self.setting_name,
                               type=self.setting_type.upper(),
                               categ=self.category)
        header = [header]

        if self.dependencies:
            header += ["# Depends on: "]
            header += ["#     " + d for d in sorted(self.dependencies)]

        description = wrap(self.description, 70)
        description = [("# " + s) for s in description]

        example_value = self.example_value
        default_value = self.default_value
        if example_value != default_value:
            example = "Example value: {0}"
            example = example.format(pformat(example_value)).split('\n')
            description += ["# "]
            description += [("# " + s) for s in example]

        assignment = "{name} = {value}"
        assignment = assignment.format(name=self.setting_name,
                                       value=pformat(default_value))
        assignment = [("#" + s) for s in assignment.split('\n')]

        return '\n'.join(chain(header, ['#'],
                               description, ['#'],
                               assignment))

    @staticmethod
    def configure_callback(setting, value, dependencies):
        if value is Setting.NoValue:
            return setting.default_value
        else:
            # by default, acknowledge the configured value
            # and allow it to be used.
            return Setting.NoValue

    def validate(self):
        """Example setting validate method"""

        NoValue = Setting.NoValue
        setting_name = self.setting_name
        if self is not Setting.Catalogs['settings'][setting_name]:
            raise AssertionError()

        runtime_value = self.runtime_value
        if runtime_value is NoValue:
            raise AssertionError()

        configured_value = self.configured_value
        if configured_value not in (NoValue, runtime_value):
            raise AssertionError()

    def __init__(self, **kwargs):

        attr_names = ['default_value', 'example_value', 'description',
                      'category', 'dependencies', 'configure_callback',
                      'export']

        for name in attr_names:
            if name in kwargs:
                setattr(self, name, kwargs[name])

        serial = Setting._serial
        Setting._serial = serial + 1
        registry = Setting.Catalogs['registry']
        self.serial = serial
        registry[serial] = self

    @staticmethod
    def is_valid_setting_name(name):
        return name.isupper() and not name.startswith('_')

    @staticmethod
    def get_settings_from_object(settings_object):
        var_list = []
        is_valid_setting_name = Setting.is_valid_setting_name
        for name in dir(settings_object):
            if not is_valid_setting_name(name):
                continue
            var_list.append((name, getattr(settings_object, name)))
        return var_list

    @staticmethod
    def initialize_settings(settings_dict, strict=False):
        Catalogs = Setting.Catalogs
        settings = Catalogs['settings']
        categories = Catalogs['categories']
        defaults = Catalogs['defaults']
        types = Catalogs['types']

        for name, value in settings_dict.iteritems():
            if not isinstance(value, Setting):
                if strict:
                    m = "Setting name '{name}' has non-annotated value '{value}'!"
                    m = m.format(name=name, value=value)
                    raise Setting.SettingsError(m)
                else:
                    value = Setting(default_value=value)

            # FIXME: duplicate annotations?
            #if name in settings:
            #    m = ("Duplicate annotation for setting '{name}': '{value}'. "
            #         "Original annotation: '{original}'")
            #    m = m.format(name=name, value=value, original=settings[name])
            #    raise Setting.SettingsError(m)
            value.setting_name = name
            settings[name] = value
            categories[value.category][name] = value
            types[value.setting_type][name] = value
            default_value = value.default_value
            defaults[name] = default_value

        defaults['_SETTING_CATALOGS'] = Catalogs

    @staticmethod
    def load_settings_from_file(path, settings_dict=None):
        if settings_dict is None:
            settings_dict = {}
        new_settings = {}
        execfile(path, settings_dict, new_settings)
        return new_settings

    @staticmethod
    def load_configuration(new_settings,
                           source='unknonwn',
                           allow_override=False,
                           allow_unknown=False,
                           allow_known=True):

        settings = Setting.Catalogs['settings']
        defaults = Setting.Catalogs['defaults']
        configured = Setting.Catalogs['configured']
        is_valid_setting_name = Setting.is_valid_setting_name

        for name, value in new_settings.iteritems():
            if not is_valid_setting_name(name):
                # silently ignore it?
                continue

            if name in settings:
                if not allow_known:
                    m = ("{source}: setting '{name} = {value}' not allowed to "
                         "be set here")
                    m = m.format(source=source, name=name, value=value)
                    raise Setting.SettingsError(m)
            else:
                if allow_unknown:
                    # pretend this was declared in a default settings module
                    desc = "Unknown setting from {source}".format(source=source)

                    setting = Setting(default_value=value,
                                      category='unknown',
                                      description=desc)
                    Setting.initialize_settings({name: setting}, strict=True)
                else:
                    m = ("{source}: unknown setting '{name} = {value}' not "
                         "allowed to be set here")
                    m = m.format(source=source, name=name, value=value)
                    raise Setting.SettingsError(m)

            if not allow_override and name in configured:
                m = ("{source}: new setting '{name} = {value}' "
                     "overrides setting '{name} = {oldval}'")
                m = m.format(source=source, name=name, value=value,
                             oldval=defaults[name])
                raise Setting.SettingsError(m)

            # setting has been accepted for configuration
            setting = settings[name]
            setting.configured_value = value
            setting.configured_source = source
            configured[name] = value
            defaults[name] = value

        return new_settings

    @staticmethod
    def configure_one_setting(setting_name, dep_stack=()):
        dep_stack += (setting_name,)
        Catalogs = Setting.Catalogs
        settings = Catalogs['settings']
        runtime = Catalogs['runtime']
        NoValue = Setting.NoValue

        if setting_name not in settings:
            m = "Unknown setting '{name}'"
            m = m.format(name=setting_name)
            raise Setting.SettingsError(m)

        setting = settings[setting_name]
        if setting.runtime_value is not NoValue:
            # already configured, nothing to do.
            return

        if setting.fail_exception is not None:
            # it has previously failed, re-raise the error
            exc = setting.fail_exception
            if not isinstance(exc, Exception):
                exc = Setting.SettingsError(str(exc))
            raise exc

        setting_value = setting.configured_value
        if isinstance(setting_value, Setting):
            m = ("Unprocessed setting annotation '{name} = {value}' "
                 "in setting configuration stage!")
            m = m.format(name=setting_name, value=setting_value)
            raise AssertionError(m)

        configure_callback = setting.configure_callback
        if not configure_callback:
            setting.runtime_value = setting_value
            return

        if not callable(configure_callback):
            m = ("attribute 'configure_callback' of "
                 "'{setting}' is not callable!")
            m = m.format(setting=setting)
            exc = Setting.SettingsError(m)
            setting.fail_exception = exc
            raise exc

        deps = {}
        for dep_name in setting.dependencies:
            if dep_name not in settings:
                m = ("Unknown dependecy setting '{dep_name}' "
                     "for setting '{name}'!")
                m = m.format(dep_name=dep_name, name=setting_name)
                raise Setting.SettingsError(m)

            if dep_name in dep_stack:
                m = "Settings dependency cycle detected: {stack}"
                m = m.format(stack=dep_stack)
                exc = Setting.SettingsError(m)
                setting.fail_exception = exc
                raise exc

            dep_setting = settings[dep_name]
            if dep_setting.fail_exception is not None:
                m = ("Cannot configure setting {name} because it depends "
                     "on '{dep}' which has failed to configure.")
                m = m.format(name=setting_name, dep=dep_name)
                exc = Setting.SettingsError(m)
                setting.fail_exception = exc
                raise exc

            if dep_setting.runtime_value is NoValue:
                Setting.configure_one_setting(dep_name, dep_stack)

            dep_value = dep_setting.runtime_value
            deps[dep_name] = dep_value

        try:
            new_value = configure_callback(setting, setting_value, deps)
        except Setting.SettingsError as e:
            setting.fail_exception = e
            raise

        if new_value is not NoValue:
            if setting_value is not NoValue:
                m = ("Configure callback of setting '{name}' does not "
                     "acknowledge the fact that a value '{value}' was "
                     "provided by '{source}' and wants to assign "
                     "a value '{newval}' anyway!")
                m = m.format(name=setting_name, value=setting_value,
                             source=setting.configured_source,
                             newval=new_value)
                exc = Setting.SettingsError(m)
                setting.fail_exception = exc
                raise exc
            else:
                setting_value = new_value

        setting.runtime_value = setting_value
        runtime[setting_name] = setting_value

    @staticmethod
    def configure_settings(setting_names=()):
        settings = Setting.Catalogs['settings']
        if not setting_names:
            setting_names = settings.keys()

        bottom = set(settings.keys())
        for name, setting in settings.iteritems():
            dependencies = setting.dependencies
            if not dependencies:
                continue
            bottom.discard(name)
            for dep_name in setting.dependencies:
                dep_setting = settings[dep_name]
                if not dep_setting.dependents:
                    dep_setting.dependents = []
                dep_setting.dependents.append(name)

        depth = 1
        while True:
            dependents = []
            for name in bottom:
                setting = settings[name]
                setting.configured_depth = depth
                dependents.extend(setting.dependents)
            if not dependents:
                break
            bottom = dependents
            depth += 1

        failed = []
        for name in Setting.Catalogs['settings']:
            try:
                Setting.configure_one_setting(name)
            except Setting.SettingsError as e:
                failed.append(e)

        if failed:
            import sys
            sys.stderr.write('\n')
            sys.stderr.write('\n'.join(map(str, failed)))
            sys.stderr.write('\n\n')
            raise Setting.SettingsError("Failed to configure settings.")

    @staticmethod
    def enforce_not_configurable(setting, value, deps=None):
        if value is not Setting.NoValue:
            m = "Setting '{name}' is not configurable."
            m = m.format(name=setting.setting_name)
            raise Setting.SettingsError(m)
        return setting.default_value


class Mandatory(Setting):
    """Mandatory settings have to be to be configured by the
    administrator in the configuration files. There are no defaults,
    and not giving a value will raise an exception.

    """
    setting_type = 'mandatory'

    def __init__(self, example_value=Setting.NoValue, **kwargs):
        if example_value is Setting.NoValue:
            m = "Mandatory settings require an example_value"
            raise Setting.SettingsError(m)
        kwargs['example_value'] = example_value
        kwargs['export'] = True
        Setting.__init__(self, **kwargs)

    @staticmethod
    def configure_callback(setting, value, deps):
        if value is Setting.NoValue:
            if environ.get('SYNNEFO_RELAX_MANDATORY_SETTINGS'):
                return setting.example_value

            m = ("Setting '{name}' is mandatory. "
                 "Please provide a real value. "
                 "Example value: '{example}'")
            m = m.format(name=setting.setting_name,
                         example=setting.example_value)
            raise Setting.SettingsError(m)

        return Setting.NoValue


class Default(Setting):
    """Default settings are not mandatory.
    There are default values that are meant to work well, and also serve as an
    example if no explicit example is given.

    """
    setting_type = 'default'

    def __init__(self, default_value=Setting.NoValue,
                 description="No description", **kwargs):
        if default_value is Setting.NoValue:
            m = "Default settings require a default_value"
            raise Setting.SettingsError(m)

        kwargs['default_value'] = default_value
        if 'example_value' not in kwargs:
            kwargs['example_value'] = default_value
        kwargs['description'] = description
        Setting.__init__(self, **kwargs)


class Constant(Setting):
    """Constant settings are a like defaults, only they are not intended to be
    visible or configurable by the administrator.

    """
    setting_type = 'constant'

    def __init__(self, default_value=Setting.NoValue,
                 description="No description", **kwargs):
        if default_value is Setting.NoValue:
            m = "Constant settings require a default_value"
            raise Setting.SettingsError(m)

        kwargs['default_value'] = default_value
        if 'example_value' not in kwargs:
            kwargs['example_value'] = default_value
        kwargs['export'] = False
        kwargs['description'] = description
        Setting.__init__(self, **kwargs)


class Auto(Setting):
    """Auto settings can be computed automatically.
    Administrators may attempt to override them and the setting
    may or may not accept being overriden. If override is not accepted
    it will result in an error, not in a silent discarding of user input.

    """
    setting_type = 'auto'

    def __init__(self, configure_callback=None, **kwargs):
        if not configure_callback:
            m = "Auto settings must provide a configure_callback"
            raise Setting.SettingsError(m)

        kwargs['configure_callback'] = configure_callback
        Setting.__init__(self, **kwargs)

    @staticmethod
    def configure_callback(setting, value, deps):
        raise NotImplementedError()


class Deprecated(object):
    """Deprecated settings must be removed, renamed, or otherwise fixed."""

    setting_type = 'deprecated'

    def __init__(self, rename_to=None, **kwargs):
        self.rename_to = rename_to
        kwargs['export'] = False
        Setting.__init__(self, **kwargs)

    @staticmethod
    def configure_callback(setting, value, deps):
        m = ("Setting {name} has been deprecated. "
             "Please consult upgrade notes and ")

        if setting.rename_to:
            m += "rename to {rename_to}."
        else:
            m += "remove it."

        m = m.format(name=setting.setting_name, rename_to=setting.rename_to)
        raise Setting.SettingsError(m)

