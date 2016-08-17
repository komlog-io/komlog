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
        content='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, content=content))
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
        content='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, content=content))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, content=content))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface2)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface2, iface.interface)
        self.assertEqual(content, iface.content)

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
        content='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, content=content))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, content=content))
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
        content='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, content=content))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, content=content))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface2)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface2, iface.interface)
        self.assertEqual(content, iface.content)
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface1)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface1, iface.interface)
        self.assertEqual(content, iface.content)

    def test_insert_user_iface_deny_success_content_none(self):
        ''' insert_user_iface_deny should return True '''
        uid=uuid.uuid4()
        iface1='test_insert_user_iface_deny_success_iface1'
        iface2='test_insert_user_iface_deny_success_iface2'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface2)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface2, iface.interface)
        self.assertEqual(None, iface.content)
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface1)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface1, iface.interface)
        self.assertEqual(None, iface.content)

    def test_delete_user_iface_deny_success(self):
        ''' delete_user_iface_deny should return True and delete successfully the iface passed '''
        uid=uuid.uuid4()
        iface1='test_delete_user_iface_deny_success_iface1'
        iface2='test_delete_user_iface_deny_success_iface2'
        content='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, content=content))
        iface=interfaceapi.get_user_iface_deny(uid=uid, iface=iface1)
        self.assertTrue(isinstance(iface, orminterface.UserIfaceDeny))
        self.assertEqual(uid, iface.uid)
        self.assertEqual(iface1, iface.interface)
        self.assertEqual(content, iface.content)
        self.assertTrue(interfaceapi.delete_user_iface_deny(uid=uid, iface=iface1))
        self.assertIsNone(interfaceapi.get_user_iface_deny(uid=uid, iface=iface1))

    def test_delete_user_ifaces_deny_success(self):
        ''' insert_user_iface_deny should return True '''
        uid=uuid.uuid4()
        iface1='test_delete_user_ifaces_deny_success_iface1'
        iface2='test_delete_user_ifaces_deny_success_iface2'
        content='A'
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface1, content=content))
        self.assertTrue(interfaceapi.insert_user_iface_deny(uid=uid, iface=iface2, content=content))
        ifaces=interfaceapi.get_user_ifaces_deny(uid=uid)
        self.assertTrue(isinstance(ifaces, list))
        self.assertEqual(len(ifaces), 2)
        self.assertTrue(interfaceapi.delete_user_ifaces_deny(uid=uid))
        self.assertEqual(interfaceapi.get_user_ifaces_deny(uid=uid),[])

    def test_get_user_ts_ifaces_deny_all_none_found(self):
        ''' get_user_ts_ifaces_deny should return an empty list if no interface is found '''
        uid=uuid.uuid4()
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid),[])

    def test_get_user_ts_ifaces_deny_all_some_found(self):
        ''' get_user_ts_ifaces_deny should return a list with the interfaces found  '''
        uid=uuid.uuid4()
        iface='test_interface'
        for i in range(1,1001):
            ts=i
            iface=iface+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        db_interfaces=interfaceapi.get_user_ts_ifaces_deny(uid=uid)
        self.assertEqual(len(db_interfaces),1000)

    def test_get_user_ts_ifaces_deny_iface_none_found(self):
        ''' get_user_ts_ifaces_deny should return an empty list if no interface named as the parameter is found '''
        uid=uuid.uuid4()
        iface='test_interface'
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid, iface=iface),[])
        for i in range(1,1001):
            ts=i
            iface=iface+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        iface='test_interface'
        db_interfaces=interfaceapi.get_user_ts_ifaces_deny(uid=uid, iface=iface)
        self.assertEqual(len(db_interfaces),0)

    def test_get_user_ts_ifaces_deny_iface_some_found(self):
        ''' get_user_ts_ifaces_deny should return an empty list if no interface named as the parameter is found '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        iface='test_interface500'
        db_interfaces=interfaceapi.get_user_ts_ifaces_deny(uid=uid, iface=iface)
        self.assertEqual(len(db_interfaces),1)

    def test_get_user_ts_iface_deny_none_found(self):
        ''' get_user_ts_iface_deny should return None if no interface is found '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        iface='test_interface5000'
        interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=500)
        self.assertIsNone(interface)
        iface='test_interface500'
        interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=5000)
        self.assertIsNone(interface)
        uid=uuid.uuid4()
        iface='test_interface500'
        interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=500)
        self.assertIsNone(interface)

    def test_get_user_ts_iface_deny_found(self):
        ''' get_user_ts_iface_deny should return the interface '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
            self.assertIsNotNone(interface)
            self.assertEqual(interface.uid, uid)
            self.assertEqual(interface.interface, iface)
            self.assertEqual(interface.ts, ts)
            self.assertEqual(interface.content,'a')

    def test_get_user_ts_iface_deny_interval_none_found(self):
        ''' get_user_ts_iface_deny_interval should return an empty list if no interface is found '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        iface='test_interface5000'
        interfaces=interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=0,ets=5000)
        self.assertEqual(interfaces,[])
        iface='test_interface500'
        interfaces=interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=4000,ets=5000)
        self.assertEqual(interfaces,[])
        uid=uuid.uuid4()
        iface='test_interface500'
        interfaces=interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=100, ets=1000)
        self.assertEqual(interfaces,[])

    def test_get_user_ts_iface_deny_interval_found(self):
        ''' get_user_ts_iface_deny_interval should return the interface list '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            interfaces=interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=1, ets=1001)
            self.assertEqual(len(interfaces), 1)
            self.assertEqual(interfaces[0].interface, iface)
            self.assertEqual(interfaces[0].uid,uid)
            self.assertEqual(interfaces[0].ts, ts)
            self.assertEqual(interfaces[0].content,'a')

    def test_insert_user_ts_iface_deny_success(self):
        ''' insert_user_ts_iface_deny should insert the interface '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
            self.assertIsNotNone(interface)
            self.assertEqual(interface.uid, uid)
            self.assertEqual(interface.interface, iface)
            self.assertEqual(interface.ts, ts)
            self.assertEqual(interface.content,'a')

    def test_new_user_ts_iface_deny_success(self):
        ''' new_user_ts_iface_deny should insert the interface if it does not exist previously '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.new_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
            self.assertIsNotNone(interface)
            self.assertEqual(interface.uid, uid)
            self.assertEqual(interface.interface, iface)
            self.assertEqual(interface.ts, ts)
            self.assertEqual(interface.content,'a')

    def test_new_user_ts_iface_deny_failure(self):
        ''' new_user_ts_iface_deny should fail inserting the interface if it existed previously '''
        uid=uuid.uuid4()
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.new_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            interface=interfaceapi.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
            self.assertIsNotNone(interface)
            self.assertEqual(interface.uid, uid)
            self.assertEqual(interface.interface, iface)
            self.assertEqual(interface.ts, ts)
            self.assertEqual(interface.content,'a')
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertFalse(interfaceapi.new_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))

    def test_delete_user_ts_ifaces_deny_none_existed_previously(self):
        ''' delete_user_ts_ifaces_deny should return True even if no interface existed '''
        uid=uuid.uuid4()
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid),[])
        self.assertTrue(interfaceapi.delete_user_ts_ifaces_deny(uid=uid))

    def test_delete_user_ts_ifaces_deny_success(self):
        ''' delete_user_ts_ifaces_deny should return True and delete interfaces '''
        uid=uuid.uuid4()
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid),[])
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),1000)
        self.assertTrue(interfaceapi.delete_user_ts_ifaces_deny(uid=uid))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),0)

    def test_delete_user_ts_iface_deny_without_ts_none_existed_previously(self):
        ''' delete_user_ts_iface_deny should return True even if no interface existed '''
        uid=uuid.uuid4()
        iface='test_interface'
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid, iface=iface),[])
        self.assertTrue(interfaceapi.delete_user_ts_iface_deny(uid=uid, iface=iface))

    def test_delete_user_ts_iface_deny_with_ts_none_existed_previously(self):
        ''' delete_user_ts_iface_deny should return True even if no interface existed '''
        uid=uuid.uuid4()
        iface='test_interface'
        ts=1000
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid, iface=iface),[])
        self.assertTrue(interfaceapi.delete_user_ts_iface_deny(uid=uid, iface=iface, ts=ts))

    def test_delete_user_ts_iface_deny_without_ts_success(self):
        ''' delete_user_ts_iface_deny should return True and delete interfaces '''
        uid=uuid.uuid4()
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid),[])
        for i in range(1,1001):
            ts=i
            iface='test_interface'+str(i)
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),1000)
        self.assertTrue(interfaceapi.delete_user_ts_iface_deny(uid=uid, iface=iface))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),999)

    def test_delete_user_ts_iface_deny_with_ts_success(self):
        ''' delete_user_ts_iface_deny should return True and delete interfaces '''
        uid=uuid.uuid4()
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid),[])
        iface='test_interface'
        for i in range(1,1001):
            ts=i
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),1000)
        self.assertTrue(interfaceapi.delete_user_ts_iface_deny(uid=uid, iface=iface, ts=500))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),999)

    def test_delete_user_ts_iface_deny_interval_none_existed_previously(self):
        ''' delete_user_ts_iface_deny_interval should return True even if no interface existed '''
        uid=uuid.uuid4()
        iface='test_interface'
        its=1
        ets=1000
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid, iface=iface),[])
        self.assertTrue(interfaceapi.delete_user_ts_iface_deny_interval(uid=uid, iface=iface, its=its, ets=ets))

    def test_delete_user_ts_iface_deny_interval_success(self):
        ''' delete_user_ts_iface_deny_interval should return True and delete interfaces '''
        uid=uuid.uuid4()
        self.assertEqual(interfaceapi.get_user_ts_ifaces_deny(uid=uid),[])
        iface='test_interface'
        its=100
        ets=199
        for i in range(1,1001):
            ts=i
            self.assertTrue(interfaceapi.insert_user_ts_iface_deny(uid=uid, iface=iface, ts=ts, content='a'))
        self.assertEqual(len(interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=1, ets=1000)),1000)
        self.assertTrue(interfaceapi.delete_user_ts_iface_deny_interval(uid=uid, iface=iface, its=its, ets=ets))
        self.assertEqual(len(interfaceapi.get_user_ts_ifaces_deny(uid=uid)),900)
        self.assertEqual(len(interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=1, ets=1000)),900)
        self.assertEqual(len(interfaceapi.get_user_ts_iface_deny_interval(uid=uid, iface=iface, its=its, ets=ets)),0)

