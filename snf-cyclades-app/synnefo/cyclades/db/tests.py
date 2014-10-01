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

# Unit Tests for db
#
# Provides automated tests for db module

from django.test import TestCase, TransactionTestCase
from django.db import transaction as django_transaction
from django.conf import settings

# Import pool tests
from synnefo.cyclades.db.pools.tests import *
from synnefo.cyclades.db.models import *

from synnefo.cyclades.db import models_factory as mfact
from synnefo.cyclades.db.pools import IPPool, EmptyPool
from synnefo.cyclades.db import transaction as cyclades_transaction

from django.db import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
from synnefo.django.utils.testing import override_settings
from mock import patch


class FlavorTest(TestCase):
    def test_flavor_name(self):
        """Test a flavor object name method."""
        flavor = mfact.FlavorFactory(cpu=1, ram=1024, disk=40,
                                     volume_type__disk_template="temp")
        self.assertEqual(
            flavor.name, "C1R1024D40temp", "flavor.name is not"
            " generated correctly. Name is %s instead of C1R1024D40temp" %
            flavor.name)


class BackendTest(TestCase):
    def setUp(self):
        self.backend = mfact.BackendFactory()

    @patch("synnefo.cyclades.db.models.get_rapi_client")
    def test_get_client(self, client):
        id_ = self.backend.id
        hash_ = self.backend.hash
        name = self.backend.clustername
        passwd = self.backend.password
        user = self.backend.username
        port = self.backend.port
        self.backend.get_client()
        client.assert_called_once_with(id_, hash_, name, port, user, passwd)

    def test_save_hash(self):
        """Test that backend hash is generated on credential change"""
        old_hash = self.backend.hash
        for field in ['clustername', 'username', 'password', 'port']:
            value = 5181 if field == 'port' else 'foo'
            self.backend.__setattr__(field, value)
            self.backend.save()
            self.assertNotEqual(old_hash, self.backend.hash)
            old_hash = self.backend.hash

    def test_unique_index(self):
        """Test that each backend gets a unique index"""
        backends = [self.backend]
        for i in xrange(0, 14):
            backends.append(mfact.BackendFactory())
        indexes = map(lambda x: x.index, backends)
        self.assertEqual(len(indexes), len(set(indexes)))

    def test_backend_number(self):
        """Test that no more than 16 backends are created"""
        for i in xrange(0, 14):
            mfact.BackendFactory()
        self.assertRaises(Exception, mfact.BackendFactory, ())

    def test_delete_active_backend(self):
        """Test that a backend with non-deleted VMS is not deleted"""
        backend = mfact.BackendFactory()
        vm = mfact.VirtualMachineFactory(backend=backend)
        self.assertRaises(IntegrityError, backend.delete, ())
        vm.backend = None
        vm.save()
        backend.delete()

    def test_password_encryption(self):
        password_hash = self.backend.password
        self.backend.password = '123'
        self.assertNotEqual(self.backend.password_hash, '123')
        self.assertNotEqual(self.backend.password_hash, password_hash)
        self.assertEqual(self.backend.password, '123')

    def test_hypervisor(self):
        from synnefo.cyclades.db.models import snf_settings
        kvm_backend = mfact.BackendFactory(hypervisor="kvm")
        xen_pvm_backend = mfact.BackendFactory(hypervisor="xen-pvm")
        xen_hvm_backend = mfact.BackendFactory(hypervisor="xen-hvm")
        with override_settings(snf_settings, GANETI_USE_HOTPLUG=True):
            self.assertTrue(kvm_backend.use_hotplug())
            self.assertFalse(xen_pvm_backend.use_hotplug())
            self.assertFalse(xen_hvm_backend.use_hotplug())
        with override_settings(snf_settings, GANETI_USE_HOTPLUG=False):
            self.assertFalse(kvm_backend.use_hotplug())
            self.assertFalse(xen_pvm_backend.use_hotplug())
            self.assertFalse(xen_hvm_backend.use_hotplug())
        kwargs = {"os": "snf-image+default",
                  "hvparams": {"kvm": {"foo1": "mpaz1"},
                               "xen-pvm": {"foo2": "mpaz2"},
                               "xen-hvm": {"foo3": "mpaz3"}}}
        with override_settings(snf_settings,
                               GANETI_CREATEINSTANCE_KWARGS=kwargs):
            self.assertEqual(kvm_backend.get_create_params(),
                             {"os": "snf-image+default",
                              "hvparams": {"foo1": "mpaz1"}})
            self.assertEqual(xen_pvm_backend.get_create_params(),
                             {"os": "snf-image+default",
                              "hvparams": {"foo2": "mpaz2"}})
            self.assertEqual(xen_hvm_backend.get_create_params(),
                             {"os": "snf-image+default",
                              "hvparams": {"foo3": "mpaz3"}})
        with override_settings(snf_settings, GANETI_CREATEINSTANCE_KWARGS={}):
            self.assertEqual(kvm_backend.get_create_params(), {"hvparams": {}})


class VirtualMachineTest(TestCase):
    def setUp(self):
        self.vm = mfact.VirtualMachineFactory()

    @patch("synnefo.cyclades.db.models.get_rapi_client")
    def test_get_client(self, client):
        backend = self.vm.backend
        id_ = backend.id
        hash_ = backend.hash
        name = backend.clustername
        passwd = backend.password
        user = backend.username
        port = backend.port
        self.vm.get_client()
        client.assert_called_once_with(id_, hash_, name, port, user, passwd)

    def test_create(self):
        vm = VirtualMachine()
        self.assertEqual(vm.action, None)
        self.assertEqual(vm.backendjobid, None)
        self.assertEqual(vm.backendjobstatus, None)
        self.assertEqual(vm.backendopcode, None)
        self.assertEqual(vm.backendlogmsg, None)
        self.assertEqual(vm.operstate, 'BUILD')


class NetworkTest(TestCase):
    def setUp(self):
        self.net = mfact.NetworkWithSubnetFactory()

    def test_tags(self):
        net1 = mfact.NetworkFactory(flavor='IP_LESS_ROUTED')
        self.assertEqual(net1.backend_tag, ['ip-less-routed'])
        net1 = mfact.NetworkFactory(flavor='CUSTOM')
        self.assertEqual(net1.backend_tag, [])

    def test_create_backend_network(self):
        len_backends = len(Backend.objects.all())
        back = mfact.BackendFactory()
        self.net.create_backend_network(backend=back)
        BackendNetwork.objects.get(network=self.net, backend=back)
        back1 = mfact.BackendFactory()
        back2 = mfact.BackendFactory()
        self.net.create_backend_network()
        BackendNetwork.objects.get(network=self.net, backend=back1)
        BackendNetwork.objects.get(network=self.net, backend=back2)
        self.assertEqual(len(BackendNetwork.objects.filter(network=self.net)),
                         len_backends + 3)

    def test_pool(self):
        pool = self.net.get_ip_pools()[0]
        pool.network = self.net
        self.assertTrue(isinstance(pool, IPPool))

    def test_reserve_ip(self):
        net1 = mfact.NetworkWithSubnetFactory(subnet__cidr='192.168.2.0/24')
        pool = net1.get_ip_pools()[0]
        self.assertTrue(pool.is_available('192.168.2.12'))
        net1.reserve_address('192.168.2.12')
        pool = net1.get_ip_pools()[0]
        self.assertFalse(pool.is_available('192.168.2.12'))
        net1.release_address('192.168.2.12')
        pool = net1.get_ip_pools()[0]
        self.assertTrue(pool.is_available('192.168.2.12'))


class BackendNetworkTest(TestCase):
    def test_mac_prefix(self):
        network = mfact.NetworkFactory(mac_prefix='aa:bb:c')
        backend = mfact.BackendFactory()
        bnet = mfact.BackendNetworkFactory(network=network, backend=backend)
        self.assertTrue(backend.index < 10)
        self.assertEqual(bnet.mac_prefix, 'aa:bb:c%s' % backend.index)

    def test_invalid_mac(self):
        network = mfact.NetworkFactory(mac_prefix='zz:bb:c')
        backend = mfact.BackendFactory()
        self.assertRaises(utils.InvalidMacAddress,
                          mfact.BackendNetworkFactory,
                          network=network, backend=backend)


class BridgePoolTest(TestCase):
    def test_no_pool(self):
        self.assertRaises(EmptyPool,
                          BridgePoolTable.get_pool)

    def test_two_pools(self):
        mfact.BridgePoolTableFactory()
        mfact.BridgePoolTableFactory()
        self.assertRaises(MultipleObjectsReturned, BridgePoolTable.get_pool)


class AESTest(TestCase):
    def test_encrypt_decrtypt(self):
        from synnefo.cyclades.db import aes_encrypt as aes
        old = 'bar'
        new = aes.decrypt_db_charfield(aes.encrypt_db_charfield(old))
        self.assertEqual(old, new)

    def test_password_change(self):
        from synnefo.cyclades.db import aes_encrypt as aes
        old_pass = aes.SECRET_ENCRYPTION_KEY
        old = 'bar'
        encrypted = aes.encrypt_db_charfield(old)
        aes.SECRET_ENCRYPTION_KEY = 'foo2'
        self.assertRaises(aes.CorruptedPassword, aes.decrypt_db_charfield,
                          encrypted)
        aes.SECRET_ENCRYPTION_KEY = old_pass
        new = aes.decrypt_db_charfield(encrypted)
        self.assertEqual(old, new)

    def test_big_secret(self):
        from synnefo.cyclades.db import aes_encrypt as aes
        old = aes.SECRET_ENCRYPTION_KEY
        aes.SECRET_ENCRYPTION_KEY = \
            '91490231234814234812348913289481294812398421893489'
        self.assertRaises(ValueError, aes.encrypt_db_charfield, 'la')
        aes.SECRET_ENCRYPTION_KEY = old


class TransactionException(Exception):

    """A dummy exception specifically for the transaction tests."""

    pass


class TransactionTest(TransactionTestCase):

    """Check if cyclades transactions work properly.

    TODO: Add multi-db tests.
    """

    def good_transaction(self):
        mfact.VirtualMachineFactory()

    def bad_transaction(self):
        self.good_transaction()
        raise TransactionException

    def test_good_transaction(self):
        django_transaction.commit_on_success(self.good_transaction)()
        self.assertEqual(VirtualMachine.objects.count(), 1)

    def test_bad_transaction(self):
        with self.assertRaises(TransactionException):
            django_transaction.commit_on_success(self.bad_transaction)()
        self.assertEqual(VirtualMachine.objects.count(), 0)

    def test_good_transaction_custom_decorator(self):
        cyclades_transaction.commit_on_success(self.good_transaction)()
        self.assertEqual(VirtualMachine.objects.count(), 1)

    def test_bad_transaction_custom_decorator(self):
        with self.assertRaises(TransactionException):
            cyclades_transaction.commit_on_success(self.bad_transaction)()
        self.assertEqual(VirtualMachine.objects.count(), 0)

    def test_bad_transaction_custom_decorator_incorrect_dbs(self):
        settings.DATABASES['cyclades'] = settings.DATABASES['default']
        with self.assertRaises(TransactionException):
            cyclades_transaction.commit_on_success(self.bad_transaction)()
        self.assertEqual(VirtualMachine.objects.count(), 0)
        settings.DATABASES.pop("cyclades")

    def test_bad_transaction_custom_decorator_using(self):
        with self.assertRaises(TransactionException):
            cyclades_transaction.commit_on_success(using="default")(self.bad_transaction)()
        self.assertEqual(VirtualMachine.objects.count(), 0)
