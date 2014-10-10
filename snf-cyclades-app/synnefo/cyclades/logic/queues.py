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


from synnefo.settings import CYCLADES_BACKEND_PREFIX_ID, DEBUG, CYCLADES_EXCHANGE_GANETI

try:
    prefix = CYCLADES_BACKEND_PREFIX_ID.split('-')[0]
except TypeError, IndexError:
    raise Exception("Invalid CYCLADES_BACKEND_PREFIX_ID")

# EXCHANGES
EXCHANGES = (CYCLADES_EXCHANGE_GANETI,)


# QUEUES
QUEUE_OP = "%s-events-op" % prefix
QUEUE_NETWORK = "%s-events-network" % prefix
QUEUE_PROGRESS = "%s-events-progress" % prefix
QUEUE_CLUSTER = "%s-events-cluster" % prefix


QUEUES = (QUEUE_OP,
          QUEUE_NETWORK,
          QUEUE_PROGRESS,
          QUEUE_CLUSTER)

# ROUTING KEYS
# notifications of type "ganeti-op-status"
KEY_OP = 'ganeti.%s.event.op' % prefix
# notifications of type "ganeti-network-status"
KEY_NETWORK = 'ganeti.%s.event.network' % prefix
# notifications of type "ganeti-create-progress"
KEY_PROGRESS = 'ganeti.%s.event.progress' % prefix
KEY_CLUSTER = 'ganeti.event.cluster'

# BINDINGS:
BINDINGS = (
    # Queue           # Exchange        # RouteKey    # Handler
    (QUEUE_OP,        CYCLADES_EXCHANGE_GANETI,  KEY_OP,       'update_db'),
    (QUEUE_NETWORK,   CYCLADES_EXCHANGE_GANETI,  KEY_NETWORK,  'update_network'),
    (QUEUE_PROGRESS,  CYCLADES_EXCHANGE_GANETI,  KEY_PROGRESS, 'update_build_progress'),
    (QUEUE_CLUSTER,   CYCLADES_EXCHANGE_GANETI,  KEY_CLUSTER,  'update_cluster'),
)


## Extra for DEBUG:
if DEBUG is True:
    # Debug queue, retrieves all messages
    QUEUE_DEBUG = "%s-debug" % prefix
    QUEUES += (QUEUE_DEBUG,)
    BINDINGS += ((QUEUE_DEBUG, CYCLADES_EXCHANGE_GANETI, "#", "dummy_proc"),)


def convert_queue_to_dead(queue):
    """Convert the name of a queue to the corresponding dead-letter one"""
    return queue + "-dl"


def convert_exchange_to_dead(exchange):
    """Convert the name of an exchange to the corresponding dead-letter one"""
    return exchange + "-dl"


EVENTD_HEARTBEAT_ROUTING_KEY = "eventd.heartbeat"


def get_dispatcher_request_queue(hostname, pid):
    return "snf:dispatcher:%s:%s" % (hostname, pid)


def get_dispatcher_heartbeat_queue(hostname, pid):
    return "snf:dispatcher:heartbeat:%s:%s" % (hostname, pid)
