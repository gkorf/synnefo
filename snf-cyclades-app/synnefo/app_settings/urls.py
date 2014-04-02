# Copyright 2011 GRNET S.A. All rights reserved.
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

from django.conf.urls import patterns, include

from snf_django.lib.api.proxy import proxy
from snf_django.lib.api.utils import prefix_pattern, prefix_pattern_of
from snf_django.utils.urls import \
    extend_with_root_redirects, extend_endpoint_with_slash
from snf_django.lib.api.urls import api_patterns
from django.conf import settings

from functools import partial


urlpatterns = []

cyclades_services = settings.SYNNEFO_SERVICES["cyclades"]

# Redirects should be first, otherwise they may get overridden by wildcards
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_ui')
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_helpdesk')
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'admin')
extend_endpoint_with_slash(urlpatterns, cyclades_services, 'cyclades_userdata')

cyclades_patterns = api_patterns(
    '',
    (prefix_pattern_of('cyclades_vmapi'), include('synnefo.vmapi.urls')),
    (prefix_pattern_of('cyclades_plankton'), include('synnefo.plankton.urls')),
    (prefix_pattern_of('cyclades_compute'), include('synnefo.api.urls')),
    (prefix_pattern_of('cyclades_network'),
     include('synnefo.api.network_urls')),
    (prefix_pattern_of('cyclades_userdata'), include('synnefo.userdata.urls')),
    (prefix_pattern_of('cyclades_admin'), include('synnefo.admin.urls')),
    (prefix_pattern_of('cyclades_volume'), include('cyclades.volume.urls')),
)

cyclades_patterns += patterns(
    '',
    (prefix_pattern_of('cyclades_ui'), include('synnefo.ui.urls')),
)

cyclades_patterns += api_patterns(
    '',
    (prefix_pattern_of('cyclades_helpdesk'), include('synnefo.helpdesk.urls')),
)

urlpatterns += patterns(
    '',
    (prefix_pattern(settings.CYCLADES_BASE_PATH), include(cyclades_patterns)),
)


# # --------------------------------------
# # PROXY settings
# astakos_auth_proxy = \
#     partial(proxy, proxy_base=ASTAKOS_AUTH_PROXY_PATH,
#             target_base=ASTAKOS_AUTH_URL)
# astakos_account_proxy = \
#     partial(proxy, proxy_base=ASTAKOS_ACCOUNT_PROXY_PATH,
#             target_base=ASTAKOS_ACCOUNT_URL)

# # ui views serve html content, redirect instead of proxing
# astakos_ui_proxy = \
#     partial(proxy, proxy_base=ASTAKOS_UI_PROXY_PATH,
#             target_base=ASTAKOS_UI_URL, redirect=True)

# urlpatterns += api_patterns(
#     '',
#     (prefix_pattern(ASTAKOS_AUTH_PROXY_PATH), astakos_auth_proxy),
#     (prefix_pattern(ASTAKOS_ACCOUNT_PROXY_PATH), astakos_account_proxy),
# )
# urlpatterns += patterns(
#     '',
#     (prefix_pattern(ASTAKOS_UI_PROXY_PATH), astakos_ui_proxy),
# )

# --------------------------------------
# set utility redirects
extend_with_root_redirects(urlpatterns, cyclades_services,
                           'cyclades_ui', settings.CYCLADES_BASE_PATH)
