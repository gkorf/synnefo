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

from synnefo.cyclades.api import api as api_lib
from synnefo.django.lib.api import *
from django.conf import settings


def api_method(*args, **kwargs):
    if 'astakos_auth_url' not in kwargs:
        kwargs['astakos_auth_url'] = settings.CYCLADES_ASTAKOS_AUTH_URL

    return api_lib.api_method(args, kwargs)
