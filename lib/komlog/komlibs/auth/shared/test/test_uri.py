import unittest
import uuid
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.auth import exceptions, permissions
from komlog.komlibs.auth.shared import uri as shareduri
from komlog.komlibs.auth.errors import Errors

class AuthSharedUriTest(unittest.TestCase):
    ''' komlog.auth.shared.uri tests '''

    def test_share_uri_tree_failure_invalid_uid(self):
        ''' share_uri_tree should fail if uid is invalid '''
        uids = [None,1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        dest_uid=uuid.uuid4()
        uri='uri'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ASU_SUT_IUID)

    def test_share_uri_tree_failure_invalid_dest_uid(self):
        ''' share_uri_tree should fail if dest_uid is invalid '''
        dest_uids = [None,1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        uid=uuid.uuid4()
        uri='uri'
        for dest_uid in dest_uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ASU_SUT_IDUID)

    def test_share_uri_tree_failure_invalid_uri(self):
        ''' share_uri_tree should fail if uri is invalid '''
        uris = [None,1,22.21,'global:uri',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4(),'relative..uri']
        uid=uuid.uuid4()
        dest_uid=uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ASU_SUT_IURI)

    def test_share_uri_tree_success(self):
        ''' share_uri_tree should succeed '''
        uid=uuid.uuid4()
        dest_uid=uuid.uuid4()
        uri='uri.shared'
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
        self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)

    def test_share_uri_tree_success_already_shared(self):
        ''' share_uri_tree should succeed '''
        uid=uuid.uuid4()
        dest_uid=uuid.uuid4()
        uri='uri.shared'
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
        self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)

    def test_unshare_uri_tree_failure_invalid_uid(self):
        ''' unshare_uri_tree should fail if uid is invalid '''
        uids = [None,1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        dest_uid=uuid.uuid4()
        uri='uri'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.unshare_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ASU_USUT_IUID)

    def test_unshare_uri_tree_failure_invalid_dest_uid(self):
        ''' unshare_uri_tree should fail if dest_uid is invalid '''
        dest_uids = [1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        uid=uuid.uuid4()
        uri='uri'
        for dest_uid in dest_uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.unshare_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ASU_USUT_IDUID)

    def test_unshare_uri_tree_failure_invalid_uri(self):
        ''' unshare_uri_tree should fail if uri is invalid '''
        uris = [None,1,22.21,'global:uri',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4(),'relative..uri']
        dest_uid=uuid.uuid4()
        uid=uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.unshare_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ASU_USUT_IURI)

    def test_unshare_uri_tree_success_all_dest_uids_was_not_shared(self):
        ''' unshare_uri_tree should succeed '''
        uid=uuid.uuid4()
        dest_uid=uuid.uuid4()
        uri='uri.shared'
        not_shared_uri='uri.not_shared'
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
        self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
        self.assertTrue(shareduri.unshare_uri_tree(uid=uid, uri=not_shared_uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))

    def test_unshare_uri_tree_success_specific_dest_uid_was_not_shared(self):
        ''' unshare_uri_tree should succeed '''
        uid=uuid.uuid4()
        dest_uid=uuid.uuid4()
        uri='uri.shared'
        not_shared_uri='uri.not_shared'
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
        self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
        self.assertTrue(shareduri.unshare_uri_tree(uid=uid, uri=not_shared_uri, dest_uid=dest_uid))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))

    def test_unshare_uri_tree_success_all_dest_uids_was_shared(self):
        ''' unshare_uri_tree should succeed '''
        uid=uuid.uuid4()
        dest_uid1=uuid.uuid4()
        dest_uid2=uuid.uuid4()
        uri='uri.shared'
        not_shared_uri='uri.not_shared'
        for dest_uid in (dest_uid1,dest_uid2):
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
            self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
            perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(perm.uid, uid)
            self.assertEqual(perm.dest_uid, dest_uid)
            self.assertEqual(perm.uri, uri)
            self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
            perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
            self.assertEqual(perm.uid, dest_uid)
            self.assertEqual(perm.owner_uid, uid)
            self.assertEqual(perm.uri, uri)
            self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
        self.assertTrue(shareduri.unshare_uri_tree(uid=uid, uri=uri))
        for dest_uid in (dest_uid1,dest_uid2):
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))

    def test_unshare_uri_tree_success_specific_dest_uid_was_shared(self):
        ''' unshare_uri_tree should succeed '''
        uid=uuid.uuid4()
        dest_uid1=uuid.uuid4()
        dest_uid2=uuid.uuid4()
        uri='uri.shared'
        not_shared_uri='uri.not_shared'
        for dest_uid in (dest_uid1,dest_uid2):
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
            self.assertTrue(shareduri.share_uri_tree(uid=uid, dest_uid=dest_uid, uri=uri))
            perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertEqual(perm.uid, uid)
            self.assertEqual(perm.dest_uid, dest_uid)
            self.assertEqual(perm.uri, uri)
            self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
            perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
            self.assertEqual(perm.uid, dest_uid)
            self.assertEqual(perm.owner_uid, uid)
            self.assertEqual(perm.uri, uri)
            self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
            self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
            self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))
        self.assertTrue(shareduri.unshare_uri_tree(uid=uid, uri=uri, dest_uid=dest_uid1))
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid1, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid1, owner_uid=uid, uri=uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid1, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid1, owner_uid=uid, uri=not_shared_uri))
        perm=cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid2, uri=uri)
        self.assertEqual(perm.uid, uid)
        self.assertEqual(perm.dest_uid, dest_uid2)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        perm=cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid2, owner_uid=uid, uri=uri)
        self.assertEqual(perm.uid, dest_uid2)
        self.assertEqual(perm.owner_uid, uid)
        self.assertEqual(perm.uri, uri)
        self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
        self.assertIsNone(cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=not_shared_uri))
        self.assertIsNone(cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=not_shared_uri))

    def test_get_uris_shared_with_me_failure_invalid_uid(self):
        ''' get_uris_shared_with_me should fail if uid is invalid '''
        uids = [None,1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        owner_uid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.get_uris_shared_with_me(uid=uid, owner_uid=owner_uid)
            self.assertEqual(cm.exception.error, Errors.E_ASU_GUSWM_IUID)

    def test_get_uris_shared_with_me_failure_invalid_owner_uid(self):
        ''' get_uris_shared_with_me should fail if owner_uid is invalid '''
        owner_uids = [1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        uid=uuid.uuid4()
        for owner_uid in owner_uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.get_uris_shared_with_me(uid=uid, owner_uid=owner_uid)
            self.assertEqual(cm.exception.error, Errors.E_ASU_GUSWM_IOUID)

    def test_get_uris_shared_with_me_success_no_data_specific_owner(self):
        ''' get_uris_shared_with_me should succeed returning an array with the data '''
        uid=uuid.uuid4()
        owner_uid=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared_with_me(uid=uid, owner_uid=owner_uid),[])

    def test_get_uris_shared_with_me_success_no_data_every_owner(self):
        ''' get_uris_shared_with_me should succeed returning an array with the data '''
        uid=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared_with_me(uid=uid),[])

    def test_get_uris_shared_with_me_success_data_specific_owner(self):
        ''' get_uris_shared_with_me should succeed '''
        owner1=uuid.uuid4()
        owner2=uuid.uuid4()
        dest1=uuid.uuid4()
        dest2=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared_with_me(uid=dest1),[])
        for i in range(0,10):
            uri=owner1.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest1, uri=uri))
            uri=owner1.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest2, uri=uri))
            uri=owner2.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest1, uri=uri))
            uri=owner2.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest2, uri=uri))
        for uid in (dest1,dest2):
            for owner in (owner1,owner2):
                shares=shareduri.get_uris_shared_with_me(uid=uid, owner_uid=owner)
                self.assertEqual(len(shares),10)
                expected_shares=[]
                for i in range(0,10):
                    expected_shares.append({
                        'owner':owner,
                        'uri':owner.hex+'to'+uid.hex+str(i),
                        'perm':permissions.CAN_READ|permissions.CAN_SNAPSHOT
                    })
                self.assertEqual(sorted(shares, key=lambda x: x['uri']),sorted(expected_shares,key=lambda x:x['uri']))

    def test_get_uris_shared_with_me_success_data_all_owners(self):
        ''' get_uris_shared_with_me should succeed '''
        owner1=uuid.uuid4()
        owner2=uuid.uuid4()
        dest1=uuid.uuid4()
        dest2=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared_with_me(uid=dest1),[])
        for i in range(0,10):
            uri=owner1.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest1, uri=uri))
            uri=owner1.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest2, uri=uri))
            uri=owner2.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest1, uri=uri))
            uri=owner2.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest2, uri=uri))
        for uid in (dest1,dest2):
            shares=shareduri.get_uris_shared_with_me(uid=uid)
            self.assertEqual(len(shares),20)
            expected_shares=[]
            for i in range(0,10):
                expected_shares.append({
                    'owner':owner1,
                    'uri':owner1.hex+'to'+uid.hex+str(i),
                    'perm':permissions.CAN_READ|permissions.CAN_SNAPSHOT
                })
                expected_shares.append({
                    'owner':owner2,
                    'uri':owner2.hex+'to'+uid.hex+str(i),
                    'perm':permissions.CAN_READ|permissions.CAN_SNAPSHOT
                })
            self.assertEqual(sorted(shares, key=lambda x: x['uri']),sorted(expected_shares,key=lambda x:x['uri']))

    def test_get_uris_shared_failure_invalid_uid(self):
        ''' get_uris_shared should fail if uid is invalid '''
        uids = [None,1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        dest_uid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.get_uris_shared(uid=uid, dest_uid=dest_uid)
            self.assertEqual(cm.exception.error, Errors.E_ASU_GUS_IUID)

    def test_get_uris_shared_failure_invalid_dest_uid(self):
        ''' get_uris_shared should fail if dest_uid is invalid '''
        dest_uids = [1,22.21,'string',set(),dict(),list(),tuple(),uuid.uuid1(),uuid.uuid4().hex]
        uid=uuid.uuid4()
        for dest_uid in dest_uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                shareduri.get_uris_shared(uid=uid, dest_uid=dest_uid)
            self.assertEqual(cm.exception.error, Errors.E_ASU_GUS_IDUID)

    def test_get_uris_shared_success_no_data_specific_dest(self):
        ''' get_uris_shared should succeed returning an array with the data '''
        uid=uuid.uuid4()
        dest_uid=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared(uid=uid, dest_uid=dest_uid),[])

    def test_get_uris_shared_success_no_data_every_dest(self):
        ''' get_uris_shared should succeed returning an array with the data '''
        uid=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared(uid=uid),[])

    def test_get_uris_shared_success_data_specific_dest(self):
        ''' get_uris_shared should succeed '''
        owner1=uuid.uuid4()
        owner2=uuid.uuid4()
        dest1=uuid.uuid4()
        dest2=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared(uid=owner1),[])
        for i in range(0,10):
            uri=owner1.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest1, uri=uri))
            uri=owner1.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest2, uri=uri))
            uri=owner2.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest1, uri=uri))
            uri=owner2.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest2, uri=uri))
        for uid in (dest1,dest2):
            for owner in (owner1,owner2):
                shares=shareduri.get_uris_shared(uid=owner, dest_uid=uid)
                self.assertEqual(len(shares),10)
                expected_shares=[]
                for i in range(0,10):
                    expected_shares.append({
                        'dest':uid,
                        'uri':owner.hex+'to'+uid.hex+str(i),
                        'perm':permissions.CAN_READ|permissions.CAN_SNAPSHOT
                    })
                self.assertEqual(sorted(shares, key=lambda x: x['uri']),sorted(expected_shares,key=lambda x:x['uri']))

    def test_get_uris_shared_success_data_all_dest(self):
        ''' get_uris_shared should succeed '''
        owner1=uuid.uuid4()
        owner2=uuid.uuid4()
        dest1=uuid.uuid4()
        dest2=uuid.uuid4()
        self.assertEqual(shareduri.get_uris_shared(uid=owner1),[])
        self.assertEqual(shareduri.get_uris_shared(uid=owner2),[])
        for i in range(0,10):
            uri=owner1.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest1, uri=uri))
            uri=owner1.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner1, dest_uid=dest2, uri=uri))
            uri=owner2.hex+'to'+dest1.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest1, uri=uri))
            uri=owner2.hex+'to'+dest2.hex+str(i)
            self.assertTrue(shareduri.share_uri_tree(uid=owner2, dest_uid=dest2, uri=uri))
        for uid in (owner1,owner2):
            shares=shareduri.get_uris_shared(uid=uid)
            self.assertEqual(len(shares),20)
            expected_shares=[]
            for i in range(0,10):
                expected_shares.append({
                    'dest':dest1,
                    'uri':uid.hex+'to'+dest1.hex+str(i),
                    'perm':permissions.CAN_READ|permissions.CAN_SNAPSHOT
                })
                expected_shares.append({
                    'dest':dest2,
                    'uri':uid.hex+'to'+dest2.hex+str(i),
                    'perm':permissions.CAN_READ|permissions.CAN_SNAPSHOT
                })
            self.assertEqual(sorted(shares, key=lambda x: x['uri']),sorted(expected_shares,key=lambda x:x['uri']))

