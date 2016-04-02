import unittest
import uuid
from komlog.komcass.api import interface as interfaceapi
from komlog.komcass.model.orm import interface as orminterface


class KomcassApiInterfaceTest(unittest.TestCase):
    ''' komlog.komcass.api.interface tests '''

    def test_get_user_iface_deny_non_existing_iface(self):
        ''' get_user_iface_deny should return None if iface does not exist '''
        uid=uuid.uuid4()
        iface1='test_get_user_iface_deny_non_existing_iface_iface1'
        iface2='test_get_user_iface_deny_non_existing_iface_iface2'
        perm='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, perm=perm))
        self.assertIsNone(interfaceapi.get_user_iface_deny(uid=uid, iface=iface2))

    def test_get_user_iface_deny_non_existing_uid(self):
        ''' get_user_iface_deny should return None if uid does not exist '''
        uid=uuid.uuid4()
        iface1='test_get_user_iface_deny_non_existing_uid_iface1'
        self.assertIsNone(interfaceapi.get_user_iface_deny(uid=uid, iface=iface1))

    def test_get_user_iface_deny_success(self):
        ''' get_user_iface_deny should return a UserIfaceDeny object if iface exists '''
        uid=uuid.uuid4()
        iface1='test_get_user_iface_deny_success_iface1'
        iface2='test_get_user_iface_deny_success_iface2'
        perm='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, perm=perm))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, perm=perm))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface2)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface2, iface.interface)
        self.assertEqual(perm, iface.perm)

    def test_get_user_ifaces_deny_non_existing_uid(self):
        ''' get_user_ifaces_deny should return None if uid does not exist '''
        uid=uuid.uuid4()
        ifaces=interfaceapi.get_user_ifaces_deny(uid=uid)
        self.assertEqual(ifaces, [])

    def test_get_user_ifaces_deny_success(self):
        ''' get_user_ifaces_deny should return a UserIfaceDeny objects list if uid has ifaces '''
        uid=uuid.uuid4()
        iface1='test_get_user_ifaces_deny_success_iface1'
        iface2='test_get_user_ifaces_deny_success_iface2'
        perm='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, perm=perm))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, perm=perm))
        ifaces=interfaceapi.get_user_ifaces_deny(uid=uid)
        self.assertTrue(isinstance(ifaces, list))
        self.assertEqual(len(ifaces), 2)
        self.assertTrue(isinstance(ifaces[0], orminterface.UserIfaceDeny))
        self.assertTrue(isinstance(ifaces[1], orminterface.UserIfaceDeny))

    def test_insert_user_iface_deny_success(self):
        ''' insert_user_iface_deny should return True '''
        uid=uuid.uuid4()
        iface1='test_insert_user_iface_deny_success_iface1'
        iface2='test_insert_user_iface_deny_success_iface2'
        perm='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, perm=perm))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, perm=perm))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface2)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface2, iface.interface)
        self.assertEqual(perm, iface.perm)
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface1)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface1, iface.interface)
        self.assertEqual(perm, iface.perm)

    def test_delete_user_iface_deny_success(self):
        ''' delete_user_iface_deny should return True and delete successfully the iface passed '''
        uid=uuid.uuid4()
        iface1='test_delete_user_iface_deny_success_iface1'
        iface2='test_delete_user_iface_deny_success_iface2'
        perm='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, perm=perm))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface1)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface1, iface.interface)
        self.assertEqual(perm, iface.perm)
        self.assertTrue(interfaceapi.delete_user_iface_deny(uid=uid, iface=iface1))
        self.assertIsNone(interfaceapi.get_user_iface_deny(uid=uid, iface=iface1))

    def test_delete_user_ifaces_deny_success(self):
        ''' insert_user_iface_deny should return True '''
        uid=uuid.uuid4()
        iface1='test_delete_user_ifaces_deny_success_iface1'
        iface2='test_delete_user_ifaces_deny_success_iface2'
        perm='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, perm=perm))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, perm=perm))
        ifaces=interfaceapi.get_user_ifaces_deny(uid=uid)
        self.assertTrue(isinstance(ifaces, list))
        self.assertEqual(len(ifaces), 2)
        self.assertTrue(interfaceapi.delete_user_ifaces_deny(uid=uid))
        self.assertEqual(interfaceapi.get_user_ifaces_deny(uid=uid),[])

