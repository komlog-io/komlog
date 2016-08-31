import unittest
import uuid
from komlog.komcass.api import quote as quoteapi
from komlog.komcass.model.orm import quote as ormquote 


class KomcassApiQuoteTest(unittest.TestCase):
    ''' komlog.komcass.api.quote tests '''

    def test_get_user_quotes_non_existing_uid(self):
        ''' get_user_quotes should return an empty list if uid does not exist or has no quotes '''
        uid=uuid.uuid4()
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])

    def test_get_user_quotes_existing_quotes(self):
        ''' get_user_quotes should return a list of UserQuo objects if uid has quotes '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote, value=value))
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for userquote in quotes_db:
            self.assertTrue(isinstance(userquote, ormquote.UserQuo))
            self.assertTrue(userquote.quote in quote_set)
            self.assertEqual(userquote.value, quotes[userquote.quote])
            self.assertEqual(userquote.uid, uid)
            quote_set.remove(userquote.quote)

    def test_set_user_quote_success(self):
        ''' set_user_quote should return True and set the quote successfully '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.uid, uid)

    def test_set_user_quote_previously_uid_had_other_quotes(self):
        ''' set_user_quotes should return True and set quotes successfully '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.uid, uid)
        self.assertTrue(quoteapi.set_user_quote(uid=uid, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_user_quotes(uid=uid)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for userquote in quotes_db:
            self.assertTrue(isinstance(userquote, ormquote.UserQuo))
            self.assertTrue(userquote.quote in quote_set)
            self.assertEqual(userquote.value, quotes[userquote.quote])
            self.assertEqual(userquote.uid, uid)
            quote_set.remove(userquote.quote)

    def test_set_user_quote_previously_uid_had_other_quotes_and_we_update_it(self):
        ''' set_user_quotes should return True and update the selected quote successfully '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.uid, uid)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value+5))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.uid, uid)

    def test_delete_user_quote_previously_uid_had_the_quote(self):
        ''' delete_user_quote should return True and delete quote properly '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.uid, uid)
            self.assertTrue(quoteapi.delete_user_quote(uid=uid, quote=quote))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])

    def test_delete_user_quote_previously_uid_didnt_have_the_quote(self):
        ''' delete_user_quotes should return True even if quote didn't exist '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.uid, uid)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_user_quote(uid=uid, quote=quote))
        quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_user_quote_previously_uid_did_not_have_any_quotes(self):
        ''' set_user_quotes should return True and set quotes successfully '''
        uid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_user_quote(uid=uid, quote='quote4'))
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])

    def test_delete_user_quotes_non_existing_uid(self):
        ''' delete_user_quotes should return True even if uid does not exist '''
        uid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_user_quotes(uid=uid))

    def test_delete_user_quotes_existing_quotes(self):
        ''' delete_user_quotes should return True and delete all user quotes '''
        uid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_user_quote(uid=uid, quote=quote,value=value))
            quote_db=quoteapi.get_user_quote(uid=uid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.UserQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.uid, uid)
        self.assertTrue(quoteapi.delete_user_quotes(uid=uid))
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])

    def test_increment_user_quote_success_non_existent_quote(self):
        ''' increment_user_quote should increment the quote value with the value passed. If the quote did not exist previously, the value will be set to the value passed '''
        uid=uuid.uuid4()
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_user_quote(uid=uid, quote=quote))
        self.assertTrue(quoteapi.increment_user_quote(uid=uid, quote=quote, value=value))
        db_quote=quoteapi.get_user_quote(uid=uid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.uid, uid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_user_quote_success_previously_set_quote(self):
        ''' increment_user_quote should increment the quote value with the value passed. '''
        uid=uuid.uuid4()
        self.assertEqual(quoteapi.get_user_quotes(uid=uid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_user_quote(uid=uid, quote=quote))
        self.assertTrue(quoteapi.increment_user_quote(uid=uid, quote=quote, value=value))
        db_quote=quoteapi.get_user_quote(uid=uid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.uid, uid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_user_quote(uid=uid, quote=quote, value=inc_value))
        db_quote=quoteapi.get_user_quote(uid=uid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.uid, uid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_agent_quotes_non_existing_aid(self):
        ''' get_agent_quotes should return an empty list if aid does not exist or has no quotes '''
        aid=uuid.uuid4()
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])

    def test_get_agent_quotes_existing_quotes(self):
        ''' get_agent_quotes should return a list of AgentQuo objects if aid has quotes '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote, value=value))
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for agentquote in quotes_db:
            self.assertTrue(isinstance(agentquote, ormquote.AgentQuo))
            self.assertTrue(agentquote.quote in quote_set)
            self.assertEqual(agentquote.value, quotes[agentquote.quote])
            self.assertEqual(agentquote.aid, aid)
            quote_set.remove(agentquote.quote)

    def test_set_agent_quote_success(self):
        ''' set_agent_quote should return True and set the quote successfully '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.aid, aid)

    def test_set_agent_quote_previously_aid_had_other_quotes(self):
        ''' set_agent_quotes should return True and set quotes successfully '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.aid, aid)
        self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_agent_quotes(aid=aid)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for agentquote in quotes_db:
            self.assertTrue(isinstance(agentquote, ormquote.AgentQuo))
            self.assertTrue(agentquote.quote in quote_set)
            self.assertEqual(agentquote.value, quotes[agentquote.quote])
            self.assertEqual(agentquote.aid, aid)
            quote_set.remove(agentquote.quote)

    def test_set_agent_quote_previously_aid_had_other_quotes_and_we_update_it(self):
        ''' set_agent_quotes should return True and update the selected quote successfully '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.aid, aid)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value+5))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.aid, aid)

    def test_delete_agent_quote_previously_aid_had_the_quote(self):
        ''' delete_agent_quote should return True and delete quote properly '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.aid, aid)
            self.assertTrue(quoteapi.delete_agent_quote(aid=aid, quote=quote))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])

    def test_delete_agent_quote_previously_aid_didnt_have_the_quote(self):
        ''' delete_agent_quotes should return True even if quote didn't exist '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.aid, aid)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_agent_quote(aid=aid, quote=quote))
        quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_agent_quote_previously_aid_did_not_have_any_quotes(self):
        ''' set_agent_quotes should return True and set quotes successfully '''
        aid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_agent_quote(aid=aid, quote='quote4'))
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])

    def test_delete_agent_quotes_non_existing_aid(self):
        ''' delete_agent_quotes should return True even if aid does not exist '''
        aid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_agent_quotes(aid=aid))

    def test_delete_agent_quotes_existing_quotes(self):
        ''' delete_agent_quotes should return True and delete all agent quotes '''
        aid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_agent_quote(aid=aid, quote=quote,value=value))
            quote_db=quoteapi.get_agent_quote(aid=aid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.AgentQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.aid, aid)
        self.assertTrue(quoteapi.delete_agent_quotes(aid=aid))
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])

    def test_increment_agent_quote_success_non_existent_quote(self):
        ''' increment_agent_quote should increment the quote value with the value passed. If the quote did not exist previously, the value will be set to the value passed '''
        aid=uuid.uuid4()
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_agent_quote(aid=aid, quote=quote))
        self.assertTrue(quoteapi.increment_agent_quote(aid=aid, quote=quote, value=value))
        db_quote=quoteapi.get_agent_quote(aid=aid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.aid, aid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_agent_quote_success_previously_set_quote(self):
        ''' increment_agent_quote should increment the quote value with the value passed. '''
        aid=uuid.uuid4()
        self.assertEqual(quoteapi.get_agent_quotes(aid=aid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_agent_quote(aid=aid, quote=quote))
        self.assertTrue(quoteapi.increment_agent_quote(aid=aid, quote=quote, value=value))
        db_quote=quoteapi.get_agent_quote(aid=aid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.aid, aid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_agent_quote(aid=aid, quote=quote, value=inc_value))
        db_quote=quoteapi.get_agent_quote(aid=aid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.aid, aid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_datasource_quotes_non_existing_did(self):
        ''' get_datasource_quotes should return an empty list if did does not exist or has no quotes '''
        did=uuid.uuid4()
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])

    def test_get_datasource_quotes_existing_quotes(self):
        ''' get_datasource_quotes should return a list of DatasourceQuo objects if did has quotes '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote, value=value))
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for datasourcequote in quotes_db:
            self.assertTrue(isinstance(datasourcequote, ormquote.DatasourceQuo))
            self.assertTrue(datasourcequote.quote in quote_set)
            self.assertEqual(datasourcequote.value, quotes[datasourcequote.quote])
            self.assertEqual(datasourcequote.did, did)
            quote_set.remove(datasourcequote.quote)

    def test_set_datasource_quote_success(self):
        ''' set_datasource_quote should return True and set the quote successfully '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.did, did)

    def test_set_datasource_quote_previously_did_had_other_quotes(self):
        ''' set_datasource_quotes should return True and set quotes successfully '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.did, did)
        self.assertTrue(quoteapi.set_datasource_quote(did=did, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_datasource_quotes(did=did)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for datasourcequote in quotes_db:
            self.assertTrue(isinstance(datasourcequote, ormquote.DatasourceQuo))
            self.assertTrue(datasourcequote.quote in quote_set)
            self.assertEqual(datasourcequote.value, quotes[datasourcequote.quote])
            self.assertEqual(datasourcequote.did, did)
            quote_set.remove(datasourcequote.quote)

    def test_set_datasource_quote_previously_did_had_other_quotes_and_we_update_it(self):
        ''' set_datasource_quotes should return True and update the selected quote successfully '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.did, did)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value+5))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.did, did)

    def test_delete_datasource_quote_previously_did_had_the_quote(self):
        ''' delete_datasource_quote should return True and delete quote properly '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.did, did)
            self.assertTrue(quoteapi.delete_datasource_quote(did=did, quote=quote))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])

    def test_delete_datasource_quote_previously_did_didnt_have_the_quote(self):
        ''' delete_datasource_quotes should return True even if quote didn't exist '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.did, did)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_datasource_quote(did=did, quote=quote))
        quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_datasource_quote_previously_did_did_not_have_any_quotes(self):
        ''' set_datasource_quotes should return True and set quotes successfully '''
        did=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datasource_quote(did=did, quote='quote4'))
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])

    def test_delete_datasource_quotes_non_existing_did(self):
        ''' delete_datasource_quotes should return True even if did does not exist '''
        did=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datasource_quotes(did=did))

    def test_delete_datasource_quotes_existing_quotes(self):
        ''' delete_datasource_quotes should return True and delete all datasource quotes '''
        did=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datasource_quote(did=did, quote=quote,value=value))
            quote_db=quoteapi.get_datasource_quote(did=did,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatasourceQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.did, did)
        self.assertTrue(quoteapi.delete_datasource_quotes(did=did))
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])

    def test_increment_datasource_quote_success_non_existent_quote(self):
        ''' increment_datasource_quote should increment the quote value with the value passed. If the quote did not exist previously, the value will be set to the value passed '''
        did=uuid.uuid4()
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_datasource_quote(did=did, quote=quote))
        self.assertTrue(quoteapi.increment_datasource_quote(did=did, quote=quote, value=value))
        db_quote=quoteapi.get_datasource_quote(did=did, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.did, did)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_datasource_quote_success_previously_set_quote(self):
        ''' increment_datasource_quote should increment the quote value with the value passed. '''
        did=uuid.uuid4()
        self.assertEqual(quoteapi.get_datasource_quotes(did=did),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_datasource_quote(did=did, quote=quote))
        self.assertTrue(quoteapi.increment_datasource_quote(did=did, quote=quote, value=value))
        db_quote=quoteapi.get_datasource_quote(did=did, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.did, did)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_datasource_quote(did=did, quote=quote, value=inc_value))
        db_quote=quoteapi.get_datasource_quote(did=did, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.did, did)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_datapoint_quotes_non_existing_pid(self):
        ''' get_datapoint_quotes should return an empty list if pid does not exist or has no quotes '''
        pid=uuid.uuid4()
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])

    def test_get_datapoint_quotes_existing_quotes(self):
        ''' get_datapoint_quotes should return a list of DatapointQuo objects if pid has quotes '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote, value=value))
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for datapointquote in quotes_db:
            self.assertTrue(isinstance(datapointquote, ormquote.DatapointQuo))
            self.assertTrue(datapointquote.quote in quote_set)
            self.assertEqual(datapointquote.value, quotes[datapointquote.quote])
            self.assertEqual(datapointquote.pid, pid)
            quote_set.remove(datapointquote.quote)

    def test_set_datapoint_quote_success(self):
        ''' set_datapoint_quote should return True and set the quote successfully '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.pid, pid)

    def test_set_datapoint_quote_previously_pid_had_other_quotes(self):
        ''' set_datapoint_quotes should return True and set quotes successfully '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.pid, pid)
        self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_datapoint_quotes(pid=pid)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for datapointquote in quotes_db:
            self.assertTrue(isinstance(datapointquote, ormquote.DatapointQuo))
            self.assertTrue(datapointquote.quote in quote_set)
            self.assertEqual(datapointquote.value, quotes[datapointquote.quote])
            self.assertEqual(datapointquote.pid, pid)
            quote_set.remove(datapointquote.quote)

    def test_set_datapoint_quote_previously_pid_had_other_quotes_and_we_update_it(self):
        ''' set_datapoint_quotes should return True and update the selected quote successfully '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.pid, pid)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value+5))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.pid, pid)

    def test_delete_datapoint_quote_previously_pid_had_the_quote(self):
        ''' delete_datapoint_quote should return True and delete quote properly '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.pid, pid)
            self.assertTrue(quoteapi.delete_datapoint_quote(pid=pid, quote=quote))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])

    def test_delete_datapoint_quote_previously_pid_pidnt_have_the_quote(self):
        ''' delete_datapoint_quotes should return True even if quote pidn't exist '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.pid, pid)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_datapoint_quote(pid=pid, quote=quote))
        quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_datapoint_quote_previously_pid_pid_not_have_any_quotes(self):
        ''' set_datapoint_quotes should return True and set quotes successfully '''
        pid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datapoint_quote(pid=pid, quote='quote4'))
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])

    def test_delete_datapoint_quotes_non_existing_pid(self):
        ''' delete_datapoint_quotes should return True even if pid does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datapoint_quotes(pid=pid))

    def test_delete_datapoint_quotes_existing_quotes(self):
        ''' delete_datapoint_quotes should return True and delete all datapoint quotes '''
        pid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_datapoint_quote(pid=pid, quote=quote,value=value))
            quote_db=quoteapi.get_datapoint_quote(pid=pid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DatapointQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.pid, pid)
        self.assertTrue(quoteapi.delete_datapoint_quotes(pid=pid))
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])

    def test_increment_datapoint_quote_success_non_existent_quote(self):
        ''' increment_datapoint_quote should increment the quote value with the value passed. If the quote pid not exist previously, the value will be set to the value passed '''
        pid=uuid.uuid4()
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_datapoint_quote(pid=pid, quote=quote))
        self.assertTrue(quoteapi.increment_datapoint_quote(pid=pid, quote=quote, value=value))
        db_quote=quoteapi.get_datapoint_quote(pid=pid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.pid, pid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_datapoint_quote_success_previously_set_quote(self):
        ''' increment_datapoint_quote should increment the quote value with the value passed. '''
        pid=uuid.uuid4()
        self.assertEqual(quoteapi.get_datapoint_quotes(pid=pid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_datapoint_quote(pid=pid, quote=quote))
        self.assertTrue(quoteapi.increment_datapoint_quote(pid=pid, quote=quote, value=value))
        db_quote=quoteapi.get_datapoint_quote(pid=pid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.pid, pid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_datapoint_quote(pid=pid, quote=quote, value=inc_value))
        db_quote=quoteapi.get_datapoint_quote(pid=pid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.pid, pid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_widget_quotes_non_existing_wid(self):
        ''' get_widget_quotes should return an empty list if wid does not exist or has no quotes '''
        wid=uuid.uuid4()
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])

    def test_get_widget_quotes_existing_quotes(self):
        ''' get_widget_quotes should return a list of WidgetQuo objects if wid has quotes '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote, value=value))
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for widgetquote in quotes_db:
            self.assertTrue(isinstance(widgetquote, ormquote.WidgetQuo))
            self.assertTrue(widgetquote.quote in quote_set)
            self.assertEqual(widgetquote.value, quotes[widgetquote.quote])
            self.assertEqual(widgetquote.wid, wid)
            quote_set.remove(widgetquote.quote)

    def test_set_widget_quote_success(self):
        ''' set_widget_quote should return True and set the quote successfully '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.wid, wid)

    def test_set_widget_quote_previously_wid_had_other_quotes(self):
        ''' set_widget_quotes should return True and set quotes successfully '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.wid, wid)
        self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_widget_quotes(wid=wid)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for widgetquote in quotes_db:
            self.assertTrue(isinstance(widgetquote, ormquote.WidgetQuo))
            self.assertTrue(widgetquote.quote in quote_set)
            self.assertEqual(widgetquote.value, quotes[widgetquote.quote])
            self.assertEqual(widgetquote.wid, wid)
            quote_set.remove(widgetquote.quote)

    def test_set_widget_quote_previously_wid_had_other_quotes_and_we_update_it(self):
        ''' set_widget_quotes should return True and update the selected quote successfully '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.wid, wid)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value+5))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.wid, wid)

    def test_delete_widget_quote_previously_wid_had_the_quote(self):
        ''' delete_widget_quote should return True and delete quote properly '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.wid, wid)
            self.assertTrue(quoteapi.delete_widget_quote(wid=wid, quote=quote))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])

    def test_delete_widget_quote_previously_wid_widnt_have_the_quote(self):
        ''' delete_widget_quotes should return True even if quote widn't exist '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.wid, wid)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_widget_quote(wid=wid, quote=quote))
        quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_widget_quote_previously_wid_wid_not_have_any_quotes(self):
        ''' set_widget_quotes should return True and set quotes successfully '''
        wid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_widget_quote(wid=wid, quote='quote4'))
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])

    def test_delete_widget_quotes_non_existing_wid(self):
        ''' delete_widget_quotes should return True even if wid does not exist '''
        wid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_widget_quotes(wid=wid))

    def test_delete_widget_quotes_existing_quotes(self):
        ''' delete_widget_quotes should return True and delete all widget quotes '''
        wid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_widget_quote(wid=wid, quote=quote,value=value))
            quote_db=quoteapi.get_widget_quote(wid=wid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.WidgetQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.wid, wid)
        self.assertTrue(quoteapi.delete_widget_quotes(wid=wid))
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])

    def test_increment_widget_quote_success_non_existent_quote(self):
        ''' increment_widget_quote should increment the quote value with the value passed. If the quote wid not exist previously, the value will be set to the value passed '''
        wid=uuid.uuid4()
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_widget_quote(wid=wid, quote=quote))
        self.assertTrue(quoteapi.increment_widget_quote(wid=wid, quote=quote, value=value))
        db_quote=quoteapi.get_widget_quote(wid=wid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.wid, wid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_widget_quote_success_previously_set_quote(self):
        ''' increment_widget_quote should increment the quote value with the value passed. '''
        wid=uuid.uuid4()
        self.assertEqual(quoteapi.get_widget_quotes(wid=wid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_widget_quote(wid=wid, quote=quote))
        self.assertTrue(quoteapi.increment_widget_quote(wid=wid, quote=quote, value=value))
        db_quote=quoteapi.get_widget_quote(wid=wid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.wid, wid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_widget_quote(wid=wid, quote=quote, value=inc_value))
        db_quote=quoteapi.get_widget_quote(wid=wid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.wid, wid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_dashboard_quotes_non_existing_bid(self):
        ''' get_dashboard_quotes should return an empty list if bid does not exist or has no quotes '''
        bid=uuid.uuid4()
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])

    def test_get_dashboard_quotes_existing_quotes(self):
        ''' get_dashboard_quotes should return a list of DashboardQuo objects if bid has quotes '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote, value=value))
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for dashboardquote in quotes_db:
            self.assertTrue(isinstance(dashboardquote, ormquote.DashboardQuo))
            self.assertTrue(dashboardquote.quote in quote_set)
            self.assertEqual(dashboardquote.value, quotes[dashboardquote.quote])
            self.assertEqual(dashboardquote.bid, bid)
            quote_set.remove(dashboardquote.quote)

    def test_set_dashboard_quote_success(self):
        ''' set_dashboard_quote should return True and set the quote successfully '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.bid, bid)

    def test_set_dashboard_quote_previously_bid_had_other_quotes(self):
        ''' set_dashboard_quotes should return True and set quotes successfully '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.bid, bid)
        self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_dashboard_quotes(bid=bid)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for dashboardquote in quotes_db:
            self.assertTrue(isinstance(dashboardquote, ormquote.DashboardQuo))
            self.assertTrue(dashboardquote.quote in quote_set)
            self.assertEqual(dashboardquote.value, quotes[dashboardquote.quote])
            self.assertEqual(dashboardquote.bid, bid)
            quote_set.remove(dashboardquote.quote)

    def test_set_dashboard_quote_previously_bid_had_other_quotes_and_we_update_it(self):
        ''' set_dashboard_quotes should return True and update the selected quote successfully '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.bid, bid)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value+5))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.bid, bid)

    def test_delete_dashboard_quote_previously_bid_had_the_quote(self):
        ''' delete_dashboard_quote should return True and delete quote properly '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.bid, bid)
            self.assertTrue(quoteapi.delete_dashboard_quote(bid=bid, quote=quote))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])

    def test_delete_dashboard_quote_previously_bid_bidnt_have_the_quote(self):
        ''' delete_dashboard_quotes should return True even if quote bidn't exist '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.bid, bid)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_dashboard_quote(bid=bid, quote=quote))
        quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_dashboard_quote_previously_bid_bid_not_have_any_quotes(self):
        ''' set_dashboard_quotes should return True and set quotes successfully '''
        bid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_dashboard_quote(bid=bid, quote='quote4'))
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])

    def test_delete_dashboard_quotes_non_existing_bid(self):
        ''' delete_dashboard_quotes should return True even if bid does not exist '''
        bid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_dashboard_quotes(bid=bid))

    def test_delete_dashboard_quotes_existing_quotes(self):
        ''' delete_dashboard_quotes should return True and delete all dashboard quotes '''
        bid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_dashboard_quote(bid=bid, quote=quote,value=value))
            quote_db=quoteapi.get_dashboard_quote(bid=bid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.DashboardQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.bid, bid)
        self.assertTrue(quoteapi.delete_dashboard_quotes(bid=bid))
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])

    def test_increment_dashboard_quote_success_non_existent_quote(self):
        ''' increment_dashboard_quote should increment the quote value with the value passed. If the quote bid not exist previously, the value will be set to the value passed '''
        bid=uuid.uuid4()
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_dashboard_quote(bid=bid, quote=quote))
        self.assertTrue(quoteapi.increment_dashboard_quote(bid=bid, quote=quote, value=value))
        db_quote=quoteapi.get_dashboard_quote(bid=bid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.bid, bid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_dashboard_quote_success_previously_set_quote(self):
        ''' increment_dashboard_quote should increment the quote value with the value passed. '''
        bid=uuid.uuid4()
        self.assertEqual(quoteapi.get_dashboard_quotes(bid=bid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_dashboard_quote(bid=bid, quote=quote))
        self.assertTrue(quoteapi.increment_dashboard_quote(bid=bid, quote=quote, value=value))
        db_quote=quoteapi.get_dashboard_quote(bid=bid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.bid, bid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_dashboard_quote(bid=bid, quote=quote, value=inc_value))
        db_quote=quoteapi.get_dashboard_quote(bid=bid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.bid, bid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_circle_quotes_non_existing_cid(self):
        ''' get_circle_quotes should return an empty list if cid does not exist or has no quotes '''
        cid=uuid.uuid4()
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])

    def test_get_circle_quotes_existing_quotes(self):
        ''' get_circle_quotes should return a list of CircleQuo objects if cid has quotes '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote, value=value))
        quotes_db=quoteapi.get_circle_quotes(cid=cid)
        self.assertEqual(len(quotes_db),3)
        quote_set=set(quotes.keys())
        for circlequote in quotes_db:
            self.assertTrue(isinstance(circlequote, ormquote.CircleQuo))
            self.assertTrue(circlequote.quote in quote_set)
            self.assertEqual(circlequote.value, quotes[circlequote.quote])
            self.assertEqual(circlequote.cid, cid)
            quote_set.remove(circlequote.quote)

    def test_set_circle_quote_success(self):
        ''' set_circle_quote should return True and set the quote successfully '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.cid, cid)

    def test_set_circle_quote_previously_cid_had_other_quotes(self):
        ''' set_circle_quotes should return True and set quotes successfully '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.cid, cid)
        self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote='quote4',value=5))
        quotes['quote4']=5
        quotes_db=quoteapi.get_circle_quotes(cid=cid)
        self.assertEqual(len(quotes_db),4)
        quote_set=set(quotes.keys())
        for circlequote in quotes_db:
            self.assertTrue(isinstance(circlequote, ormquote.CircleQuo))
            self.assertTrue(circlequote.quote in quote_set)
            self.assertEqual(circlequote.value, quotes[circlequote.quote])
            self.assertEqual(circlequote.cid, cid)
            quote_set.remove(circlequote.quote)

    def test_set_circle_quote_previously_cid_had_other_quotes_and_we_update_it(self):
        ''' set_circle_quotes should return True and update the selected quote successfully '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.cid, cid)
        for quote,value in quotes.items():
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value+5))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value+5)
            self.assertEqual(quote_db.cid, cid)

    def test_delete_circle_quote_previously_cid_had_the_quote(self):
        ''' delete_circle_quote should return True and delete quote properly '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.cid, cid)
            self.assertTrue(quoteapi.delete_circle_quote(cid=cid, quote=quote))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])

    def test_delete_circle_quote_previously_cid_cidnt_have_the_quote(self):
        ''' delete_circle_quotes should return True even if quote cidn't exist '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.cid, cid)
        quote='nonexistent_quote'
        self.assertTrue(quoteapi.delete_circle_quote(cid=cid, quote=quote))
        quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
        self.assertIsNone(quote_db)

    def test_delete_circle_quote_previously_cid_cid_not_have_any_quotes(self):
        ''' set_circle_quotes should return True and set quotes successfully '''
        cid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_circle_quote(cid=cid, quote='quote4'))
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])

    def test_delete_circle_quotes_non_existing_cid(self):
        ''' delete_circle_quotes should return True even if cid does not exist '''
        cid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_circle_quotes(cid=cid))

    def test_delete_circle_quotes_existing_quotes(self):
        ''' delete_circle_quotes should return True and delete all circle quotes '''
        cid=uuid.uuid4()
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        for quote,value in quotes.items():
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertIsNone(quote_db)
            self.assertTrue(quoteapi.set_circle_quote(cid=cid, quote=quote,value=value))
            quote_db=quoteapi.get_circle_quote(cid=cid,quote=quote)
            self.assertTrue(isinstance(quote_db, ormquote.CircleQuo))
            self.assertEqual(quote_db.quote, quote)
            self.assertEqual(quote_db.value, value)
            self.assertEqual(quote_db.cid, cid)
        self.assertTrue(quoteapi.delete_circle_quotes(cid=cid))
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])

    def test_increment_circle_quote_success_non_existent_quote(self):
        ''' increment_circle_quote should increment the quote value with the value passed. If the quote cid not exist previously, the value will be set to the value passed '''
        cid=uuid.uuid4()
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_circle_quote(cid=cid, quote=quote))
        self.assertTrue(quoteapi.increment_circle_quote(cid=cid, quote=quote, value=value))
        db_quote=quoteapi.get_circle_quote(cid=cid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.cid, cid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)

    def test_increment_circle_quote_success_previously_set_quote(self):
        ''' increment_circle_quote should increment the quote value with the value passed. '''
        cid=uuid.uuid4()
        self.assertEqual(quoteapi.get_circle_quotes(cid=cid),[])
        quote='quote'
        value=1000
        self.assertIsNone(quoteapi.get_circle_quote(cid=cid, quote=quote))
        self.assertTrue(quoteapi.increment_circle_quote(cid=cid, quote=quote, value=value))
        db_quote=quoteapi.get_circle_quote(cid=cid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.cid, cid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value)
        inc_value=1000
        self.assertTrue(quoteapi.increment_circle_quote(cid=cid, quote=quote, value=inc_value))
        db_quote=quoteapi.get_circle_quote(cid=cid, quote=quote)
        self.assertIsNotNone(db_quote)
        self.assertEqual(db_quote.cid, cid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.value,value+inc_value)

    def test_get_user_ts_quotes_none_found(self):
        ''' get_user_ts_quotes should return an empty array if no quote is found '''
        uid=uuid.uuid4()
        self.assertEqual(quoteapi.get_user_ts_quotes(uid=uid),[])

    def test_get_user_ts_quotes_none_found_with_that_quote_name(self):
        ''' get_user_ts_quotes should return an empty array if no quote is found '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=1
        self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        quotedb=quoteapi.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotedb),1)
        self.assertEqual(quotedb[0].uid, uid)
        self.assertEqual(quotedb[0].quote,quote)
        self.assertEqual(quotedb[0].ts,ts)
        self.assertEqual(quotedb[0].value,value)
        quote='quote2'
        self.assertEqual(quoteapi.get_user_ts_quotes(uid=uid, quote=quote),[])

    def test_get_user_ts_quotes_only_retrieve_last_one(self):
        ''' get_user_ts_quotes should retrieve the last ts of a quote if count is 1 '''
        uid=uuid.uuid4()
        quote='quote'
        for i in range(1,1001):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, i,i))
        for i in range(2000,1001,-1):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, i,i))
        db_quote=quoteapi.get_user_ts_quotes(uid=uid, quote=quote, count=1)
        self.assertEqual(len(db_quote),1)
        self.assertEqual(db_quote[0].uid,uid)
        self.assertEqual(db_quote[0].quote,quote)
        self.assertEqual(db_quote[0].ts,2000)
        self.assertEqual(db_quote[0].value,2000)

    def test_get_user_ts_quote_none_found(self):
        ''' get_user_ts_quote should return None if no quote is found '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        self.assertIsNotNone(quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=ts))
        self.assertIsNone(quoteapi.get_user_ts_quote(uid=uuid.uuid4(), quote=quote, ts=ts))
        self.assertIsNone(quoteapi.get_user_ts_quote(uid=uid, quote='quote2', ts=ts))
        self.assertIsNone(quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=2))

    def test_get_user_ts_quote_found(self):
        ''' get_user_ts_quote should return the quote object '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        quotedb=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=ts)
        self.assertTrue(isinstance(quotedb, ormquote.UserTsQuo))
        self.assertEqual(quotedb.uid, uid)
        self.assertEqual(quotedb.quote,quote)
        self.assertEqual(quotedb.ts,ts)
        self.assertEqual(quotedb.value,value)

    def test_get_user_ts_quote_interval_none_found(self):
        ''' get_user_ts_quotes should return an empty array if no quote is found '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        self.assertNotEqual(quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=50,ets=60),[])
        self.assertEqual(quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=101, ets=200),[])
        self.assertEqual(quoteapi.get_user_ts_quote_interval(uid=uuid.uuid4(), quote=quote, its=10, ets=20),[])
        self.assertEqual(quoteapi.get_user_ts_quote_interval(uid=uid, quote='quote2', its=10, ets=20),[])
        self.assertEqual(quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=50, ets=10),[])

    def test_get_user_ts_quote_interval_found(self):
        ''' get_user_ts_quotes should return an empty array if no quote is found '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=11)
        self.assertEqual(len(db_quotes),2)
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=1, ets=1000)
        self.assertEqual(len(db_quotes),90)
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=10)
        self.assertEqual(len(db_quotes),1)

    def test_get_user_ts_quote_value_sum_no_uid_found(self):
        ''' get_user_ts_quote_value_sum should return 0 if uid is not found '''
        uid=uuid.uuid4()
        quote='quote'
        self.assertEqual(quoteapi.get_user_ts_quote_value_sum(uid=uid, quote=quote), 0)

    def test_get_user_ts_quote_value_sum_no_quote_found(self):
        ''' get_user_ts_quote_value_sum should return 0 if quote is not found '''
        uid=uuid.uuid4()
        quote='quote'
        for i in range(1,100):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, i,i))
        quote='non_existent'
        self.assertEqual(quoteapi.get_user_ts_quote_value_sum(uid=uid, quote=quote), 0)

    def test_get_user_ts_quote_value_sum_found(self):
        ''' get_user_ts_quote_value_sum should return the sum of the selected rows value '''
        uid=uuid.uuid4()
        quote='quote'
        value=1
        for i in range(1,101):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, i,value))
        self.assertEqual(quoteapi.get_user_ts_quote_value_sum(uid=uid, quote=quote), 100)

    def test_insert_user_ts_quote_success(self):
        ''' insert_user_ts_quote should succeed and insert the quote '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.UserTsQuo))
        self.assertEqual(db_quote.uid, uid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)

    def test_new_user_ts_quote_success(self):
        ''' new_user_ts_quote should succeed if quote didnt exist previously '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.new_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.UserTsQuo))
        self.assertEqual(db_quote.uid, uid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)

    def test_new_user_ts_quote_failed(self):
        ''' new_user_ts_quote should fail if quote did exist previously '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.new_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.UserTsQuo))
        self.assertEqual(db_quote.uid, uid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)
        self.assertFalse(quoteapi.new_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value))

    def test_delete_user_ts_quotes_no_previous_quotes(self):
        ''' delete_user_ts_quotes should succeed even if no quote existed '''
        uid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_user_ts_quotes(uid=uid))

    def test_delete_user_ts_quotes_previous_existing_quotes(self):
        ''' delete_user_ts_quotes should delete all uid ts quotes '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_user_ts_quotes(uid=uid))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_delete_user_ts_quote_no_previous_quote(self):
        ''' delete_user_ts_quote should succeed even if no quote existed '''
        uid=uuid.uuid4()
        quote='quote'
        ts=1
        self.assertTrue(quoteapi.delete_user_ts_quote(uid=uid, quote=quote))
        self.assertTrue(quoteapi.delete_user_ts_quote(uid=uid, quote=quote, ts=ts))

    def test_delete_user_ts_quote_previous_existing_quote(self):
        ''' delete_user_ts_quote should delete the quote '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_user_ts_quote(uid=uid, quote=quote, ts=10))
        self.assertIsNone(quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=10))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),89)
        self.assertTrue(quoteapi.delete_user_ts_quote(uid=uid, quote=quote))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_delete_user_ts_quote_interval_no_previous_quote(self):
        ''' delete_user_ts_quote_interval should succeed even if no quote existed '''
        uid=uuid.uuid4()
        quote='quote'
        its=1
        ets=1000
        self.assertTrue(quoteapi.delete_user_ts_quote_interval(uid=uid, quote=quote, its=its, ets=ets))

    def test_delete_user_ts_quote_interval_previously_existing_quote(self):
        ''' delete_user_ts_quote_interval should delete the quote interval '''
        uid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_user_ts_quote(uid, quote, ts, value))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=19))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),80)
        self.assertTrue(quoteapi.delete_user_ts_quote_interval(uid=uid, quote=quote, its=100, ets=190))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),80)
        self.assertTrue(quoteapi.delete_user_ts_quote_interval(uid=uid, quote=quote, its=0, ets=190))
        db_quotes=quoteapi.get_user_ts_quote_interval(uid=uid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_increment_user_ts_quote_non_existent_quote(self):
        ''' increment_user_ts_quote should set the quote value if the quote did not exist previously '''
        uid = uuid.uuid4()
        quote='quote'
        ts=1000
        value=5000
        value_set=quoteapi.increment_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value)
        quote_db=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=1000)
        self.assertEqual(quote_db.uid, uid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value)

    def test_increment_user_ts_quote_previously_existent_quote(self):
        ''' increment_user_ts_quote should add the value to the actual quote value '''
        uid = uuid.uuid4()
        quote='quote'
        ts=1000
        value=5000
        value_set=quoteapi.increment_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value)
        quote_db=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=1000)
        self.assertEqual(quote_db.uid, uid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value)
        for i in range(0,100):
            value_set=quoteapi.increment_user_ts_quote(uid=uid, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value+100*value)
        quote_db=quoteapi.get_user_ts_quote(uid=uid, quote=quote, ts=1000)
        self.assertEqual(quote_db.uid, uid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value+100*value)

    def test_get_datasource_ts_quotes_none_found(self):
        ''' get_datasource_ts_quotes should return an empty array if no quote is found '''
        did=uuid.uuid4()
        self.assertEqual(quoteapi.get_datasource_ts_quotes(did=did),[])

    def test_get_datasource_ts_quotes_none_found_with_that_quote_name(self):
        ''' get_datasource_ts_quotes should return an empty array if no quote is found '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=1
        self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        quotedb=quoteapi.get_datasource_ts_quotes(did=did, quote=quote)
        self.assertEqual(len(quotedb),1)
        self.assertEqual(quotedb[0].did, did)
        self.assertEqual(quotedb[0].quote,quote)
        self.assertEqual(quotedb[0].ts,ts)
        self.assertEqual(quotedb[0].value,value)
        quote='quote2'
        self.assertEqual(quoteapi.get_datasource_ts_quotes(did=did, quote=quote),[])

    def test_get_datasource_ts_quotes_only_retrieve_last_one(self):
        ''' get_datasource_ts_quotes should retrieve the last ts of a quote if count is 1 
            because quo_ts_datasource table is created WITH CLUSTERING ORDER BY (quote asc,ts desc)
        '''
        did=uuid.uuid4()
        quote='quote'
        for i in range(1,1001):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, i,i))
        for i in range(2000,1001,-1):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, i,i))
        db_quote=quoteapi.get_datasource_ts_quotes(did=did, quote=quote, count=1)
        self.assertEqual(len(db_quote),1)
        self.assertEqual(db_quote[0].did,did)
        self.assertEqual(db_quote[0].quote,quote)
        self.assertEqual(db_quote[0].ts,2000)
        self.assertEqual(db_quote[0].value,2000)

    def test_get_datasource_ts_quote_none_found(self):
        ''' get_datasource_ts_quote should return None if no quote is found '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        self.assertIsNotNone(quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=ts))
        self.assertIsNone(quoteapi.get_datasource_ts_quote(did=uuid.uuid4(), quote=quote, ts=ts))
        self.assertIsNone(quoteapi.get_datasource_ts_quote(did=did, quote='quote2', ts=ts))
        self.assertIsNone(quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=2))

    def test_get_datasource_ts_quote_found(self):
        ''' get_datasource_ts_quote should return the quote object '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        quotedb=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=ts)
        self.assertTrue(isinstance(quotedb, ormquote.DatasourceTsQuo))
        self.assertEqual(quotedb.did, did)
        self.assertEqual(quotedb.quote,quote)
        self.assertEqual(quotedb.ts,ts)
        self.assertEqual(quotedb.value,value)

    def test_get_datasource_ts_quote_interval_none_found(self):
        ''' get_datasource_ts_quotes should return an empty array if no quote is found '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        self.assertNotEqual(quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=50,ets=60),[])
        self.assertEqual(quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=101, ets=200),[])
        self.assertEqual(quoteapi.get_datasource_ts_quote_interval(did=uuid.uuid4(), quote=quote, its=10, ets=20),[])
        self.assertEqual(quoteapi.get_datasource_ts_quote_interval(did=did, quote='quote2', its=10, ets=20),[])
        self.assertEqual(quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=50, ets=10),[])

    def test_get_datasource_ts_quote_interval_found(self):
        ''' get_datasource_ts_quotes should return an empty array if no quote is found '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=11)
        self.assertEqual(len(db_quotes),2)
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=1, ets=1000)
        self.assertEqual(len(db_quotes),90)
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=10)
        self.assertEqual(len(db_quotes),1)

    def test_get_datasource_ts_quote_value_sum_no_did_found(self):
        ''' get_datasource_ts_quote_value_sum should return 0 if did is not found '''
        did=uuid.uuid4()
        quote='quote'
        self.assertEqual(quoteapi.get_datasource_ts_quote_value_sum(did=did, quote=quote), 0)

    def test_get_datasource_ts_quote_value_sum_no_quote_found(self):
        ''' get_datasource_ts_quote_value_sum should return 0 if quote is not found '''
        did=uuid.uuid4()
        quote='quote'
        for i in range(1,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, i,i))
        quote='non_existent'
        self.assertEqual(quoteapi.get_datasource_ts_quote_value_sum(did=did, quote=quote), 0)

    def test_get_datasource_ts_quote_value_sum_quote_found(self):
        ''' get_datasource_ts_quote_value_sum should return the quote sum '''
        did=uuid.uuid4()
        quote='quote'
        result=0
        for i in range(1,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, i,i))
            result+=i
        self.assertEqual(quoteapi.get_datasource_ts_quote_value_sum(did=did, quote=quote), result)

    def test_insert_datasource_ts_quote_success(self):
        ''' insert_datasource_ts_quote should succeed and insert the quote '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.DatasourceTsQuo))
        self.assertEqual(db_quote.did, did)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)

    def test_new_datasource_ts_quote_success(self):
        ''' new_datasource_ts_quote should succeed if quote didnt exist previously '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.new_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.DatasourceTsQuo))
        self.assertEqual(db_quote.did, did)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)

    def test_new_datasource_ts_quote_failed(self):
        ''' new_datasource_ts_quote should fail if quote did exist previously '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.new_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.DatasourceTsQuo))
        self.assertEqual(db_quote.did, did)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)
        self.assertFalse(quoteapi.new_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value))

    def test_delete_datasource_ts_quotes_no_previous_quotes(self):
        ''' delete_datasource_ts_quotes should succeed even if no quote existed '''
        did=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datasource_ts_quotes(did=did))

    def test_delete_datasource_ts_quotes_previous_existing_quotes(self):
        ''' delete_datasource_ts_quotes should delete all did ts quotes '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_datasource_ts_quotes(did=did))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_delete_datasource_ts_quote_no_previous_quote(self):
        ''' delete_datasource_ts_quote should succeed even if no quote existed '''
        did=uuid.uuid4()
        quote='quote'
        ts=1
        self.assertTrue(quoteapi.delete_datasource_ts_quote(did=did, quote=quote))
        self.assertTrue(quoteapi.delete_datasource_ts_quote(did=did, quote=quote, ts=ts))

    def test_delete_datasource_ts_quote_previous_existing_quote(self):
        ''' delete_datasource_ts_quote should delete the quote '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_datasource_ts_quote(did=did, quote=quote, ts=10))
        self.assertIsNone(quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=10))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),89)
        self.assertTrue(quoteapi.delete_datasource_ts_quote(did=did, quote=quote))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_delete_datasource_ts_quote_interval_no_previous_quote(self):
        ''' delete_datasource_ts_quote_interval should succeed even if no quote existed '''
        did=uuid.uuid4()
        quote='quote'
        its=1
        ets=1000
        self.assertTrue(quoteapi.delete_datasource_ts_quote_interval(did=did, quote=quote, its=its, ets=ets))

    def test_delete_datasource_ts_quote_interval_previously_existing_quote(self):
        ''' delete_datasource_ts_quote_interval should delete the quote interval '''
        did=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datasource_ts_quote(did, quote, ts, value))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=19))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),80)
        self.assertTrue(quoteapi.delete_datasource_ts_quote_interval(did=did, quote=quote, its=100, ets=190))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),80)
        self.assertTrue(quoteapi.delete_datasource_ts_quote_interval(did=did, quote=quote, its=0, ets=190))
        db_quotes=quoteapi.get_datasource_ts_quote_interval(did=did, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_increment_datasource_ts_quote_non_existent_quote(self):
        ''' increment_datasource_ts_quote should set the quote value if the quote did not exist previously '''
        did = uuid.uuid4()
        quote='quote'
        ts=1000
        value=5000
        value_set=quoteapi.increment_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value)
        quote_db=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=1000)
        self.assertEqual(quote_db.did, did)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value)

    def test_increment_datasource_ts_quote_previously_existent_quote(self):
        ''' increment_datasource_ts_quote should add the value to the actual quote value '''
        did = uuid.uuid4()
        quote='quote'
        ts=1000
        value=5000
        value_set=quoteapi.increment_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value)
        quote_db=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=1000)
        self.assertEqual(quote_db.did, did)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value)
        for i in range(0,100):
            value_set=quoteapi.increment_datasource_ts_quote(did=did, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value+100*value)
        quote_db=quoteapi.get_datasource_ts_quote(did=did, quote=quote, ts=1000)
        self.assertEqual(quote_db.did, did)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value+100*value)

    def test_get_datapoint_ts_quotes_none_found(self):
        ''' get_datapoint_ts_quotes should return an empty array if no quote is found '''
        pid=uuid.uuid4()
        self.assertEqual(quoteapi.get_datapoint_ts_quotes(pid=pid),[])

    def test_get_datapoint_ts_quotes_none_found_with_that_quote_name(self):
        ''' get_datapoint_ts_quotes should return an empty array if no quote is found '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=1
        self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        quotedb=quoteapi.get_datapoint_ts_quotes(pid=pid, quote=quote)
        self.assertEqual(len(quotedb),1)
        self.assertEqual(quotedb[0].pid, pid)
        self.assertEqual(quotedb[0].quote,quote)
        self.assertEqual(quotedb[0].ts,ts)
        self.assertEqual(quotedb[0].value,value)
        quote='quote2'
        self.assertEqual(quoteapi.get_datapoint_ts_quotes(pid=pid, quote=quote),[])

    def test_get_datapoint_ts_quotes_only_retrieve_last_one(self):
        ''' get_datapoint_ts_quotes should retrieve the last ts of a quote if count is 1 
            because quo_ts_datapoint table is created WITH CLUSTERING ORDER BY (quote asc,ts desc)
        '''
        pid=uuid.uuid4()
        quote='quote'
        for i in range(1,1001):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, i,i))
        for i in range(2000,1001,-1):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, i,i))
        db_quote=quoteapi.get_datapoint_ts_quotes(pid=pid, quote=quote, count=1)
        self.assertEqual(len(db_quote),1)
        self.assertEqual(db_quote[0].pid,pid)
        self.assertEqual(db_quote[0].quote,quote)
        self.assertEqual(db_quote[0].ts,2000)
        self.assertEqual(db_quote[0].value,2000)

    def test_get_datapoint_ts_quote_none_found(self):
        ''' get_datapoint_ts_quote should return None if no quote is found '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        self.assertIsNotNone(quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=ts))
        self.assertIsNone(quoteapi.get_datapoint_ts_quote(pid=uuid.uuid4(), quote=quote, ts=ts))
        self.assertIsNone(quoteapi.get_datapoint_ts_quote(pid=pid, quote='quote2', ts=ts))
        self.assertIsNone(quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=2))

    def test_get_datapoint_ts_quote_found(self):
        ''' get_datapoint_ts_quote should return the quote object '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        quotedb=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=ts)
        self.assertTrue(isinstance(quotedb, ormquote.DatapointTsQuo))
        self.assertEqual(quotedb.pid, pid)
        self.assertEqual(quotedb.quote,quote)
        self.assertEqual(quotedb.ts,ts)
        self.assertEqual(quotedb.value,value)

    def test_get_datapoint_ts_quote_interval_none_found(self):
        ''' get_datapoint_ts_quotes should return an empty array if no quote is found '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        self.assertNotEqual(quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=50,ets=60),[])
        self.assertEqual(quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=101, ets=200),[])
        self.assertEqual(quoteapi.get_datapoint_ts_quote_interval(pid=uuid.uuid4(), quote=quote, its=10, ets=20),[])
        self.assertEqual(quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote='quote2', its=10, ets=20),[])
        self.assertEqual(quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=50, ets=10),[])

    def test_get_datapoint_ts_quote_interval_found(self):
        ''' get_datapoint_ts_quotes should return an empty array if no quote is found '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=11)
        self.assertEqual(len(db_quotes),2)
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=1, ets=1000)
        self.assertEqual(len(db_quotes),90)
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=10)
        self.assertEqual(len(db_quotes),1)

    def test_get_datapoint_ts_quote_value_sum_no_pid_found(self):
        ''' get_datapoint_ts_quote_value_sum should return 0 if pid is not found '''
        pid=uuid.uuid4()
        quote='quote'
        self.assertEqual(quoteapi.get_datapoint_ts_quote_value_sum(pid=pid, quote=quote), 0)

    def test_get_datapoint_ts_quote_value_sum_no_quote_found(self):
        ''' get_datapoint_ts_quote_value_sum should return 0 if quote is not found '''
        pid=uuid.uuid4()
        quote='quote'
        for i in range(1,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, i,i))
        quote='non_existent'
        self.assertEqual(quoteapi.get_datapoint_ts_quote_value_sum(pid=pid, quote=quote), 0)

    def test_get_datapoint_ts_quote_value_sum_quote_found(self):
        ''' get_datapoint_ts_quote_value_sum should return the quote value sum '''
        pid=uuid.uuid4()
        quote='quote'
        result=0
        for i in range(1,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, i,i))
            result+=i
        self.assertEqual(quoteapi.get_datapoint_ts_quote_value_sum(pid=pid, quote=quote), result)

    def test_insert_datapoint_ts_quote_success(self):
        ''' insert_datapoint_ts_quote should succeed and insert the quote '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.DatapointTsQuo))
        self.assertEqual(db_quote.pid, pid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)

    def test_new_datapoint_ts_quote_success(self):
        ''' new_datapoint_ts_quote should succeed if quote didnt exist previously '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.new_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.DatapointTsQuo))
        self.assertEqual(db_quote.pid, pid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)

    def test_new_datapoint_ts_quote_failed(self):
        ''' new_datapoint_ts_quote should fail if quote did exist previously '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        self.assertTrue(quoteapi.new_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value))
        db_quote=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=ts)
        self.assertTrue(isinstance(db_quote,ormquote.DatapointTsQuo))
        self.assertEqual(db_quote.pid, pid)
        self.assertEqual(db_quote.quote,quote)
        self.assertEqual(db_quote.ts,ts)
        self.assertEqual(db_quote.value,value)
        self.assertFalse(quoteapi.new_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value))

    def test_delete_datapoint_ts_quotes_no_previous_quotes(self):
        ''' delete_datapoint_ts_quotes should succeed even if no quote existed '''
        pid=uuid.uuid4()
        self.assertTrue(quoteapi.delete_datapoint_ts_quotes(pid=pid))

    def test_delete_datapoint_ts_quotes_previous_existing_quotes(self):
        ''' delete_datapoint_ts_quotes should delete all pid ts quotes '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_datapoint_ts_quotes(pid=pid))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_delete_datapoint_ts_quote_no_previous_quote(self):
        ''' delete_datapoint_ts_quote should succeed even if no quote existed '''
        pid=uuid.uuid4()
        quote='quote'
        ts=1
        self.assertTrue(quoteapi.delete_datapoint_ts_quote(pid=pid, quote=quote))
        self.assertTrue(quoteapi.delete_datapoint_ts_quote(pid=pid, quote=quote, ts=ts))

    def test_delete_datapoint_ts_quote_previous_existing_quote(self):
        ''' delete_datapoint_ts_quote should delete the quote '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_datapoint_ts_quote(pid=pid, quote=quote, ts=10))
        self.assertIsNone(quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=10))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),89)
        self.assertTrue(quoteapi.delete_datapoint_ts_quote(pid=pid, quote=quote))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_delete_datapoint_ts_quote_interval_no_previous_quote(self):
        ''' delete_datapoint_ts_quote_interval should succeed even if no quote existed '''
        pid=uuid.uuid4()
        quote='quote'
        its=1
        ets=1000
        self.assertTrue(quoteapi.delete_datapoint_ts_quote_interval(pid=pid, quote=quote, its=its, ets=ets))

    def test_delete_datapoint_ts_quote_interval_previously_existing_quote(self):
        ''' delete_datapoint_ts_quote_interval should delete the quote interval '''
        pid=uuid.uuid4()
        quote='quote1'
        ts=1
        value=100
        for ts in range(10,100):
            self.assertTrue(quoteapi.insert_datapoint_ts_quote(pid, quote, ts, value))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),90)
        self.assertTrue(quoteapi.delete_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=19))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),80)
        self.assertTrue(quoteapi.delete_datapoint_ts_quote_interval(pid=pid, quote=quote, its=100, ets=190))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),80)
        self.assertTrue(quoteapi.delete_datapoint_ts_quote_interval(pid=pid, quote=quote, its=0, ets=190))
        db_quotes=quoteapi.get_datapoint_ts_quote_interval(pid=pid, quote=quote, its=10, ets=99)
        self.assertEqual(len(db_quotes),0)

    def test_increment_datapoint_ts_quote_non_existent_quote(self):
        ''' increment_datapoint_ts_quote should set the quote value if the quote pid not exist previously '''
        pid = uuid.uuid4()
        quote='quote'
        ts=1000
        value=5000
        value_set=quoteapi.increment_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value)
        quote_db=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=1000)
        self.assertEqual(quote_db.pid, pid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value)

    def test_increment_datapoint_ts_quote_previously_existent_quote(self):
        ''' increment_datapoint_ts_quote should add the value to the actual quote value '''
        pid = uuid.uuid4()
        quote='quote'
        ts=1000
        value=5000
        value_set=quoteapi.increment_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value)
        quote_db=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=1000)
        self.assertEqual(quote_db.pid, pid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value)
        for i in range(0,100):
            value_set=quoteapi.increment_datapoint_ts_quote(pid=pid, quote=quote, ts=ts, value=value)
        self.assertEqual(value_set, value+100*value)
        quote_db=quoteapi.get_datapoint_ts_quote(pid=pid, quote=quote, ts=1000)
        self.assertEqual(quote_db.pid, pid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.ts,ts)
        self.assertEqual(quote_db.value,value+100*value)

