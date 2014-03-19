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

from copy import deepcopy
from synnefo.lib import join_urls
from urlparse import urlparse


class ServiceNotFound(Exception):
    pass


def fill_endpoints(service, base_url):
    prefix = service['prefix']
    endpoints = service['endpoints']
    for endpoint in endpoints:
        version = endpoint['versionId']
        publicURL = endpoint['publicURL']
        if publicURL is not None:
            continue

        publicURL = join_urls(base_url, prefix, version).rstrip('/')
        endpoint['publicURL'] = publicURL


def filter_public(services):
    public_services = {}
    for name, service in services.iteritems():
        if service.get('public', False):
            public_services[name] = deepcopy(service)
    return public_services


def filter_component(services, component_name):
    component_services = {}
    for name, service in services.iteritems():
        if service['component'] == component_name:
            component_services[name] = service
    return component_services


def get_service_prefix(services, service_name):
    return services[service_name]['prefix']


def get_service_resources(services, service_name):
    return services[service_name]['resources']


def get_public_endpoint(services, service_type, version=None):
    found_endpoints = {}
    for service_name, service in services.iteritems():
        if service_type != service['type']:
            continue

        for endpoint in service['endpoints']:
            endpoint_version = endpoint['versionId']
            if version is not None:
                if version != endpoint_version:
                    continue
            found_endpoints[endpoint_version] = endpoint

    if not found_endpoints:
        m = "No endpoint found for service type '{0}'".format(service_type)
        if version is not None:
            m += " and version '{0}'".format(version)
        raise ServiceNotFound(m)

    selected = sorted(found_endpoints.keys())[-1]
    return found_endpoints[selected]['publicURL']


def get_service_endpoints(services, service_name, version=None):
    endpoints = services[service_name]['endpoints']
    if version is not None:
        filtered = []
        for endpoint in endpoints:
            if endpoint['versionId'] != version:
                continue
            filtered.append(endpoint)
        endpoints = filtered
    return endpoints


def get_service_path(services, service_name, version=None):
    endpoints = get_service_endpoints(services, service_name, version=version)
    if not endpoints:
        m = "No endpoint found for service '{0}'".format(service_name)
        if version is not None:
            m += " and version '{0}'".format(version)
        raise ServiceNotFound(m)
    service_url = endpoints[0]['publicURL']
    return urlparse(service_url).path.rstrip('/')
