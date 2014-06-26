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

from synnefo.util.entry_points import extend_dict_from_entry_point
from synnefo.lib.services import fill_endpoints
from synnefo.lib import parse_base_url

from synnefo.lib.settings.setup import Setting, Auto, Default

CUSTOMIZE_SERVICES = Default(
    default_value=(),
    example_value={('cyclades_ui', 'prefix'): 'view',
                   ('astakos_ui', 'prefix'): 'view'},
    export=0,
    #dependencies=('SYNNEFO_SERVICES',)  #uncomment this to test cycle
    description=("A list of key-path and value pairs that would be applied to "
                 "the services registry after its automatic initialization."),
)

services = {}
extend_dict_from_entry_point(services, 'synnefo', 'services')

from sys import modules
module = modules[__name__]


def customize_from_items(document, items):
    d = document
    for path, value in items:
        for step in path[:-1]:
            d = d[step]
        d[path[-1]] = value


def mk_auto_configure_base_host(base_url_name):
    def auto_configure_base_host(setting, value, deps):
        Setting.enforce_not_configurable(setting, value)
        base_url = deps[base_url_name]
        base_host, base_path = parse_base_url(base_url)
        return base_host
    return auto_configure_base_host


def mk_auto_configure_base_path(base_url_name):
    def auto_configure_base_path(setting, value, deps):
        Setting.enforce_not_configurable(setting, value)
        base_url = deps[base_url_name]
        base_host, base_path = parse_base_url(base_url)
        return base_path
    return auto_configure_base_path


components = {}
for service_name, service in services.items():
    component_name = service['component']
    if component_name not in components:
        components[component_name] = {}
    components[component_name][service_name] = service


SYNNEFO_COMPONENTS = Auto(
    configure_callback=Setting.enforce_not_configurable,
    export=0,
    default_value=components,
    description=("A list with the names of all synnefo components currently "
                 "installed. Initialized from SYNNEFO_SERVICES. "
                 "It is dynamically generated and cannot be configured."),
    dependencies=['SYNNEFO_SERVICES'],
)


def auto_configure_services(setting, value, deps):
    Setting.enforce_not_configurable(setting, value)
    services = setting.default_value
    customization = deps['CUSTOMIZE_SERVICES']
    if isinstance(customization, dict):
        customization = customization.items()
    customize_from_items(services, customization)
    return services


def mk_auto_configure_services(component_name, base_url_name):
    def auto_configure_service(setting, value, deps):
        components = deps['SYNNEFO_COMPONENTS']
        component = components[component_name]
        base_url = deps[base_url_name]
        for service_name, service in component.iteritems():
            fill_endpoints(service, base_url)
        return component
    return auto_configure_service


SYNNEFO_SERVICES = Auto(
    configure_callback=auto_configure_services,
    export=0,
    default_value=services,
    dependencies=['CUSTOMIZE_SERVICES'],
    description=("An auto-generated registry of all services provided by all "
                 "currently installed Synnefo components. "
                 "It is dynamically generated and cannot be configured. "
                 "For service customization use CUSTOMIZE_SERVICES."),
)
