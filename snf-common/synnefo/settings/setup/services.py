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
from synnefo.util.keypath import customize_from_items
from synnefo.lib.services import fill_endpoints
from synnefo.lib import parse_base_url


def setup_services(settings):
    services = {}
    extend_dict_from_entry_point(services, 'synnefo', 'services')

    customization = getattr(settings, 'CUSTOMIZE_SERVICES', ())
    if isinstance(customization, dict):
        customization = customization.items()
    customize_from_items(services, customization)
    setattr(settings, 'SYNNEFO_SERVICES', services)

    components = {}
    for service_name, service in services.items():
        component_name = service['component']
        if component_name not in components:
            components[component_name] = {}
        components[component_name][service_name] = service
    setattr(settings, 'SYNNEFO_COMPONENTS', components)


def setup_base_urls(settings):
    for component_name in settings.SYNNEFO_COMPONENTS.keys():
        name_upper = component_name.upper()
        base_url_name = name_upper + '_BASE_URL'
        base_host_name = name_upper + '_BASE_HOST'
        base_path_name = name_upper + '_BASE_PATH'
        base_url = getattr(settings, base_url_name, None)
        if base_url is None:
            m = ("No '{setting_name}' setting found even though "
                 "component '{component_name}' is installed!\n")
            m = m.format(setting_name=base_url_name,
                         component_name=component_name)
            raise AssertionError(m)

        base_host, base_path = parse_base_url(base_url)
        setattr(settings, base_host_name, base_host)
        setattr(settings, base_path_name, base_path)


def setup_endpoints(settings):
    for service_name, service in settings.SYNNEFO_SERVICES.iteritems():
        component_name = service['component']
        base_url_name = component_name.upper() + '_BASE_URL'
        base_url = getattr(settings, base_url_name)
        fill_endpoints(service, base_url)


def setup_settings(settings):
    setup_services(settings)
    setup_base_urls(settings)
    setup_endpoints(settings)
