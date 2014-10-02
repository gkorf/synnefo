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


def mk_components(setting, value, deps):
    Setting.enforce_not_configurable(setting, value)
    services = {}
    extend_dict_from_entry_point(services, 'synnefo', 'services')
    components = {}
    for service_name, service in services.items():
        component_name = service['component']
        if component_name not in components:
            components[component_name] = {}
        components[component_name][service_name] = service
    return components


SYNNEFO_COMPONENTS = Auto(
    configure_callback=mk_components,
    export=0,
    description=("A list with the names of all synnefo components currently "
                 "installed. Initialized from SYNNEFO_SERVICES. "
                 "It is dynamically generated and cannot be configured."),
    dependencies=['SYNNEFO_SERVICES'],
)


def auto_configure_services(setting, value, deps):
    Setting.enforce_not_configurable(setting, value)
    services = {}
    extend_dict_from_entry_point(services, 'synnefo', 'services')
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
    dependencies=['CUSTOMIZE_SERVICES'],
    description=("An auto-generated registry of all services provided by all "
                 "currently installed Synnefo components. "
                 "It is dynamically generated and cannot be configured. "
                 "For service customization use CUSTOMIZE_SERVICES."),
)
