# Copyright 2013-2014 GRNET S.A. All rights reserved.
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
