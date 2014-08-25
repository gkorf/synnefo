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

from django.conf.urls import patterns, include

from synnefo.django.lib.api.proxy import proxy
from synnefo.django.lib.api.utils import prefix_pattern, prefix_pattern_of
from synnefo.django.utils.urls import \
    extend_with_root_redirects, extend_endpoint_with_slash
from synnefo.django.lib.api.urls import api_patterns
from synnefo.cyclades import cyclades_settings as settings

from functools import partial


urlpatterns = []

cyclades_services = settings.cyclades_services
# Redirects should be first, otherwise they may get overridden by wildcards
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_ui')
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_helpdesk')
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_admin')
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_userdata')

cyclades_patterns = api_patterns(
    '',
    (prefix_pattern_of('cyclades_vmapi'),
     include('synnefo.cyclades.vmapi.urls')),
    (prefix_pattern_of('cyclades_plankton'),
     include('synnefo.cyclades.plankton.urls')),
    (prefix_pattern_of('cyclades_compute'),
     include('synnefo.cyclades.api.compute_urls')),
    (prefix_pattern_of('cyclades_network'),
     include('synnefo.cyclades.api.network_urls')),
    (prefix_pattern_of('cyclades_userdata'),
     include('synnefo.cyclades.userdata.urls')),
    (prefix_pattern_of('cyclades_admin'),
     include('synnefo.cyclades.admin.urls')),
    (prefix_pattern_of('cyclades_volume'),
     include('synnefo.cyclades.volume.urls')),
)

cyclades_patterns += patterns(
    '',
    (prefix_pattern_of('cyclades_ui'), include('synnefo.cyclades.ui.urls')),
)

cyclades_patterns += api_patterns(
    '',
    (prefix_pattern_of('cyclades_helpdesk'),
     include('synnefo.cyclades.helpdesk.urls')),
)

urlpatterns += patterns(
    '',
    (prefix_pattern(settings.BASE_PATH), include(cyclades_patterns)),
)


# --------------------------------------
# PROXY settings
astakos_auth_proxy = \
    partial(proxy, proxy_base=settings.ASTAKOS_AUTH_PROXY_PATH,
            target_base=settings.ASTAKOS_AUTH_URL)
astakos_account_proxy = \
    partial(proxy, proxy_base=settings.ASTAKOS_ACCOUNT_PROXY_PATH,
            target_base=settings.ASTAKOS_ACCOUNT_URL)

# ui views serve html content, redirect instead of proxing
astakos_ui_proxy = \
    partial(proxy, proxy_base=settings.ASTAKOS_UI_PROXY_PATH,
            target_base=settings.ASTAKOS_UI_URL, redirect=True)

urlpatterns += api_patterns(
    '',
    (prefix_pattern(settings.ASTAKOS_AUTH_PROXY_PATH), astakos_auth_proxy),
    (prefix_pattern(settings.ASTAKOS_ACCOUNT_PROXY_PATH),
     astakos_account_proxy),
)
urlpatterns += patterns(
    '',
    (prefix_pattern(settings.ASTAKOS_UI_PROXY_PATH), astakos_ui_proxy),
)

# --------------------------------------
# set utility redirects
extend_with_root_redirects(urlpatterns, cyclades_services,
                           'cyclades_ui', settings.BASE_PATH)
