import unittest
import uuid
from komcass.api import quote as quoteapi
from komcass.model.orm import quote as ormquote 


class KomcassApiQuoteTest(unittest.TestCase):
    ''' komlog.komcass.api.quote tests '''

    def test_get_user_quotes_non_existing_uid(self):
        ''' get_user_quotes should return None if uid does not exist '''
        uid=uuid.uuid4()
        self.assertIsNone(quoteapi.get_user_quotes(uid=uid))

    def test_get_user_quotes_existing_quotes(self):
        ''' get_user_quotes should return a UserQuo object if uid has quotes '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_set_user_quotes_success(self):
        ''' set_user_quotes should return True and set quotes successfully '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_set_user_quote_previosly_uid_had_other_quotes(self):
        ''' set_user_quotes should return True and set quotes successfully '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        self.assertTrue(quoteapi.set_user_quote(uid=uid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        new_quotes=quotes
        new_quotes['quote4']='value4'
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_set_user_quote_previosly_uid_did_not_have_other_quotes(self):
        ''' set_user_quotes should return True and set quotes successfully '''
        uid=uuid.uuid4()
        self.assertTrue(quoteapi.set_user_quote(uid=uid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        new_quotes={'quote4':'value4'}
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_set_user_quote_previosly_uid_had_other_quotes_and_we_update_it(self):
        ''' set_user_quotes should return True and update the selected quote successfully '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        self.assertTrue(quoteapi.set_user_quote(uid=uid, quote='quote3', value='value1'))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        new_quotes=quotes
        new_quotes['quote3']='value1'
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_delete_user_quote_previosly_uid_had_the_quote(self):
        ''' delete_user_quotes should return True and delete quote properly '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        self.assertTrue(quoteapi.delete_user_quote(uid=uid, quote='quote3'))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        new_quotes=quotes
        new_quotes.pop('quote3',None)
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_delete_user_quote_previosly_uid_didnt_have_the_quote(self):
        ''' delete_user_quotes should return True and delete quote properly '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        self.assertTrue(quoteapi.delete_user_quote(uid=uid, quote='quote4'))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        new_quotes=quotes
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.uid, uid)

    def test_delete_user_quote_previosly_uid_did_not_have_any_quotes(self):
        ''' set_user_quotes should return True and set quotes successfully '''
        uid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_user_quote(uid=uid, quote='quote4'))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        self.assertIsNone(quotes_db)

    def test_delete_user_quotes_non_existing_uid(self):
        ''' delete_user_quotes should return True even if uid does not exist '''
        uid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_user_quotes(uid=uid))

    def test_delete_user_quotes_existing_quotes(self):
        ''' delete_user_quotes should return True and delete all user quotes '''
        uid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_user_quotes(uid=uid, quotes=quotes))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        self.assertTrue(isinstance(quotes_db, ormquote.UserQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.uid, uid)
        self.assertTrue(quoteapi.delete_user_quotes(uid=uid))
        self.assertIsNone(quoteapi.get_user_quotes(uid=uid))

    def test_get_agent_quotes_non_existing_aid(self):
        ''' get_agent_quotes should return None if aid does not exist '''
        aid=uuid.uuid4()
        self.assertIsNone(quoteapi.get_agent_quotes(aid=aid))

    def test_get_agent_quotes_existing_quotes(self):
        ''' get_agent_quotes should return a AgentQuo object if aid has quotes '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_set_agent_quotes_success(self):
        ''' set_agent_quotes should return True and set quotes successfully '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_set_agent_quote_previosly_aid_had_other_quotes(self):
        ''' set_agent_quotes should return True and set quotes successfully '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        new_quotes=quotes
        new_quotes['quote4']='value4'
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_set_agent_quote_previosly_aid_did_not_have_other_quotes(self):
        ''' set_agent_quotes should return True and set quotes successfully '''
        aid=uuid.uuid4()
        self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        new_quotes={'quote4':'value4'}
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_set_agent_quote_previosly_aid_had_other_quotes_and_we_update_it(self):
        ''' set_agent_quotes should return True and update the selected quote successfully '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote='quote3', value='value1'))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        new_quotes=quotes
        new_quotes['quote3']='value1'
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_delete_agent_quote_previosly_aid_had_the_quote(self):
        ''' delete_agent_quotes should return True and delete quote properly '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        self.assertTrue(quoteapi.delete_agent_quote(aid=aid, quote='quote3'))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        new_quotes=quotes
        new_quotes.pop('quote3',None)
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_delete_agent_quote_previosly_aid_didnt_have_the_quote(self):
        ''' delete_agent_quotes should return True and delete quote properly '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        self.assertTrue(quoteapi.delete_agent_quote(aid=aid, quote='quote4'))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        new_quotes=quotes
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.aid, aid)

    def test_delete_agent_quote_previosly_aid_did_not_have_any_quotes(self):
        ''' set_agent_quotes should return True and set quotes successfully '''
        aid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_agent_quote(aid=aid, quote='quote4'))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        self.assertIsNone(quotes_db)

    def test_delete_agent_quotes_non_existing_aid(self):
        ''' delete_agent_quotes should return True even if aid does not exist '''
        aid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_agent_quotes(aid=aid))

    def test_delete_agent_quotes_existing_quotes(self):
        ''' delete_agent_quotes should return True and delete all agent quotes '''
        aid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_agent_quotes(aid=aid, quotes=quotes))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        self.assertTrue(isinstance(quotes_db, ormquote.AgentQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.aid, aid)
        self.assertTrue(quoteapi.delete_agent_quotes(aid=aid))
        self.assertIsNone(quoteapi.get_agent_quotes(aid=aid))

    def test_get_datasource_quotes_non_existing_did(self):
        ''' get_datasource_quotes should return None if did does not exist '''
        did=uuid.uuid4()
        self.assertIsNone(quoteapi.get_datasource_quotes(did=did))

    def test_get_datasource_quotes_existing_quotes(self):
        ''' get_datasource_quotes should return a DatasourceQuo object if did has quotes '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.did, did)

    def test_set_datasource_quotes_success(self):
        ''' set_datasource_quotes should return True and set quotes successfully '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.did, did)

    def test_set_datasource_quote_previosly_did_had_other_quotes(self):
        ''' set_datasource_quotes should return True and set quotes successfully '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        self.assertTrue(quoteapi.set_datasource_quote(did=did, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        new_quotes=quotes
        new_quotes['quote4']='value4'
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.did, did)

    def test_set_datasource_quote_previosly_did_did_not_have_other_quotes(self):
        ''' set_datasource_quotes should return True and set quotes successfully '''
        did=uuid.uuid4()
        self.assertTrue(quoteapi.set_datasource_quote(did=did, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        new_quotes={'quote4':'value4'}
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.did, did)

    def test_set_datasource_quote_previosly_did_had_other_quotes_and_we_update_it(self):
        ''' set_datasource_quotes should return True and update the selected quote successfully '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        self.assertTrue(quoteapi.set_datasource_quote(did=did, quote='quote3', value='value1'))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        new_quotes=quotes
        new_quotes['quote3']='value1'
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.did, did)

    def test_delete_datasource_quote_previosly_did_had_the_quote(self):
        ''' delete_datasource_quotes should return True and delete quote properly '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        self.assertTrue(quoteapi.delete_datasource_quote(did=did, quote='quote3'))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        new_quotes=quotes
        new_quotes.pop('quote3',None)
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.did, did)

    def test_delete_datasource_quote_previosly_did_didnt_have_the_quote(self):
        ''' delete_datasource_quotes should return True and delete quote properly '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        self.assertTrue(quoteapi.delete_datasource_quote(did=did, quote='quote4'))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        new_quotes=quotes
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.did, did)

    def test_delete_datasource_quote_previosly_did_did_not_have_any_quotes(self):
        ''' set_datasource_quotes should return True and set quotes successfully '''
        did=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datasource_quote(did=did, quote='quote4'))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        self.assertIsNone(quotes_db)

    def test_delete_datasource_quotes_non_existing_did(self):
        ''' delete_datasource_quotes should return True even if did does not exist '''
        did=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datasource_quotes(did=did))

    def test_delete_datasource_quotes_existing_quotes(self):
        ''' delete_datasource_quotes should return True and delete all datasource quotes '''
        did=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datasource_quotes(did=did, quotes=quotes))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        self.assertTrue(isinstance(quotes_db, ormquote.DatasourceQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.did, did)
        self.assertTrue(quoteapi.delete_datasource_quotes(did=did))
        self.assertIsNone(quoteapi.get_datasource_quotes(did=did))

    def test_get_datapoint_quotes_non_existing_pid(self):
        ''' get_datapoint_quotes should return None if pid does not exist '''
        pid=uuid.uuid4()
        self.assertIsNone(quoteapi.get_datapoint_quotes(pid=pid))

    def test_get_datapoint_quotes_existing_quotes(self):
        ''' get_datapoint_quotes should return a DatapointQuo object if pid has quotes '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_set_datapoint_quotes_success(self):
        ''' set_datapoint_quotes should return True and set quotes successfully '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_set_datapoint_quote_previosly_pid_had_other_quotes(self):
        ''' set_datapoint_quotes should return True and set quotes successfully '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        new_quotes=quotes
        new_quotes['quote4']='value4'
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_set_datapoint_quote_previosly_pid_did_not_have_other_quotes(self):
        ''' set_datapoint_quotes should return True and set quotes successfully '''
        pid=uuid.uuid4()
        self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        new_quotes={'quote4':'value4'}
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_set_datapoint_quote_previosly_pid_had_other_quotes_and_we_update_it(self):
        ''' set_datapoint_quotes should return True and update the selected quote successfully '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote='quote3', value='value1'))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        new_quotes=quotes
        new_quotes['quote3']='value1'
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_delete_datapoint_quote_previosly_pid_had_the_quote(self):
        ''' delete_datapoint_quotes should return True and delete quote properly '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        self.assertTrue(quoteapi.delete_datapoint_quote(pid=pid, quote='quote3'))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        new_quotes=quotes
        new_quotes.pop('quote3',None)
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_delete_datapoint_quote_previosly_pid_pidnt_have_the_quote(self):
        ''' delete_datapoint_quotes should return True and delete quote properly '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        self.assertTrue(quoteapi.delete_datapoint_quote(pid=pid, quote='quote4'))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        new_quotes=quotes
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.pid, pid)

    def test_delete_datapoint_quote_previosly_pid_did_not_have_any_quotes(self):
        ''' set_datapoint_quotes should return True and set quotes successfully '''
        pid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datapoint_quote(pid=pid, quote='quote4'))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        self.assertIsNone(quotes_db)

    def test_delete_datapoint_quotes_non_existing_pid(self):
        ''' delete_datapoint_quotes should return True even if pid does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datapoint_quotes(pid=pid))

    def test_delete_datapoint_quotes_existing_quotes(self):
        ''' delete_datapoint_quotes should return True and delete all datapoint quotes '''
        pid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_datapoint_quotes(pid=pid, quotes=quotes))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        self.assertTrue(isinstance(quotes_db, ormquote.DatapointQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.pid, pid)
        self.assertTrue(quoteapi.delete_datapoint_quotes(pid=pid))
        self.assertIsNone(quoteapi.get_datapoint_quotes(pid=pid))

    def test_get_widget_quotes_non_existing_wid(self):
        ''' get_widget_quotes should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(quoteapi.get_widget_quotes(wid=wid))

    def test_get_widget_quotes_existing_quotes(self):
        ''' get_widget_quotes should return a WidgetQuo object if wid has quotes '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_set_widget_quotes_success(self):
        ''' set_widget_quotes should return True and set quotes successfully '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_set_widget_quote_previosly_wid_had_other_quotes(self):
        ''' set_widget_quotes should return True and set quotes successfully '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        new_quotes=quotes
        new_quotes['quote4']='value4'
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_set_widget_quote_previosly_wid_wid_not_have_other_quotes(self):
        ''' set_widget_quotes should return True and set quotes successfully '''
        wid=uuid.uuid4()
        self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        new_quotes={'quote4':'value4'}
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_set_widget_quote_previosly_wid_had_other_quotes_and_we_update_it(self):
        ''' set_widget_quotes should return True and update the selected quote successfully '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote='quote3', value='value1'))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        new_quotes=quotes
        new_quotes['quote3']='value1'
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_delete_widget_quote_previosly_wid_had_the_quote(self):
        ''' delete_widget_quotes should return True and delete quote properly '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        self.assertTrue(quoteapi.delete_widget_quote(wid=wid, quote='quote3'))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        new_quotes=quotes
        new_quotes.pop('quote3',None)
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_delete_widget_quote_previosly_wid_widnt_have_the_quote(self):
        ''' delete_widget_quotes should return True and delete quote properly '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        self.assertTrue(quoteapi.delete_widget_quote(wid=wid, quote='quote4'))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        new_quotes=quotes
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.wid, wid)

    def test_delete_widget_quote_previosly_wid_wid_not_have_any_quotes(self):
        ''' set_widget_quotes should return True and set quotes successfully '''
        wid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_widget_quote(wid=wid, quote='quote4'))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        self.assertIsNone(quotes_db)

    def test_delete_widget_quotes_non_existing_wid(self):
        ''' delete_widget_quotes should return True even if wid does not exist '''
        wid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_widget_quotes(wid=wid))

    def test_delete_widget_quotes_existing_quotes(self):
        ''' delete_widget_quotes should return True and delete all widget quotes '''
        wid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_widget_quotes(wid=wid, quotes=quotes))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        self.assertTrue(isinstance(quotes_db, ormquote.WidgetQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.wid, wid)
        self.assertTrue(quoteapi.delete_widget_quotes(wid=wid))
        self.assertIsNone(quoteapi.get_widget_quotes(wid=wid))

    def test_get_dashboard_quotes_non_existing_bid(self):
        ''' get_dashboard_quotes should return None if bid does not exist '''
        bid=uuid.uuid4()
        self.assertIsNone(quoteapi.get_dashboard_quotes(bid=bid))

    def test_get_dashboard_quotes_existing_quotes(self):
        ''' get_dashboard_quotes should return a DashboardQuo object if bid has quotes '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_set_dashboard_quotes_success(self):
        ''' set_dashboard_quotes should return True and set quotes successfully '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_set_dashboard_quote_previosly_bid_had_other_quotes(self):
        ''' set_dashboard_quotes should return True and set quotes successfully '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        new_quotes=quotes
        new_quotes['quote4']='value4'
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_set_dashboard_quote_previosly_bid_bid_not_have_other_quotes(self):
        ''' set_dashboard_quotes should return True and set quotes successfully '''
        bid=uuid.uuid4()
        self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote='quote4', value='value4'))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        new_quotes={'quote4':'value4'}
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_set_dashboard_quote_previosly_bid_had_other_quotes_and_we_update_it(self):
        ''' set_dashboard_quotes should return True and update the selected quote successfully '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote='quote3', value='value1'))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        new_quotes=quotes
        new_quotes['quote3']='value1'
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_delete_dashboard_quote_previosly_bid_had_the_quote(self):
        ''' delete_dashboard_quotes should return True and delete quote properly '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        self.assertTrue(quoteapi.delete_dashboard_quote(bid=bid, quote='quote3'))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        new_quotes=quotes
        new_quotes.pop('quote3',None)
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_delete_dashboard_quote_previosly_bid_bidnt_have_the_quote(self):
        ''' delete_dashboard_quotes should return True and delete quote properly '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        self.assertTrue(quoteapi.delete_dashboard_quote(bid=bid, quote='quote4'))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        new_quotes=quotes
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, new_quotes)
        self.assertEqual(quotes_db.bid, bid)

    def test_delete_dashboard_quote_previosly_bid_bid_not_have_any_quotes(self):
        ''' set_dashboard_quotes should return True and set quotes successfully '''
        bid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_dashboard_quote(bid=bid, quote='quote4'))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        self.assertIsNone(quotes_db)

    def test_delete_dashboard_quotes_non_existing_bid(self):
        ''' delete_dashboard_quotes should return True even if bid does not exist '''
        bid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_dashboard_quotes(bid=bid))

    def test_delete_dashboard_quotes_existing_quotes(self):
        ''' delete_dashboard_quotes should return True and delete all dashboard quotes '''
        bid=uuid.uuid4()
        quotes={'quote1':'value1', 'quote2':'value2', 'quote3':'value3'}
        self.assertTrue(quoteapi.set_dashboard_quotes(bid=bid, quotes=quotes))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        self.assertTrue(isinstance(quotes_db, ormquote.DashboardQuo))
        self.assertEqual(quotes_db.quotes, quotes)
        self.assertEqual(quotes_db.bid, bid)
        self.assertTrue(quoteapi.delete_dashboard_quotes(bid=bid))
        self.assertIsNone(quoteapi.get_dashboard_quotes(bid=bid))

