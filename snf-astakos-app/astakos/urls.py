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

from django.conf.urls import include, patterns

from snf_django.lib.api.utils import prefix_pattern_of, prefix_pattern
from snf_django.utils.urls import \
    extend_with_root_redirects, extend_endpoint_with_slash
from django.conf import settings

urlpatterns = []

astakos_services = settings.SYNNEFO_COMPONENTS['astakos']

# Redirects should be first, otherwise they may get overridden by wildcards
extend_endpoint_with_slash(urlpatterns, astakos_services, 'astakos_ui')
extend_endpoint_with_slash(urlpatterns, astakos_services, 'astakos_weblogin')

astakos_patterns = patterns(
    '',
    (prefix_pattern_of('astakos_ui'), include('astakos.im.urls')),
    (prefix_pattern_of('astakos_account'), include('astakos.api.urls')),
    (prefix_pattern_of('astakos_identity'),
     include('astakos.api.keystone_urls')),
    (prefix_pattern_of('astakos_weblogin'),
     include('astakos.im.weblogin_urls')),
    (prefix_pattern_of('astakos_admin'), include('astakos.admin.admin_urls')),
    ('', include('astakos.oa2.urls')),
)

urlpatterns += patterns(
    '',
    (prefix_pattern(settings.ASTAKOS_BASE_PATH), include(astakos_patterns)),
)

# set utility redirects
extend_with_root_redirects(urlpatterns, astakos_services,
                           'astakos_ui', settings.ASTAKOS_BASE_PATH)
