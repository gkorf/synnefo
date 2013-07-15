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


class Example(object):
    """Example settings are mandatory to be configured with real values.
    There are no defaults, and not giving a value is a fatal error.

    """
    def __init__(self, example_value, description=None):
        self.example_value = example_value
        self.default_value = None
        self.description = description


class Default(object):
    """Default settings are not mandatory in nature.
    There are default values that are meant to work well,
    and also serve as an example.

    """
    def __init__(self, default_value, example=None, description=None):
        self.default_value = default_value
        if example is None:
            example = default_value
        self.example_value = example
        self.description = description


class Deprecated(object):
    """Deprecated settings must be removed, renamed, or otherwise fixed."""
    def __init__(self, rename_to=None, description=None):
        self.rename_to = rename_to
        self.description = description


def get_all_settings(settings):
    var_list = []
    for name in dir(settings):
        if not name.isupper() or name.startswith('_'):
            continue
        var_list.append((name, getattr(settings, name)))
    return var_list


def preproc_settings(settings):
    other = {}
    defaults = {}
    mandatory = {}
    deprecated = {}

    for name, value in get_all_settings(settings):
        if isinstance(value, Example):
            mandatory[name] = value
        elif isinstance(value, Default):
            defaults[name] = value
            setattr(settings, name, value.default_value)
        elif isinstance(value, Deprecated):
            deprecated[name] = value
        else:
            other[name] = value

    settings._OTHER = other
    settings._DEFAULTS = defaults
    settings._MANDATORY = mandatory
    settings._DEPRECATED = deprecated


def postproc_settings(settings):
    configured = {}
    defaults = settings._DEFAULTS
    failed = []
    import os
    relax_mandatory = bool(os.environ.get('SYNNEFO_RELAX_MANDATORY_SETTINGS'))

    for name, value in get_all_settings(settings):
        if isinstance(value, Example):
            if relax_mandatory:
                setattr(settings, name, value.example_value)
            else:
                m = ("Setting '{name}' is mandatory. "
                     "Please provide a real value. "
                     "Example value: '{example}'")
                m = m.format(name=name, example=value.example_value)
                failed.append(m)
        elif isinstance(value, Default):
            m = "unprocessed default setting in post processing"
            raise AssertionError(m)
            defaults[name] = value
            setattr(settings, name, value.default_value)
        elif isinstance(value, Deprecated):
            m = "Setting '{name}' has been deprecated.".format(name=name)
            if value.rename_to:
                m += " Please rename it to '{rename}'.".format(
                    rename=value.rename_to)
            if value.description:
                m += "details: {desc}".format(desc=value.description)
            failed.append(m)
        elif name in defaults:
            if defaults[name].default_value is not value:
                configured[name] = value

    settings._CONFIGURED = configured
    if failed:
        import sys
        sys.stderr.write('\n')
        sys.stderr.write('\n'.join(failed))
        sys.stderr.write('\n\n')
        raise AssertionError("Failed to read settings.")
