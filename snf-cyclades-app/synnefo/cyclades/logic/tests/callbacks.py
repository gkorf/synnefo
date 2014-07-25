# vim: set fileencoding=utf-8 :
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

# Provides automated tests for logic module

from random import randint

from django.test import TestCase

from synnefo.cyclades.db.models import (VirtualMachine, IPAddress, BackendNetwork,
                               Network, BridgePoolTable, MacPrefixPoolTable)
from synnefo.cyclades.db import models_factory as mfactory
from synnefo.lib.utils import split_time
from datetime import datetime
from mock import patch
from synnefo.cyclades.api.util import allocate_resource
from synnefo.cyclades.logic.callbacks import (update_db, update_network,
                                     update_build_progress)
from snf_django.utils.testing import mocked_quotaholder
from synnefo.cyclades.logic.rapi import GanetiApiError

now = datetime.now
from time import time
import json


## Test Callbacks
@patch('synnefo.lib.amqp.AMQPClient')
class UpdateDBTest(TestCase):
    def create_msg(self, **kwargs):
        """Create snf-ganeti-eventd message"""
        msg = {'event_time': split_time(time())}
        msg['type'] = 'ganeti-op-status'
        msg['status'] = 'success'
        msg['jobId'] = 1
        msg['logmsg'] = 'Dummy Log'
        for key, val in kwargs.items():
            msg[key] = val
        message = {'body': json.dumps(msg)}
        return message

    def test_missing_attribute(self, client):
        update_db(client, json.dumps({'body': {}}))
        self.assertTrue(client.basic_reject.called)

    def test_unhandled_exception(self, client):
        update_db(client, {})
        client.basic_reject.assert_called_once()

    def test_missing_instance(self, client):
        msg = self.create_msg(operation='OP_INSTANCE_STARTUP',
                              instance='foo')
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)

    def test_wrong_type(self, client):
        msg = self.create_msg(type="WRONG_TYPE")
        update_db(client, msg)
        self.assertTrue(client.basic_nack.called)

    def test_old_msg(self, client):
        from time import sleep
        from datetime import datetime
        old_time = time()
        sleep(0.01)
        new_time = datetime.fromtimestamp(time())
        vm = mfactory.VirtualMachineFactory(backendtime=new_time)
        vm.operstate = 'STOPPED'
        vm.save()
        msg = self.create_msg(operation='OP_INSTANCE_STARTUP',
                              event_time=split_time(old_time),
                              instance=vm.backend_vm_id)
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEquals(db_vm.operstate, "STOPPED")
        self.assertEquals(db_vm.backendtime, new_time)

    def test_start(self, client):
        vm = mfactory.VirtualMachineFactory()
        msg = self.create_msg(operation='OP_INSTANCE_STARTUP',
                              instance=vm.backend_vm_id)
        with mocked_quotaholder():
            update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'STARTED')

    def test_stop(self, client):
        vm = mfactory.VirtualMachineFactory()
        msg = self.create_msg(operation='OP_INSTANCE_SHUTDOWN',
                              instance=vm.backend_vm_id)
        with mocked_quotaholder():
            update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'STOPPED')

    def test_reboot(self, client):
        vm = mfactory.VirtualMachineFactory()
        msg = self.create_msg(operation='OP_INSTANCE_REBOOT',
                              instance=vm.backend_vm_id)
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'STARTED')

    def test_remove(self, client):
        vm = mfactory.VirtualMachineFactory(flavor__cpu=1, flavor__ram=128)
        mfactory.VolumeFactory(userid=vm.userid, machine=vm, size=1)
        mfactory.VolumeFactory(userid=vm.userid, machine=vm, size=3)
        # Also create a NIC
        ip = mfactory.IPv4AddressFactory(nic__machine=vm)
        nic = ip.nic
        nic.network.get_ip_pools()[0].reserve(nic.ipv4_address)
        msg = self.create_msg(operation='OP_INSTANCE_REMOVE',
                              instance=vm.backend_vm_id)
        with mocked_quotaholder() as m:
            update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'DESTROYED')
        self.assertTrue(db_vm.deleted)
        # Check that nics are deleted
        self.assertFalse(db_vm.nics.all())
        self.assertTrue(nic.network.get_ip_pools()[0].is_available(ip.address))
        # Check that volumes are deleted
        self.assertFalse(db_vm.volumes.filter(deleted=False))
        # Check quotas
        name, args, kwargs = m.mock_calls[0]
        for (userid, res), value in args[1].items():
            if res == 'cyclades.disk':
                self.assertEqual(value, -4 << 30)
            elif res == 'cyclades.cpu':
                self.assertEqual(value, -1)
            elif res == 'cyclades.ram':
                self.assertEqual(value, -128 << 20)
        vm2 = mfactory.VirtualMachineFactory()
        fp1 = mfactory.IPv4AddressFactory(nic__machine=vm2, floating_ip=True,
                                          network__floating_ip_pool=True)
        network = fp1.network
        nic1 = mfactory.NetworkInterfaceFactory(machine=vm2)
        fp1.nic = nic1
        fp1.save()
        pool = network.get_ip_pools()[0]
        pool.reserve(fp1.address)
        pool.save()
        msg = self.create_msg(operation='OP_INSTANCE_REMOVE',
                              instance=vm2.backend_vm_id)
        with mocked_quotaholder():
            update_db(client, msg)
        client.basic_ack.assert_called_once()
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'DESTROYED')
        self.assertTrue(db_vm.deleted)
        self.assertEqual(IPAddress.objects.get(id=fp1.id).nic, None)
        pool = network.get_ip_pools()[0]
        # Test that floating ips are not released
        self.assertFalse(pool.is_available(fp1.address))

    @patch("synnefo.cyclades.logic.rapi_pool.GanetiRapiClient")
    def test_remove_error(self, rapi, client):
        vm = mfactory.VirtualMachineFactory()
        # Also create a NIC
        msg = self.create_msg(operation='OP_INSTANCE_REMOVE',
                              status="error",
                              instance=vm.backend_vm_id)
        rapi().GetInstance.return_value = {}
        update_db(client, msg)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertFalse(db_vm.deleted)

        rapi().GetInstance.side_effect = GanetiApiError(msg="msg",
                                                        code=503)
        update_db(client, msg)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertFalse(db_vm.deleted)

        rapi().GetInstance.side_effect = GanetiApiError(msg="msg",
                                                        code=404)
        with mocked_quotaholder():
            update_db(client, msg)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertTrue(db_vm.deleted)

    def test_create(self, client):
        vm = mfactory.VirtualMachineFactory()
        msg = self.create_msg(operation='OP_INSTANCE_CREATE',
                              instance=vm.backend_vm_id)
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'STARTED')

    def test_create_error(self, client):
        """Test that error create sets vm to ERROR state"""
        vm = mfactory.VirtualMachineFactory()
        msg = self.create_msg(operation='OP_INSTANCE_CREATE',
                              instance=vm.backend_vm_id,
                              status='error')
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'ERROR')

    def test_remove_from_error(self, client):
        """Test that error removes delete error builds"""
        vm = mfactory.VirtualMachineFactory(operstate='ERROR')
        # Also create a NIC
        mfactory.NetworkInterfaceFactory(machine=vm)
        msg = self.create_msg(operation='OP_INSTANCE_REMOVE',
                              instance=vm.backend_vm_id)
        with mocked_quotaholder():
            update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, 'DESTROYED')
        self.assertTrue(db_vm.deleted)
        # Check that nics are deleted
        self.assertFalse(db_vm.nics.all())

    def test_other_error(self, client):
        """Test that other error messages do no affect the VM"""
        vm = mfactory.VirtualMachineFactory()
        msg = self.create_msg(operation='OP_INSTANCE_STARTUP',
                              instance=vm.backend_vm_id,
                              status='error')
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, vm.operstate)
        self.assertEqual(db_vm.backendtime, vm.backendtime)

    def test_resize_msg(self, client):
        vm = mfactory.VirtualMachineFactory()
        # Test empty beparams
        for status in ["success", "error"]:
            msg = self.create_msg(operation='OP_INSTANCE_SET_PARAMS',
                                  instance=vm.backend_vm_id,
                                  job_fields={"beparams": {}},
                                  status=status)
            client.reset_mock()
            with mocked_quotaholder():
                update_db(client, msg)
            self.assertTrue(client.basic_ack.called)
            db_vm = VirtualMachine.objects.get(id=vm.id)
            self.assertEqual(db_vm.operstate, vm.operstate)
        # Test intermediate states
        vm.operstate = "STOPPED"
        vm.save()
        for status in ["queued", "waiting", "running"]:
            beparams = {"vcpus": 4, "minmem": 2048, "maxmem": 2048}
            msg = self.create_msg(operation='OP_INSTANCE_SET_PARAMS',
                                  instance=vm.backend_vm_id,
                                  job_fields={"beparams": beparams},
                                  status=status)
            client.reset_mock()
            update_db(client, msg)
            self.assertTrue(client.basic_ack.called)
            db_vm = VirtualMachine.objects.get(id=vm.id)
            self.assertEqual(db_vm.operstate, "STOPPED")
        # Test operstate after error
        msg = self.create_msg(operation='OP_INSTANCE_SET_PARAMS',
                              instance=vm.backend_vm_id,
                              beparams={"vcpus": 4},
                              status="error")
        client.reset_mock()
        with mocked_quotaholder():
            update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, "STOPPED")
        # Test success
        f1 = mfactory.FlavorFactory(cpu=4, ram=1024,
                                    volume_type__disk_template="drbd",
                                    disk=1024)
        vm.flavor = f1
        vm.save()
        f2 = mfactory.FlavorFactory(cpu=8, ram=2048,
                                    volume_type__disk_template="drbd",
                                    disk=1024)
        beparams = {"vcpus": 8, "minmem": 2048, "maxmem": 2048}
        msg = self.create_msg(operation='OP_INSTANCE_SET_PARAMS',
                              instance=vm.backend_vm_id,
                              job_fields={"beparams": beparams},
                              status="success")
        client.reset_mock()
        with mocked_quotaholder():
            update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(db_vm.operstate, "STOPPED")
        self.assertEqual(db_vm.flavor, f2)
        beparams = {"vcpus": 100, "minmem": 2048, "maxmem": 2048}
        msg = self.create_msg(operation='OP_INSTANCE_SET_PARAMS',
                              instance=vm.backend_vm_id,
                              job_fields={"beparams": beparams},
                              status="success")
        client.reset_mock()
        with mocked_quotaholder():
            update_db(client, msg)
        self.assertTrue(client.basic_reject.called)


@patch('synnefo.lib.amqp.AMQPClient')
class UpdateNetTest(TestCase):
    def create_msg(self, **kwargs):
        """Create snf-ganeti-hook message"""
        msg = {'event_time': split_time(time())}
        msg['type'] = 'ganeti-op-status'
        msg['operation'] = 'OP_INSTANCE_SET_PARAMS'
        msg['status'] = 'success'
        msg['jobId'] = 1
        msg['logmsg'] = 'Dummy Log'
        for key, val in kwargs.items():
            msg[key] = val
        message = {'body': json.dumps(msg)}
        return message

    def test_missing_attribute(self, client):
        update_db(client, json.dumps({'body': {}}))
        self.assertTrue(client.basic_reject.called)

    def test_unhandled_exception(self, client):
        update_db(client, {})
        client.basic_reject.assert_called_once()

    def test_wrong_type(self, client):
        msg = self.create_msg(type="WRONG_TYPE")
        update_db(client, msg)
        self.assertTrue(client.basic_nack.called)

    def test_missing_instance(self, client):
        msg = self.create_msg(operation='OP_INSTANCE_STARTUP',
                              instance='foo')
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)

    def test_no_nics(self, client):
        vm = mfactory.VirtualMachineFactory(operstate='ERROR')
        mfactory.NetworkInterfaceFactory(machine=vm, state="ACTIVE")
        mfactory.NetworkInterfaceFactory(machine=vm, state="ACTIVE")
        mfactory.NetworkInterfaceFactory(machine=vm, state="ACTIVE")
        self.assertEqual(len(vm.nics.all()), 3)
        msg = self.create_msg(instance_nics=[],
                              instance=vm.backend_vm_id)
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        self.assertEqual(len(db_vm.nics.all()), 0)

    def test_changed_nic(self, client):
        ip = mfactory.IPv4AddressFactory(subnet__cidr="10.0.0.0/24",
                                         address="10.0.0.2")
        network = ip.network
        subnet = ip.subnet
        vm = ip.nic.machine
        pool = subnet.get_ip_pools()[0]
        pool.reserve("10.0.0.2")
        pool.save()

        msg = self.create_msg(instance_nics=[{'network': network.backend_id,
                                              'ip': '10.0.0.3',
                                              'mac': 'aa:bb:cc:00:11:22',
                                              'name': ip.nic.backend_uuid}],
                              instance=vm.backend_vm_id)
        update_db(client, msg)
        self.assertTrue(client.basic_ack.called)
        db_vm = VirtualMachine.objects.get(id=vm.id)
        nics = db_vm.nics.all()
        self.assertEqual(len(nics), 1)
        self.assertEqual(nics[0].index, 0)
        self.assertEqual(nics[0].ipv4_address, '10.0.0.3')
        self.assertEqual(nics[0].mac, 'aa:bb:cc:00:11:22')
        pool = subnet.get_ip_pools()[0]
        self.assertTrue(pool.is_available('10.0.0.2'))
        self.assertFalse(pool.is_available('10.0.0.3'))
        pool.save()


@patch('synnefo.lib.amqp.AMQPClient')
class UpdateNetworkTest(TestCase):
    def create_msg(self, **kwargs):
        """Create snf-ganeti-eventd message"""
        msg = {'event_time': split_time(time())}
        msg['type'] = 'ganeti-network-status'
        msg['status'] = 'success'
        msg['jobId'] = 1
        msg['logmsg'] = 'Dummy Log'
        for key, val in kwargs.items():
            msg[key] = val
        message = {'body': json.dumps(msg)}
        return message

    def test_missing_attribute(self, client):
        update_network(client, json.dumps({'body': {}}))
        self.assertTrue(client.basic_reject.called)

    def test_unhandled_exception(self, client):
        update_network(client, {})
        client.basic_reject.assert_called_once()

    def test_wrong_type(self, client):
        msg = self.create_msg(type="WRONG_TYPE")
        update_network(client, msg)
        self.assertTrue(client.basic_nack.called)

    def test_missing_network(self, client):
        msg = self.create_msg(operation='OP_NETWORK_CREATE',
                              network='foo')
        update_network(client, msg)
        self.assertTrue(client.basic_ack.called)

    def test_create(self, client):
        back_network = mfactory.BackendNetworkFactory(operstate='PENDING')
        net = back_network.network
        net.state = 'ACTIVE'
        net.save()
        back1 = back_network.backend

        back_network2 = mfactory.BackendNetworkFactory(operstate='PENDING',
                                                       network=net)
        back2 = back_network2.backend
        # Message from first backend network
        msg = self.create_msg(operation='OP_NETWORK_CONNECT',
                              network=net.backend_id,
                              cluster=back1.clustername)
        update_network(client, msg)
        self.assertTrue(client.basic_ack.called)

        back_net = BackendNetwork.objects.get(id=back_network.id)
        self.assertEqual(back_net.operstate, 'ACTIVE')
        db_net = Network.objects.get(id=net.id)
        self.assertEqual(db_net.state, 'ACTIVE')
        # msg from second backend network
        msg = self.create_msg(operation='OP_NETWORK_CONNECT',
                              network=net.backend_id,
                              cluster=back2.clustername)
        update_network(client, msg)
        self.assertTrue(client.basic_ack.called)

        db_net = Network.objects.get(id=net.id)
        self.assertEqual(db_net.state, 'ACTIVE')
        back_net = BackendNetwork.objects.get(id=back_network.id)
        self.assertEqual(back_net.operstate, 'ACTIVE')

    def test_create_offline_backend(self, client):
        """Test network creation when a backend is offline"""
        net = mfactory.NetworkFactory(state='ACTIVE')
        bn1 = mfactory.BackendNetworkFactory(network=net)
        mfactory.BackendNetworkFactory(network=net,
                                       backend__offline=True)
        msg = self.create_msg(operation='OP_NETWORK_CONNECT',
                              network=net.backend_id,
                              cluster=bn1.backend.clustername)
        update_network(client, msg)
        self.assertTrue(client.basic_ack.called)
        new_net = Network.objects.get(id=net.id)
        self.assertEqual(new_net.state, 'ACTIVE')

    def test_disconnect(self, client):
        bn1 = mfactory.BackendNetworkFactory(operstate='ACTIVE')
        net1 = bn1.network
        net1.state = "ACTIVE"
        net1.state = 'ACTIVE'
        net1.save()
        bn2 = mfactory.BackendNetworkFactory(operstate='ACTIVE',
                                             network=net1)
        msg = self.create_msg(operation='OP_NETWORK_DISCONNECT',
                              network=net1.backend_id,
                              cluster=bn2.backend.clustername)
        update_network(client, msg)
        self.assertTrue(client.basic_ack.called)
        self.assertEqual(Network.objects.get(id=net1.id).state, 'ACTIVE')
        self.assertEqual(BackendNetwork.objects.get(id=bn2.id).operstate,
                         'PENDING')

    def test_remove(self, client):
        mfactory.MacPrefixPoolTableFactory()
        mfactory.BridgePoolTableFactory()
        bn = mfactory.BackendNetworkFactory(operstate='ACTIVE')
        for old_state in ['success', 'canceled', 'error']:
            for flavor in Network.FLAVORS.keys():
                bn.operstate = old_state
                bn.save()
                net = bn.network
                net.state = 'ACTIVE'
                net.flavor = flavor
                if flavor == 'PHYSICAL_VLAN':
                    net.link = allocate_resource('bridge')
                if flavor == 'MAC_FILTERED':
                    net.mac_prefix = allocate_resource('mac_prefix')
                net.save()
                msg = self.create_msg(operation='OP_NETWORK_REMOVE',
                                      network=net.backend_id,
                                      cluster=bn.backend.clustername)
                with mocked_quotaholder():
                    update_network(client, msg)
                self.assertTrue(client.basic_ack.called)
                self.assertFalse(BackendNetwork.objects.filter(id=bn.id)
                                 .exists())
                db_net = Network.objects.get(id=net.id)
                self.assertEqual(db_net.state, 'DELETED', flavor)
                self.assertTrue(db_net.deleted)
                if flavor == 'PHYSICAL_VLAN':
                    pool = BridgePoolTable.get_pool()
                    self.assertTrue(pool.is_available(net.link))
                if flavor == 'MAC_FILTERED':
                    pool = MacPrefixPoolTable.get_pool()
                    self.assertTrue(pool.is_available(net.mac_prefix))

    @patch("synnefo.cyclades.logic.rapi_pool.GanetiRapiClient")
    def test_remove_error(self, rapi, client):
        mfactory.MacPrefixPoolTableFactory()
        mfactory.BridgePoolTableFactory()
        bn = mfactory.BackendNetworkFactory(operstate='ACTIVE')
        network = bn.network
        msg = self.create_msg(operation='OP_NETWORK_REMOVE',
                              network=network.backend_id,
                              status="error",
                              cluster=bn.backend.clustername)
        rapi().GetNetwork.return_value = {}
        update_network(client, msg)
        bn = BackendNetwork.objects.get(id=bn.id)
        self.assertNotEqual(bn.operstate, "DELETED")
        rapi().GetNetwork.side_effect = GanetiApiError(msg="foo", code=404)
        with mocked_quotaholder():
            update_network(client, msg)
        self.assertFalse(BackendNetwork.objects.filter(id=bn.id) .exists())

    def test_remove_offline_backend(self, client):
        """Test network removing when a backend is offline"""
        mfactory.BridgePoolTableFactory()
        net = mfactory.NetworkFactory(flavor='PHYSICAL_VLAN',
                                      state='ACTIVE',
                                      link='prv12')
        bn1 = mfactory.BackendNetworkFactory(network=net)
        mfactory.BackendNetworkFactory(network=net,
                                       operstate="ACTIVE",
                                       backend__offline=True)
        msg = self.create_msg(operation='OP_NETWORK_REMOVE',
                              network=net.backend_id,
                              cluster=bn1.backend.clustername)
        with mocked_quotaholder():
            update_network(client, msg)
        self.assertTrue(client.basic_ack.called)
        new_net = Network.objects.get(id=net.id)
        self.assertEqual(new_net.state, 'ACTIVE')
        self.assertFalse(new_net.deleted)

    @patch("synnefo.cyclades.logic.rapi_pool.GanetiRapiClient")
    def test_error_opcode(self, rapi, client):
        # Mock getting network, because code will lookup if network exists
        # in backend
        rapi().GetNetwork.return_value = {}
        mfactory.MacPrefixPoolTableFactory()
        mfactory.BridgePoolTableFactory()
        network = mfactory.NetworkFactory()
        mfactory.BackendNetworkFactory(network=network,
                                       operstate="ACTIVE")
        for state, _ in Network.OPER_STATES:
            bn = mfactory.BackendNetworkFactory(operstate="ACTIVE",
                                                network=network)
            bn.operstate = state
            bn.save()
            network = bn.network
            network.state = state
            network.save()
            for opcode, _ in BackendNetwork.BACKEND_OPCODES:
                if opcode in ['OP_NETWORK_REMOVE', 'OP_NETWORK_ADD']:
                    continue
                msg = self.create_msg(operation=opcode,
                                      network=bn.network.backend_id,
                                      status='error',
                                      add_reserved_ips=[],
                                      remove_reserved_ips=[],
                                      cluster=bn.backend.clustername)
                with mocked_quotaholder():
                    update_network(client, msg)
                self.assertTrue(client.basic_ack.called)
                db_bnet = BackendNetwork.objects.get(id=bn.id)
                self.assertEqual(bn.operstate, db_bnet.operstate)
                self.assertEqual(bn.network.state, db_bnet.network.state)

    def test_ips(self, client):
        network = mfactory.NetworkWithSubnetFactory(subnet__cidr='10.0.0.0/24',
                                                    subnet__gateway="10.0.0.1")
        bn = mfactory.BackendNetworkFactory(network=network)
        msg = self.create_msg(operation='OP_NETWORK_SET_PARAMS',
                              network=network.backend_id,
                              cluster=bn.backend.clustername,
                              status='success',
                              job_fields={"add_reserved_ips": ["10.0.0.10",
                                                               "10.0.0.20"]})
        update_network(client, msg)
        self.assertTrue(client.basic_ack.called)
        pool = network.get_ip_pools()[0]
        self.assertTrue(pool.is_reserved('10.0.0.10'))
        self.assertTrue(pool.is_reserved('10.0.0.20'))
        pool.save()
        # Check that they are not released
        msg = self.create_msg(operation='OP_NETWORK_SET_PARAMS',
                              network=network.backend_id,
                              cluster=bn.backend.clustername,
                              job_fields={
                                  "remove_reserved_ips": ["10.0.0.10",
                                                          "10.0.0.20"]})
        update_network(client, msg)
        #self.assertTrue(client.basic_ack.called)
        pool = network.get_ip_pools()[0]
        self.assertTrue(pool.is_reserved('10.0.0.10'))
        self.assertTrue(pool.is_reserved('10.0.0.20'))


@patch('synnefo.lib.amqp.AMQPClient')
class UpdateBuildProgressTest(TestCase):
    def setUp(self):
        self.vm = mfactory.VirtualMachineFactory()

    def get_db_vm(self):
        return VirtualMachine.objects.get(id=self.vm.id)

    def create_msg(self, **kwargs):
        """Create snf-progress-monitor message"""
        msg = {'event_time': split_time(time())}
        msg['type'] = 'image-copy-progress'
        msg['progress'] = 0
        for key, val in kwargs.items():
            msg[key] = val
        message = {'body': json.dumps(msg)}
        return message

    def test_missing_attribute(self, client):
        update_build_progress(client, json.dumps({'body': {}}))
        self.assertTrue(client.basic_reject.called)

    def test_unhandled_exception(self, client):
        update_build_progress(client, {})
        client.basic_reject.assert_called_once()

    def test_missing_instance(self, client):
        msg = self.create_msg(instance='foo')
        update_build_progress(client, msg)
        self.assertTrue(client.basic_ack.called)

    def test_wrong_type(self, client):
        msg = self.create_msg(type="WRONG_TYPE")
        update_build_progress(client, msg)
        self.assertTrue(client.basic_nack.called)

    def test_progress_update(self, client):
        rprogress = randint(10, 100)
        msg = self.create_msg(progress=rprogress,
                              instance=self.vm.backend_vm_id)
        update_build_progress(client, msg)
        self.assertTrue(client.basic_ack.called)
        vm = self.get_db_vm()
        self.assertEqual(vm.buildpercentage, rprogress)

    def test_invalid_value(self, client):
        old = self.vm.buildpercentage
        for rprogress in [0, -1, 'a']:
            msg = self.create_msg(progress=rprogress,
                                  instance=self.vm.backend_vm_id)
            update_build_progress(client, msg)
            self.assertTrue(client.basic_ack.called)
            vm = self.get_db_vm()
            self.assertEqual(vm.buildpercentage, old)
