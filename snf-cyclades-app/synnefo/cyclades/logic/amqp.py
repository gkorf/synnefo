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

from synnefo import settings
from synnefo.lib.amqp.amqp_puka import AMQPPukaClient
from synnefo.lib.amqp.amqp_haigha import AMQPHaighaClient

ClientMap = {
    'puka': AMQPPukaClient,
    'haigha': AMQPHaighaClient,
}

try:
    Client = ClientMap[settings.CYCLADES_AMQP_BACKEND]
except KeyError:
    raise Exception('Unknown Backend %s' % settings.CYCLADES_AMQP_BACKEND)


class AMQPClient(Client):
    def __init__(self, *args, **kwargs):
        if 'hosts' not in kwargs:
            kwargs['hosts'] = settings.CYCLADES_AMQP_HOSTS
            return Client(args, kwargs)
