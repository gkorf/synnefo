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


class SettingsError(Exception):
    pass


class CycleError(SettingsError):
    """Cyclic dependencies"""
    pass


NoValue = type('NoValue', (), {})

_serial = 0

Catalogs = {
    'registry': {},
    'settings': {},
    'types': defaultdict(dict),
    'categories': defaultdict(dict),
    'modules': defaultdict(dict),
    'defaults': {},
    'configured': {},
    'runtime': {},
    'init_dependents': {},
    'init_pending': {},
}


def initialize_settings(settings_dict, source="unknown", strict=False):
    settings = Catalogs['settings']
    categories = Catalogs['categories']
    defaults = Catalogs['defaults']
    init_dependents = Catalogs['init_dependents']
    pending = Catalogs['init_pending']
    types = Catalogs['types']
    modules = Catalogs['modules']

    for name, setting in settings_dict.iteritems():
        if not isinstance(setting, Setting):
            if strict:
                m = "Setting name '{name}' has non-annotated value '{value}'!"
                m = m.format(name=name, value=setting)
                raise SettingsError(m)
            else:
                print "non-annotated %s, %s" % (source, name)
                setting = Setting(default_value=setting)

        #FIXME: duplicate annotations?
        if name in settings:
           m = ("Duplicate setting '{name}': existing from "
                "'{orig}', new found in '{new}'.")
           m = m.format(name=name, orig=settings[name].annotation_source,
                        new=source)
           # raise SettingsError(m)
           print m
        for init_dep in setting.init_dependencies:
            if init_dep in settings:
                if init_dep in init_dependents:
                    m = ("Init dependency '{depname}' of setting '{name}' "
                         "found both in settings and in forward "
                         "dependencies!")
                    m = m.format(depname=init_dep, name=name)
                    raise AssertionError(m)
                dep_setting = settings[init_dep]
                if not dep_setting.init_dependents:
                    dep_setting.init_dependents = []
                dep_setting.init_dependents.append(name)
            else:
                if init_dep not in init_dependents:
                    init_dependents[init_dep] = []
                init_dependents[init_dep].append(name)

        setting.setting_name = name
        setting.annotation_source = source
        if name in init_dependents:
            setting.init_dependents = init_dependents.pop(name)
        settings[name] = setting
        pending[name] = setting
        modules[setting.annotation_source][name] = setting
        categories[setting.category][name] = setting
        types[setting.setting_type][name] = setting
        default_value = setting.default_value
        defaults[name] = default_value
        setting.initialize()

    defaults['_SETTING_CATALOGS'] = Catalogs


def reset_all_catalogs():
    for name, catalog in Catalogs.iteritems():
        catalog.clear()


def load_settings_from_file(path, settings_dict=None):
    if settings_dict is None:
        settings_dict = {}
    new_settings = {}
    execfile(path, settings_dict, new_settings)
    return new_settings


def is_valid_setting_name(name):
    return name.isupper() and not name.startswith('_')


def load_configuration(new_settings,
                       source='unknown',
                       allow_override=False,
                       allow_unknown=False,
                       allow_known=True):

    settings = Catalogs['settings']
    defaults = Catalogs['defaults']
    configured = Catalogs['configured']

    for name, value in new_settings.iteritems():
        if not is_valid_setting_name(name):
            # silently ignore it?
            continue

        if name in settings:
            if not allow_known:
                m = ("{source}: setting '{name} = {value}' not allowed to "
                     "be set here")
                m = m.format(source=source, name=name, value=value)
                raise SettingsError(m)
        else:
            if allow_unknown:
                # pretend it was declared in a default settings module
                desc = "Unknown setting from {source}"
                desc = desc.format(source=source)
                setting = Setting(default_value=value,
                                  category='unknown',
                                  description=desc)
                initialize_settings({name: setting}, strict=True)
            else:
                m = ("{source}: unknown setting '{name} = {value}' not "
                     "allowed to be set here")
                m = m.format(source=source, name=name, value=value)
                raise SettingsError(m)

        if not allow_override and name in configured:
            m = ("{source}: new setting '{name} = {value}' "
                 "overrides setting '{name} = {oldval}'")
            m = m.format(source=source, name=name, value=value,
                         oldval=defaults[name])
            raise SettingsError(m)

        # setting has been accepted for configuration
        setting = settings[name]
        setting.configured_value = value
        setting.configured_source = source
        configured[name] = value
        defaults[name] = value

    return new_settings


def check_setting_for_cycle(settings, name):
    """Check if a setting is in a dependency cycle among given settings.

    """
    if name not in settings:
        m = "No setting '{name}' found!"
        m = m.format(name=name)
        raise ValueError(m)

    setting = settings[name]
    stack = [(d, (name, d)) for d in (setting.dependencies)]
    while stack:
        current, path = stack.pop()
        setting = settings[current]
        for dep in setting.dependencies:
            stack.append((dep, path + (dep,)))
            if dep == name:
                path = list(path)
                path.append(name)
                m = "dependency cycle detected: {path}"
                m = m.format(path=' >> '.join(path))
                raise CycleError(m)
    return True


def assign_dependents(settings_dict):
    for setting_name, setting in settings_dict.iteritems():
        dependencies = setting.dependencies
        if not dependencies:
            continue

        for dep_name in dependencies:
            dep_setting = settings_dict[dep_name]
            dep_setting.dependents.add(setting_name)


def get_settings_from_object(settings_object):
    var_list = []
    for name in dir(settings_object):
        if not is_valid_setting_name(name):
            continue
        var_list.append((name, getattr(settings_object, name)))
    return var_list


def assign_configured_depths(settings_dict):
    unresolved = set(settings_dict.keys())
    next_surface = set(unresolved)
    while True:
        resolution_count = 0
        resolution_surface = next_surface
        next_surface = set()
        for setting_name in list(resolution_surface):
            setting = settings_dict[setting_name]

            if not setting.dependencies:
                setting.configured_depth = 0
                resolution_count += 1
                resolution_surface.discard(setting_name)
                unresolved.discard(setting_name)
                next_surface.update(setting.dependents)
                continue

            #if setting.configured_depth is not None:
            #    raise AssertionError("Cycle")

            max_depth = 0
            for dep_name in setting.dependencies:
                dep_setting = settings_dict[dep_name]
                dep_depth = dep_setting.configured_depth
                if dep_depth is None:
                    max_depth = None
                    break

                if dep_depth > max_depth:
                    max_depth = dep_depth

            if max_depth is not None:
                setting.configured_depth = max_depth + 1
                resolution_count += 1
                unresolved.discard(setting_name)
                next_surface.update(setting.dependents)

        if not unresolved:
            break

        if not resolution_count:
            # cycle detected
            for name in unresolved:
                break
            check_setting_for_cycle(settings_dict, name)
            raise AssertionError("This should have been unreachable")


def preconfigure_settings(setting_names=()):
    settings = Catalogs['settings']
    if not setting_names:
        setting_names = settings.keys()

    pending = Catalogs['init_pending']
    dependents= Catalogs['init_dependents']
    m = ""
    if pending:
        m += ("There are settings that failed to initialize: "
              "[{failed}]\n")
        failed = ', '.join(sorted(pending.iterkeys()))
        m = m.format(failed=failed)
    if dependents:
        m += ("There are settings that are referenced but not found: "
              "{notfound}\n")
        notfound = ', '.join(
            ("%s referenced by %s" % (name, ', '.join(dependents)))
            for name, dependents in dependents.iteritems())
        m = m.format(notfound=notfound)
    if m:
        raise SettingsError(m)

    # setting depth determination & cycle detection

    assign_dependents(settings)
    assign_configured_depths(settings)


def configure_settings(setting_names=()):
    preconfigure_settings(setting_names)
    failed = []
    for name, setting in Catalogs['settings'].items():
        try:
            setting.configure()
        except SettingsError as e:
            failed.append(e)

    if failed:
        import sys
        sys.stderr.write('\n')
        sys.stderr.write('\n'.join(map(str, failed)))
        sys.stderr.write('\n\n')
        raise SettingsError("Failed to configure settings.")


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
        Initialized as None. Setting.initialize_settings will set it.

    configured_value:
        This is the value given by a configuration file.
        If it does not exist, then the setting was not set by
        the administrator.

        Initialized as Setting.NoValue.
        Setting.load_configuration will set it.

    configured_source:
        This is the source (e.g. configuration file path) where the
        setting was configured. It is None if the setting has not
        been configured.

    configured_depth:
        The depth of the setting in the configure dependency tree (forest).
        Settings with no dependencies have 0 depth, others greater than 0.

    runtime_value:
        This is the final setting value after all configuration
        processing. Its existence indicates that all processing
        for this setting has been completed.

        Initialized as Setting.NoValue.
        Setting.configure will set it upon completion.

    serial:
        The setting's serial index in the 'registry' catalog.
        Represents the chronological order of execution of its annotation.

    dependents:
        The set of the names of the settings that depend on this one.

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

    setting_name = '__unnamed__'
    setting_type = 'setting'

    default_value = None
    example_value = None
    description = 'This setting is missing documentation'
    category = 'misc'
    dependencies = ()
    dependents = None
    init_dependencies = ()
    init_dependents = ()
    export = True

    serial = None
    configured_value = NoValue
    configured_source = None
    configured_depth = None
    runtime_value = NoValue
    fail_exception = None
    required_args = ()
    disallowed_args = ()
    _checked_arguments = False
    annotation_source = None

    def __repr__(self):
        flags = []
        if self.configured_value is not NoValue:
            flags.append("configured")
            value = self.configured_value
        else:
            flags.append("default")
            value = self.default_value

        if self.runtime_value is not NoValue:
            flags.append("finalized")

        if self.fail_exception is not None:
            flags.append("failed({0})".format(self.fail_exception))
        r = "<{setting_name}(type:{setting_type})[flags:{flags}]: {value}>" 
        r = r.format(setting_name=self.setting_name,
                     setting_type=self.setting_type,
                     value=repr(value),
                     flags=','.join(flags))
        return r

    __str__ = __repr__

    def present_as_comment(self, runtime=False):
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
        runtime_value = self.runtime_value
        if example_value != default_value:
            example = "Example value: {0}"
            example = example.format(pformat(example_value)).split('\n')
            description += ["# "]
            description += [("# " + s) for s in example]

        assignment = "{name} = {value}"
        assignment = assignment.format(name=self.setting_name,
                                       value=pformat(default_value))
        assignment = [("#" + s) for s in assignment.split('\n')]
        if runtime and self.configured_value is not NoValue \
                and runtime_value != self.default_value:
            runtime_assignment = "{name} = {value}"
            runtime_assignment = runtime_assignment.format(
                name=self.setting_name,
                value=pformat(self.runtime_value))
            assignment += [runtime_assignment]

        return '\n'.join(chain(header, ['#'],
                               description, ['#'],
                               assignment))

    @staticmethod
    def init_callback(setting):
        return

    @staticmethod
    def configure_callback(setting, value, dependencies):
        if value is NoValue:
            return setting.default_value
        else:
            # by default, acknowledge the configured value
            # and allow it to be used.
            return NoValue

    def validate(self):
        """Example setting validate method"""

        setting_name = self.setting_name
        if self is not Catalogs['settings'][setting_name]:
            raise AssertionError()

        runtime_value = self.runtime_value
        if runtime_value is NoValue:
            raise AssertionError()

        configured_value = self.configured_value
        if configured_value not in (NoValue, runtime_value):
            raise AssertionError()

    def check_arguments(self, kwargs):
        if self._checked_arguments:
            return

        arg_set = set(kwargs.keys())
        required_set = set(self.required_args)
        intersection = arg_set.intersection(required_set)
        if intersection != required_set:
            missing = ', '.join(required_set - intersection)
            m = "{self}: Required arguments [{missing}] not found."
            m = m.format(self=self, missing=missing)
            raise SettingsError(m)

        disallowed_set = set(self.disallowed_args)
        intersection = arg_set.intersection(disallowed_set)
        if intersection:
            m = "{self}: Given arguments [{disallowed}] are disallowed."
            m = m.format(self=self, disallowed=', '.join(intersection))
            raise SettingsError(m)

        self._checked_arguments = True

    def __init__(self, **kwargs):

        attr_names = ['default_value', 'example_value', 'description',
                      'category', 'export',
                      'init_dependencies', 'init_callback',
                      'dependencies', 'configure_callback']

        self.check_arguments(kwargs)

        for name in attr_names:
            if name in kwargs:
                setattr(self, name, kwargs[name])

        dependencies = self.dependencies
        if isinstance(dependencies, basestring):
            m = ".dependencies must be an iterable of str, not {this}"
            m = m.format(this=repr(dependencies))
            raise ValueError(m)
        self.dependencies = tuple(dependencies)
        for d in self.dependencies:
            if not isinstance(d, str):
                m = ".dependencies must be a tuple of str, not {this}"
                m = m.format(this=repr(d))
                raise ValueError(m)

        init_dependencies = self.init_dependencies
        if isinstance(dependencies, basestring):
            m = ".init_dependencies must be an iterable of str, not an str"
            raise ValueError(m)
        self.init_dependencies = tuple(init_dependencies)
        for d in self.init_dependencies:
            if not isinstance(d, str):
                m = ".init_dependencies must be a tuple of str, not {this}"
                m = m.format(this=repr(d))
                raise ValueError(m)

        self.dependents = set()
        registry = Catalogs['registry']
        global _serial
        self.serial = _serial
        _serial += 1
        registry[self.serial] = self

    def initialize(setting, dep_stack=()):
        settings = Catalogs['settings']
        pending = Catalogs['init_pending']
        setting_name = setting.setting_name
        dep_stack += (setting_name,)

        if setting_name not in pending:
            m = "Attempt to initialize already initialized setting '{name}'!"
            m = m.format(name=setting_name)
            raise AssertionError(m)

        for init_dep in setting.init_dependencies:
            if init_dep in dep_stack:
                m = "Settings init dependency cycle detected: {stack}"
                m = m.format(stack=dep_stack + (init_dep,))
                raise SettingsError(m)

            if init_dep not in settings:
                pending[setting_name] = setting
                return False

            dep_setting = settings[init_dep]
            if init_dep in pending:
                if not dep_setting.initialize(dep_stack):
                    pending[setting_name] = setting
                    return False

        init_callback = setting.init_callback
        init_callback(setting)
        del pending[setting_name]
        for dependent in setting.init_dependents:
            if dependent in pending:
                settings[dependent].initialize(dep_stack[:-1])
        return True

    def configure(setting, dep_stack=()):
        settings = Catalogs['settings']
        runtime = Catalogs['runtime']
        setting_name = setting.setting_name
        dep_stack += (setting_name,)

        if setting.runtime_value is not NoValue:
            # already configured, nothing to do.
            return

        if setting.fail_exception is not None:
            # it has previously failed, re-raise the error
            exc = setting.fail_exception
            if not isinstance(exc, Exception):
                exc = SettingsError(str(exc))
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
            exc = SettingsError(m)
            setting.fail_exception = exc
            raise exc

        deps = {}
        for dep_name in setting.dependencies:
            if dep_name not in settings:
                m = ("Unknown dependecy setting '{dep_name}' "
                     "for setting '{name}'!")
                m = m.format(dep_name=dep_name, name=setting_name)
                raise SettingsError(m)

            # The following dependency cycle check may be redundant
            # since cycles are checked in configure_settings(),
            # but better safe than sorry.
            if dep_name in dep_stack:
                m = "Settings dependency cycle detected: {stack}"
                m = m.format(stack=dep_stack + (dep_name,))
                exc = SettingsError(m)
                setting.fail_exception = exc
                raise exc

            dep_setting = settings[dep_name]
            if dep_setting.fail_exception is not None:
                m = ("Cannot configure setting {name} because it depends "
                     "on '{dep}' which has failed to configure.")
                m = m.format(name=setting_name, dep=dep_name)
                exc = SettingsError(m)
                setting.fail_exception = exc
                raise exc

            if dep_setting.runtime_value is NoValue:
                dep_setting.configure(dep_stack)

            dep_value = dep_setting.runtime_value
            deps[dep_name] = dep_value

        try:
            new_value = configure_callback(setting, setting_value, deps)
        except SettingsError as e:
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
                exc = SettingsError(m)
                setting.fail_exception = exc
                raise exc
            else:
                setting_value = new_value

        setting.runtime_value = setting_value
        runtime[setting_name] = setting_value

    def enforce_not_configurable(setting, value, deps=None):
        if value is not NoValue:
            m = "Setting '{name}' is not configurable."
            m = m.format(name=setting.setting_name)
            raise SettingsError(m)
        return setting.default_value


class Mandatory(Setting):
    """Mandatory settings have to be to be configured by the
    administrator in the configuration files. There are no defaults,
    and not giving a value will raise an exception.

    """
    setting_type = 'mandatory'
    disallowed_args = ('export', 'default_value')
    required_args = ('example_value', 'description', 'category')

    def __init__(self, **kwargs):
        kwargs.pop('export', None)
        self.check_arguments(kwargs)
        kwargs['export'] = True
        Setting.__init__(self, **kwargs)

    @staticmethod
    def configure_callback(setting, value, deps):
        if value is NoValue:
            if environ.get('SYNNEFO_RELAX_MANDATORY_SETTINGS'):
                return setting.example_value

            m = ("Setting '{name}' is mandatory. "
                 "Please provide a real value. "
                 "Example value: '{example}'")
            m = m.format(name=setting.setting_name,
                         example=setting.example_value)
            raise SettingsError(m)

        return NoValue


class SubMandatory(Setting):
    """SubMandatory settings are made mandatory only if a condition
    on their dependencies is true. The default condition is that the
    settings it depends on have a true value via bool().

    If the dependency list is not empty then 'export' and 'category' attributes
    are inherited from the settings in that list, and they must all agree on
    the same value.

    Example:
    ENABLE_FAST_BACKEND = Default(default_value=False, ...)
    FAST_BACKEND_SPEED = SubMandatory(
        example_value=9001,
        dependencies=['ENABLE_FAST_BACKEND'])

    """
    setting_type = 'submandatory'
    disallowed_args = ('init_dependencies', 'init_callback',
                       'configure_callback')
    required_args = ('example_value', 'description')

    def __init__(self, depends=None, condition_callback=None, **kwargs):

        if depends:
            if 'dependencies' in kwargs:
                m = "Cannot specify both 'depends' and 'dependencies'"
                raise TypeError(m)
            kwargs['dependencies'] = (depends,)

        dependencies = kwargs.get('dependencies', ())
        if dependencies:
            # if we depend on other settings,
            # we inherit their export and category.
            self.disallowed_args += ('export', 'category')

        self.check_arguments(kwargs)

        kwargs['init_dependencies'] = dependencies
        Setting.__init__(self, **kwargs)
        if condition_callback is not None:
            self.condition_callback = condition_callback


    @staticmethod
    def condition_callback(setting, value, deps):
        if not deps:
            m = "Setting '{name}' requires at least one dependency."
            m = m.format(name=setting.setting_name)
            raise SettingsError(m)
        return any(bool(setting_value) for setting_value in deps.itervalues())

    @staticmethod
    def configure_callback(setting, value, deps):
        condition_callback = setting.condition_callback
        if condition_callback(setting, value, deps):
            # We are mandatory
            if value is NoValue:
                if environ.get('SYNNEFO_RELAX_MANDATORY_SETTINGS'):
                    return setting.example_value

                m = ("Setting '{name}' is mandatory due to configuration of "
                     "{due}. Please provide a real value. "
                     "Example value: '{example}'")
                if deps:
                    due = "[" + ', '.join(sorted(deps.keys())) + "]"
                else:
                    due = "[runtime-determined parameters]"
                m = m.format(name=setting.setting_name,
                             example=setting.example_value,
                             due=due)
                raise SettingsError(m)

        elif value is NoValue:
            return setting.default_value

        # acknowledge configured value
        return NoValue


    @staticmethod
    def init_callback(setting):
        # if we depend on other settings,
        # they must all agree on export and category

        dependencies = setting.init_dependencies
        if not dependencies:
            return

        settings = Catalogs['settings']
        firstdep = dependencies[0]
        firstdep_setting = settings[firstdep]
        export = firstdep_setting.export
        category = firstdep_setting.category
        for dep in dependencies[1:]:
            dep_setting = settings[dep]
            if dep_setting.category != category:
                m = ("SubMandatory settings require that all "
                     "their dependencies have the same 'category' value. "
                     "However '{firstdep}' has '{firstval}' while "
                     "'{dep}' has '{val}'")
                m = m.format(firstdep=firstdep, firstval=category,
                             dep=dep, val=dep_setting.category)
                raise SettingsError(m)
            if dep_setting.export != export:
                m = ("SubMandatory settings require that all "
                     "their dependencies have the same 'export' value. "
                     "However '{firstdep}' has '{firstval}' while "
                     "'{dep}' has '{val}'")
                m = m.format(firstdep=firstdep, firstval=export,
                             dep=dep, val=dep_setting.export)
                raise SettingsError(m)
        setting.export = export
        setting.category = category


class Default(Setting):
    """Default settings are not mandatory.
    There are default values that are meant to work well, and also serve as an
    example if no explicit example is given.

    """
    setting_type = 'default'
    required_args = ('default_value', 'description')

    def __init__(self, **kwargs):
        self.check_arguments(kwargs)
        if 'example_value' not in kwargs:
            kwargs['example_value'] = kwargs['default_value']
        Setting.__init__(self, **kwargs)


class Constant(Setting):
    """Constant settings are a like defaults, only they are not intended to be
    visible or configurable by the administrator.

    """
    setting_type = 'constant'
    disallowed_args = ('export',)
    required_args = ('default_value', 'description')

    def __init__(self, **kwargs):
        kwargs.pop('export', None)
        self.check_arguments(kwargs)
        kwargs['export'] = False
        Setting.__init__(self, **kwargs)


class Auto(Setting):
    """Auto settings can be computed automatically.
    Administrators may attempt to override them and the setting
    may or may not accept being overriden. If override is not accepted
    it will result in an error, not in a silent discarding of user input.

    """
    setting_type = 'auto'
    required_args = ('configure_callback', 'description')

    @staticmethod
    def configure_callback(setting, value, deps):
        raise NotImplementedError()


class Deprecated(object):
    """Deprecated settings must be removed, renamed, or otherwise fixed."""

    setting_type = 'deprecated'
    disallowed_args = ('export', 'default_value', 'example_value')
    required_args = ('description',)

    def __init__(self, rename_to=None, **kwargs):
        self.rename_to = rename_to
        self.check_arguments(kwargs)
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
        raise SettingsError(m)


from synnefo.util.entry_points import get_entry_points
from synnefo.lib.settings import default


def initialize_modules():
    synnefo_settings = {}
    for name in dir(default):
        if not is_valid_setting_name(name):
            continue
        synnefo_settings[name] = getattr(default, name)
    initialize_settings(synnefo_settings,
                        source=default.__name__, strict=False)

    for e in get_entry_points('synnefo', 'default_settings'):
        m = e.load()
        synnefo_settings = {}
        for name in dir(m):
            if not is_valid_setting_name(name):
                continue
            synnefo_settings[name] = getattr(m, name)

        # set strict to True to require annotation of all settings
        initialize_settings(synnefo_settings,
                            source=m.__name__, strict=False)


    # e = get_module_entry_point(module, 'synnefo', 'default_settings')
    # m = e.load()
    # synnefo_settings = {}
    # for name in dir(m):
    #     if not is_valid_setting_name(name):
    #         continue
    #     synnefo_settings[name] = getattr(m, name)

    # # set strict to True to require annotation of all settings
    # initialize_settings(synnefo_settings, source=m.__name__,
    #                     strict=False)
    preconfigure_settings()
