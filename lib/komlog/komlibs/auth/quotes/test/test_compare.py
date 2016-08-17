import unittest
import uuid
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.quotes import compare
from komlog.komlibs.auth.quotes import update as quoupd
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto

class AuthQuotesCompareTest(unittest.TestCase):
    ''' komlog.auth.quotes.compare tests '''
    
    def setUp(self):
        username='test_auth.quotes.user'
        password='password'
        email='test_auth.quotes.user@komlog.org'
        try:
            uid = userapi.get_uid(username=username)
            self.user=userapi.get_user_config(uid=uid)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)

    def test_quo_user_total_agents_no_uid(self):
        ''' quo_user_total_agents should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_agents(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTA_UIDNF)

    def test_quo_user_total_agents_non_existent_user(self):
        ''' quo_user_total_agents should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_agents(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTA_USRNF)

    def test_quo_user_total_agents_no_segment_quote_info(self):
        ''' quo_user_total_agents should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_agents_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_agents(params))
        iface=interfaces.User_AgentCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_agents_no_user_quote_info(self):
        ''' quo_user_total_agents should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_agents_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_agents.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_agents(params))
        iface=interfaces.User_AgentCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_agents_user_quote_below_segment_limit(self):
        ''' quo_user_total_agents should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_agents_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_agents.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_agents(params=params)
        self.assertTrue(compare.quo_user_total_agents(params))
        iface=interfaces.User_AgentCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_agents_user_quote_equals_segment_limit(self):
        ''' quo_user_total_agents should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_agents_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_agents.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_agents(params=params)
        self.assertTrue(compare.quo_user_total_agents(params))
        iface=interfaces.User_AgentCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_agents_user_quote_equals_segment_limit_after_surpassing(self):
        ''' quo_user_total_agents should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_agents_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_agents.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_agents(params=params)
        self.assertTrue(compare.quo_user_total_agents(params))
        iface=interfaces.User_AgentCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_agents(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datasources_no_uid(self):
        ''' quo_user_total_datasources should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTDS_UIDNF)

    def test_quo_user_total_datasources_non_existent_user(self):
        ''' quo_user_total_datasources should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTDS_USRNF)

    def test_quo_user_total_datasources_no_segment_quote_info(self):
        ''' quo_user_total_datasources should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_datasources_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_datasources(params))
        iface=interfaces.User_DatasourceCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_datasources_no_user_quote_info(self):
        ''' quo_user_total_datasources should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_datasources_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datasources.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_datasources(params))
        iface=interfaces.User_DatasourceCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datasources_user_quote_below_segment_limit(self):
        ''' quo_user_total_datasources should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_datasources_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datasources.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_datasources(params=params)
        self.assertTrue(compare.quo_user_total_datasources(params))
        iface=interfaces.User_DatasourceCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datasources_user_quote_equals_segment_limit(self):
        ''' quo_user_total_datasources should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_datasources_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datasources.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_datasources(params=params)
        self.assertTrue(compare.quo_user_total_datasources(params))
        iface=interfaces.User_DatasourceCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datasources_user_quote_below_segment_limit_after_surpassing(self):
        ''' quo_user_total_datasources should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_datasources_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datasources.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_datasources(params=params)
        self.assertTrue(compare.quo_user_total_datasources(params))
        iface=interfaces.User_DatasourceCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_datasources(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datapoints_no_uid(self):
        ''' quo_user_total_datapoints should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTDP_UIDNF)

    def test_quo_user_total_datapoints_non_existent_user(self):
        ''' quo_user_total_datapoints should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTDP_USRNF)

    def test_quo_user_total_datapoints_no_segment_quote_info(self):
        ''' quo_user_total_datapoints should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_datapoints_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_datapoints(params))
        iface=interfaces.User_DatapointCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_datapoints_no_user_quote_info(self):
        ''' quo_user_total_datapoints should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_datapoints_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_datapoints(params))
        iface=interfaces.User_DatapointCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datapoints_user_quote_below_segment_limit(self):
        ''' quo_user_total_datapoints should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_datapoints_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datapoints.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_datapoints(params=params)
        self.assertTrue(compare.quo_user_total_datapoints(params))
        iface=interfaces.User_DatapointCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datapoints_user_quote_equals_segment_limit(self):
        ''' quo_user_total_datapoints should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_datapoints_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_datapoints(params=params)
        self.assertTrue(compare.quo_user_total_datapoints(params))
        iface=interfaces.User_DatapointCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_datapoints_user_quote_below_segment_limit_after_surpassing(self):
        ''' quo_user_total_datapoints should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_datapoints_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_datapoints(params=params)
        self.assertTrue(compare.quo_user_total_datapoints(params))
        iface=interfaces.User_DatapointCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_datapoints(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_widgets_no_uid(self):
        ''' quo_user_total_widgets should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_widgets(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTW_UIDNF)

    def test_quo_user_total_widgets_non_existent_user(self):
        ''' quo_user_total_widgets should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_widgets(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTW_USRNF)

    def test_quo_user_total_widgets_no_segment_quote_info(self):
        ''' quo_user_total_widgets should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_widgets_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_widgets(params))
        iface=interfaces.User_WidgetCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_widgets_no_user_quote_info(self):
        ''' quo_user_total_widgets should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_widgets_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_widgets.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_widgets(params))
        iface=interfaces.User_WidgetCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_widgets_user_quote_below_segment_limit(self):
        ''' quo_user_total_widgets should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_widgets_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_widgets.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_widgets(params=params)
        self.assertTrue(compare.quo_user_total_widgets(params))
        iface=interfaces.User_WidgetCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_widgets_user_quote_equals_segment_limit(self):
        ''' quo_user_total_widgets should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_widgets_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_widgets.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_widgets(params=params)
        self.assertTrue(compare.quo_user_total_widgets(params))
        iface=interfaces.User_WidgetCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_widgets_user_quote_below_segment_limit_after_surpassing(self):
        ''' quo_user_total_widgets should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_widgets_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_widgets.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_widgets(params=params)
        self.assertTrue(compare.quo_user_total_widgets(params))
        iface=interfaces.User_WidgetCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_widgets(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_dashboards_no_uid(self):
        ''' quo_user_total_dashboards should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_dashboards(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTDB_UIDNF)

    def test_quo_user_total_dashboards_non_existent_user(self):
        ''' quo_user_total_dashboards should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_dashboards(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTDB_USRNF)

    def test_quo_user_total_dashboards_no_segment_quote_info(self):
        ''' quo_user_total_dashboards should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_dashboards_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_dashboards(params))
        iface=interfaces.User_DashboardCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_dashboards_no_user_quote_info(self):
        ''' quo_user_total_dashboards should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_dashboards_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_dashboards.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_dashboards(params))
        iface=interfaces.User_DashboardCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_dashboards_user_quote_below_segment_limit(self):
        ''' quo_user_total_dashboards should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_dashboards_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_dashboards.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_dashboards(params=params)
        self.assertTrue(compare.quo_user_total_dashboards(params))
        iface=interfaces.User_DashboardCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_dashboards_user_quote_equals_segment_limit(self):
        ''' quo_user_total_dashboards should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_dashboards_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_dashboards.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_dashboards(params=params)
        self.assertTrue(compare.quo_user_total_dashboards(params))
        iface=interfaces.User_DashboardCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_dashboards_user_quote_below_segment_limit_after_surpassing(self):
        ''' quo_user_total_dashboards should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_dashboards_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_dashboards.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_dashboards(params=params)
        self.assertTrue(compare.quo_user_total_dashboards(params))
        iface=interfaces.User_DashboardCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_dashboards(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_snapshots_no_uid(self):
        ''' quo_user_total_snapshots should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_snapshots(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTSN_UIDNF)

    def test_quo_user_total_snapshots_non_existent_user(self):
        ''' quo_user_total_snapshots should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_snapshots(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTSN_USRNF)

    def test_quo_user_total_snapshots_no_segment_quote_info(self):
        ''' quo_user_total_snapshots should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_snapshots_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_snapshots(params))
        iface=interfaces.User_SnapshotCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_snapshots_no_user_quote_info(self):
        ''' quo_user_total_snapshots should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_snapshots_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_snapshots.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_snapshots(params))
        iface=interfaces.User_SnapshotCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_snapshots_user_quote_below_segment_limit(self):
        ''' quo_user_total_snapshots should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_snapshots_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_snapshots.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_snapshots(params=params)
        self.assertTrue(compare.quo_user_total_snapshots(params))
        iface=interfaces.User_SnapshotCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_snapshots_user_quote_equals_segment_limit(self):
        ''' quo_user_total_snapshots should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_snapshots_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_snapshots.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_snapshots(params=params)
        self.assertTrue(compare.quo_user_total_snapshots(params))
        iface=interfaces.User_SnapshotCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_snapshots_user_quote_below_segment_limit_after_surpassing(self):
        ''' quo_user_total_snapshots should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_snapshots_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_snapshots.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_snapshots(params=params)
        self.assertTrue(compare.quo_user_total_snapshots(params))
        iface=interfaces.User_SnapshotCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_snapshots(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_circles_no_uid(self):
        ''' quo_user_total_circles should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_circles(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTC_UIDNF)

    def test_quo_user_total_circles_non_existent_user(self):
        ''' quo_user_total_circles should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_circles(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTC_USRNF)

    def test_quo_user_total_circles_no_segment_quote_info(self):
        ''' quo_user_total_circles should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_user_total_circles_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_circles(params))
        iface=interfaces.User_CircleCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_user_total_circles_no_user_quote_info(self):
        ''' quo_user_total_circles should return True if no user quote info is found, not setting the deny interface '''
        username='test_quo_user_total_circles_no_user_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_circles.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        self.assertTrue(compare.quo_user_total_circles(params))
        iface=interfaces.User_CircleCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_circles_user_quote_below_segment_limit(self):
        ''' quo_user_total_circles should return True if user quote is below segment limit, not setting the deny interface '''
        username='test_quo_user_total_circles_user_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_circles.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_circles(params=params)
        self.assertTrue(compare.quo_user_total_circles(params))
        iface=interfaces.User_CircleCreation().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_circles_user_quote_equals_segment_limit(self):
        ''' quo_user_total_circles should return True if user quote is equal segment limit, setting the deny interface '''
        username='test_quo_user_total_circles_user_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_circles.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_circles(params=params)
        self.assertTrue(compare.quo_user_total_circles(params))
        iface=interfaces.User_CircleCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_user_total_circles_user_quote_below_segment_limit_after_surpassing(self):
        ''' quo_user_total_circles should return True if user quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_user_total_circles_user_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_user_total_circles.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid']}
        quoupd.quo_user_total_circles(params=params)
        self.assertTrue(compare.quo_user_total_circles(params))
        iface=interfaces.User_CircleCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        self.assertTrue(compare.quo_user_total_circles(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datasources_no_uid(self):
        ''' quo_agent_total_datasources should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_agent_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QATDS_PNF)

    def test_quo_agent_total_datasources_no_aid(self):
        ''' quo_agent_total_datasources should fail if no aid is passed '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_agent_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QATDS_PNF)

    def test_quo_agent_total_datasources_non_existent_user(self):
        ''' quo_agent_total_datasources should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'aid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_agent_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QATDS_USRNF)

    def test_quo_agent_total_datasources_no_segment_quote_info(self):
        ''' quo_agent_total_datasources should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_agent_total_datasources_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid'],'aid':agent['aid']}
        self.assertTrue(compare.quo_agent_total_datasources(params))
        iface=interfaces.Agent_DatasourceCreation(agent['aid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_agent_total_datasources_no_agent_quote_info(self):
        ''' quo_agent_total_datasources should return True if no agent quote info is found, not setting the deny interface '''
        username='test_quo_agent_total_datasources_no_agent_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datasources.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        self.assertTrue(compare.quo_agent_total_datasources(params))
        iface=interfaces.Agent_DatasourceCreation(agent['aid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datasources_agent_quote_below_segment_limit(self):
        ''' quo_agent_total_datasources should return True if agent quote is below segment limit, not setting the deny interface '''
        username='test_quo_agent_total_datasources_agent_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datasources.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        quoupd.quo_agent_total_datasources(params=params)
        self.assertTrue(compare.quo_agent_total_datasources(params))
        iface=interfaces.Agent_DatasourceCreation(agent['aid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datasources_agent_quote_equals_segment_limit(self):
        ''' quo_agent_total_datasources should return True if agent quote is equal segment limit, setting the deny interface '''
        username='test_quo_agent_total_datasources_agent_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datasources.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        quoupd.quo_agent_total_datasources(params=params)
        self.assertTrue(compare.quo_agent_total_datasources(params))
        iface=interfaces.Agent_DatasourceCreation(agent['aid']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datasources_agent_quote_below_segment_limit_after_surpassing(self):
        ''' quo_agent_total_datasources should return True if agent quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_agent_total_datasources_agent_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datasources.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        quoupd.quo_agent_total_datasources(params=params)
        self.assertTrue(compare.quo_agent_total_datasources(params))
        iface=interfaces.Agent_DatasourceCreation(agent['aid']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datapoints_no_uid(self):
        ''' quo_agent_total_datapoints should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_agent_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QATDP_PNF)

    def test_quo_agent_total_datapoints_no_aid(self):
        ''' quo_agent_total_datapoints should fail if no aid is passed '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_agent_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QATDP_PNF)

    def test_quo_agent_total_datapoints_non_existent_user(self):
        ''' quo_agent_total_datapoints should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'aid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_agent_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QATDP_USRNF)

    def test_quo_agent_total_datapoints_no_segment_quote_info(self):
        ''' quo_agent_total_datapoints should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_agent_total_datapoints_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid'],'aid':agent['aid']}
        self.assertTrue(compare.quo_agent_total_datapoints(params))
        iface=interfaces.Agent_DatapointCreation(agent['aid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_agent_total_datapoints_no_agent_quote_info(self):
        ''' quo_agent_total_datapoints should return True if no agent quote info is found, not setting the deny interface '''
        username='test_quo_agent_total_datapoints_no_agent_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        self.assertTrue(compare.quo_agent_total_datapoints(params))
        iface=interfaces.Agent_DatapointCreation(agent['aid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datapoints_agent_quote_below_segment_limit(self):
        ''' quo_agent_total_datapoints should return True if agent quote is below segment limit, not setting the deny interface '''
        username='test_quo_agent_total_datapoints_agent_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datapoints.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        quoupd.quo_agent_total_datapoints(params=params)
        self.assertTrue(compare.quo_agent_total_datapoints(params))
        iface=interfaces.Agent_DatapointCreation(agent['aid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datapoints_agent_quote_equals_segment_limit(self):
        ''' quo_agent_total_datapoints should return True if agent quote is equal segment limit, setting the deny interface '''
        username='test_quo_agent_total_datapoints_agent_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        quoupd.quo_agent_total_datapoints(params=params)
        self.assertTrue(compare.quo_agent_total_datapoints(params))
        iface=interfaces.Agent_DatapointCreation(agent['aid']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_agent_total_datapoints_agent_quote_below_segment_limit_after_surpassing(self):
        ''' quo_agent_total_datapoints should return True if agent quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_agent_total_datapoints_agent_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_agent_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'aid':agent['aid']}
        quoupd.quo_agent_total_datapoints(params=params)
        self.assertTrue(compare.quo_agent_total_datapoints(params))
        iface=interfaces.Agent_DatapointCreation(agent['aid']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_datasource_total_datapoints_no_uid(self):
        ''' quo_datasource_total_datapoints should fail if no uid is passed '''
        params={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_datasource_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDSTDP_PNF)

    def test_quo_datasource_total_datapoints_no_did(self):
        ''' quo_datasource_total_datapoints should fail if no did is passed '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_datasource_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDSTDP_PNF)

    def test_quo_datasource_total_datapoints_non_existent_user(self):
        ''' quo_datasource_total_datapoints should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'did':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_datasource_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDSTDP_USRNF)

    def test_quo_datasource_total_datapoints_no_segment_quote_info(self):
        ''' quo_datasource_total_datapoints should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_datasource_total_datapoints_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid'],'did':datasource['did']}
        self.assertTrue(compare.quo_datasource_total_datapoints(params))
        iface=interfaces.Datasource_DatapointCreation(datasource['did']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_datasource_total_datapoints_no_datasource_quote_info(self):
        ''' quo_datasource_total_datapoints should return True if no ds quote info is found, not setting the deny interface '''
        username='test_quo_datasource_total_datapoints_no_datasource_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_datasource_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'did':datasource['did']}
        self.assertTrue(compare.quo_datasource_total_datapoints(params))
        iface=interfaces.Datasource_DatapointCreation(datasource['did']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_datasource_total_datapoints_datasource_quote_below_segment_limit(self):
        ''' quo_datasource_total_datapoints should return True if datasource quote is below segment limit, not setting the deny interface '''
        username='test_quo_datasource_total_datapoints_datasource_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_datasource_total_datapoints.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'did':datasource['did']}
        quoupd.quo_datasource_total_datapoints(params=params)
        self.assertTrue(compare.quo_datasource_total_datapoints(params))
        iface=interfaces.Datasource_DatapointCreation(datasource['did']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_datasource_total_datapoints_datasource_quote_equals_segment_limit(self):
        ''' quo_datasource_total_datapoints should return True if datasource quote is equal segment limit, setting the deny interface '''
        username='test_quo_datasource_total_datapoints_datasource_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_datasource_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'did':datasource['did']}
        quoupd.quo_datasource_total_datapoints(params=params)
        self.assertTrue(compare.quo_datasource_total_datapoints(params))
        iface=interfaces.Datasource_DatapointCreation(datasource['did']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_datasource_total_datapoints_datasource_quote_below_segment_limit_after_surpassing(self):
        ''' quo_datasource_total_datapoints should return True if datasource quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_datasource_total_datapoints_datasource_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_datasource_total_datapoints.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'did':datasource['did']}
        quoupd.quo_datasource_total_datapoints(params=params)
        self.assertTrue(compare.quo_datasource_total_datapoints(params))
        iface=interfaces.Datasource_DatapointCreation(datasource['did']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_circle_total_members_no_uid(self):
        ''' quo_circle_total_members should fail if no uid is passed '''
        params={'cid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_circle_total_members(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QCTM_PNF)

    def test_quo_circle_total_members_no_cid(self):
        ''' quo_circle_total_members should fail if no uid is passed '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_circle_total_members(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QCTM_PNF)

    def test_quo_circle_total_members_non_existent_user(self):
        ''' quo_circle_total_members should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'cid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_circle_total_members(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QCTM_USRNF)

    def test_quo_circle_total_members_no_segment_quote_info(self):
        ''' quo_circle_total_members should return True if no segment quote info is found, not setting the deny interface '''
        username='test_quo_circle_total_members_no_segment_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        circlename='circlename'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        params={'uid':user['uid'],'cid':circle['cid']}
        self.assertTrue(compare.quo_circle_total_members(params))
        iface=interfaces.User_AddMemberToCircle(circle['cid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))

    def test_quo_circle_total_members_no_datasource_quote_info(self):
        ''' quo_circle_total_members should return True if no circle quote info is found, not setting the deny interface '''
        username='test_quo_circle_total_members_no_circle_quote_info'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        circlename='circlename'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_circle_total_members.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'cid':circle['cid']}
        self.assertTrue(compare.quo_circle_total_members(params))
        iface=interfaces.User_AddMemberToCircle(circle['cid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_circle_total_members_circle_quote_below_segment_limit(self):
        ''' quo_circle_total_members should return True if datasource quote is below segment limit, not setting the deny interface '''
        username='test_quo_circle_total_members_circle_quote_below_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        circlename='circlename'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_circle_total_members.name
        limit=1
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'cid':circle['cid']}
        quoupd.quo_circle_total_members(params=params)
        self.assertTrue(compare.quo_circle_total_members(params))
        iface=interfaces.User_AddMemberToCircle(circle['cid']).value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_circle_total_members_circle_quote_equals_segment_limit(self):
        ''' quo_circle_total_members should return True if datasource quote is equal segment limit, setting the deny interface '''
        username='test_quo_circle_total_members_circle_quote_equals_segment_limit'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        circlename='circlename'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_circle_total_members.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'cid':circle['cid']}
        quoupd.quo_circle_total_members(params=params)
        self.assertTrue(compare.quo_circle_total_members(params))
        iface=interfaces.User_AddMemberToCircle(circle['cid']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_circle_total_members_circle_quote_below_segment_limit_after_surpassing(self):
        ''' quo_circle_total_members should return True if circle quote is below segment limit, unsetting the deny interface if it was previously set '''
        username='test_quo_circle_total_members_circle_quote_equals_segment_limit_after_surpassing'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        circlename='circlename'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))
        quote=Quotes.quo_circle_total_members.name
        limit=0
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=user['segment'],quote=quote, value=limit))
        params={'uid':user['uid'],'cid':circle['cid']}
        quoupd.quo_circle_total_members(params=params)
        self.assertTrue(compare.quo_circle_total_members(params))
        iface=interfaces.User_AddMemberToCircle(circle['cid']).value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, params['uid'])
        self.assertEqual(db_iface.interface, iface)
        self.assertEqual(db_iface.content, None)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=user['segment']))

    def test_quo_daily_datasource_occupation_failure_no_did(self):
        ''' quo_daily_datasource_occupation should return None if params has no did '''
        params={'date':timeuuid.uuid1()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDDSO_PNF)

    def test_quo_daily_datasource_occupation_failure_no_date(self):
        ''' quo_daily_datasource_occupation should return None if params has no date '''
        params={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDDSO_PNF)

    def test_quo_daily_datasource_occupation_failure_non_existent_datasource(self):
        ''' quo_daily_datasource_occupation should return None if datasource does not exist '''
        params={'date':timeuuid.uuid1(), 'did':uuid.uuid4()}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            compare.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDDSO_DSNF)

    def test_quo_daily_datasource_occupation_failure_non_existent_user(self):
        ''' quo_daily_datasource_occupation should fail if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_datasource_occupation_failure_non_existent_user'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDDSO_USRNF)

    def test_quo_daily_datasource_occupation_non_existent_segment_quote(self):
        ''' quo_daily_datasource_occupation should return True if segment has not defined this quote, and not setting any deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation_non_existent_segment_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation_failure_non_existent_segment_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_datasource_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily(did).value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))

    def test_quo_daily_datasource_occupation_non_existent_datasource_ts_quote(self):
        ''' quo_daily_datasource_occupation should return True if user has not set this quote yet, not setting the deny interface  '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation_non_existent_user_ts_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation_failure_non_existent_datasource_ts_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_datasource_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_datasource_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily(did).value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_daily_datasource_occupation_datasource_quote_is_below_segment_limit(self):
        ''' quo_daily_datasource_occupation should return True if datasource quote value is below the limit set in the segment, and not set the interface deny '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_datasource_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_datasource_ts_quote(did=did, quote=quote, ts=ts, value=9))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_datasource_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily(did).value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_daily_datasource_occupation_user_quote_is_equal_than_segment_value(self):
        ''' quo_daily_datasource_occupation should return True if user quote value is equal or greater than the maximum value allowed set in the segment, and set the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_datasource_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_datasource_ts_quote(did=did, quote=quote, ts=ts, value=10))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_datasource_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily(did).value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNotNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_daily_user_datasources_occupation_failure_no_did(self):
        ''' quo_daily_user_datasources_occupation should return None if params has no did '''
        params={'date':timeuuid.uuid1()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDUDSO_PNF)

    def test_quo_daily_user_datasources_occupation_failure_no_date(self):
        ''' quo_daily_user_datasources_occupation should return None if params has no date '''
        params={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDUDSO_PNF)

    def test_quo_daily_user_datasources_occupation_failure_non_existent_datasource(self):
        ''' quo_daily_user_datasources_occupation should return None if datasource does not exist '''
        params={'date':timeuuid.uuid1(), 'did':uuid.uuid4()}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            compare.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDUDSO_DSNF)

    def test_quo_daily_user_datasources_occupation_failure_non_existent_user(self):
        ''' quo_daily_user_datasources_occupation should fail if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_user_datasources_occupation_failure_non_existent_user'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QDUDSO_USRNF)

    def test_quo_daily_user_datasources_occupation_non_existent_segment_quote(self):
        ''' quo_daily_user_datasources_occupation should return True if segment has not defined this quote, not setting the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation_non_existent_segment_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation_failure_non_existent_segment_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_user_datasources_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily().value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))

    def test_quo_daily_user_datasources_occupation_non_existent_user_ts_quote(self):
        ''' quo_daily_user_datasources_occupation should return False if user has not set this quote yet '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation_non_existent_user_ts_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation_failure_non_existent_user_ts_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_user_datasources_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily().value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_daily_user_datasources_occupation_user_quote_is_not_greater_than_segment_value(self):
        ''' quo_daily_user_datasources_occupation should return False if user quote value is not greater than the maximum value allowed set in the segment '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=9))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_user_datasources_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily().value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_daily_user_datasources_occupation_user_quote_is_greater_than_segment_value(self):
        ''' quo_daily_user_datasources_occupation should return True if user quote value is greater than the maximum value allowed set in the segment '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=10))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_user_datasources_occupation(params))
        iface=interfaces.User_PostDatasourceDataDaily().value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNotNone(cassapiiface.get_user_ts_iface_deny(uid=uid,iface=iface, ts=ts))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_user_total_occupation_no_did_param(self):
        ''' quo_user_total_occupation should return None if no did param is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            compare.quo_user_total_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTO_DIDNF)

    def test_quo_user_total_occupation_no_datasource_found(self):
        ''' quo_user_total_occupation should return None if datasource does not exist '''
        did=uuid.uuid4()
        params={'did':did}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            compare.quo_user_total_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTO_DSNF)

    def test_quo_user_total_occupation_no_user_found(self):
        ''' quo_user_total_occupation should fail if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            compare.quo_user_total_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQC_QUTO_USRNF)

    def test_quo_user_total_occupation_no_segment_quo_stablished(self):
        ''' quo_user_total_occupation should return True if segment quote is not established, not setting the interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_no_segment_quo_stablished'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        self.assertTrue(compare.quo_user_total_occupation(params))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=uid,iface=iface))

    def test_quo_user_total_occupation_no_user_quote_found(self):
        ''' quo_user_total_occupation should return False if user quote is not found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        params={'did':did}
        self.assertTrue(compare.quo_user_total_occupation(params))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=uid,iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))


    def test_quo_user_total_occupation_user_quote_less_than_limit(self):
        ''' quo_user_total_occupation should return True if user quote has not surpassed segment limit, not setting the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        ts=1
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=1))
        params={'did':did}
        self.assertTrue(compare.quo_user_total_occupation(params))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        ts=timeuuid.get_day_timestamp(date)
        self.assertIsNone(cassapiiface.get_user_iface_deny(uid=uid,iface=iface))
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_user_total_occupation_user_quote_above_limit(self):
        ''' quo_user_total_occupation should return True if user quote has surpassed segment limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        dsquote=Quotes.quo_daily_user_datasources_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        ts=1
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=dsquote, ts=ts, value=10))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=10))
        params={'did':did}
        self.assertTrue(compare.quo_user_total_occupation(params))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid,iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, uid)
        self.assertEqual(db_iface.interface, iface)
        min_ts=timeuuid.min_uuid_from_time(ts).hex
        self.assertEqual(db_iface.content, min_ts)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

    def test_quo_user_total_occupation_user_quote_under_limit_after_surpassing(self):
        ''' quo_user_total_occupation should return True if user quote has surpassed segment limit and after that, the quote has decreased under segment limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        dsquote=Quotes.quo_daily_user_datasources_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=10))
        ts=1
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=10))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=dsquote, ts=ts, value=10))
        params={'did':did}
        self.assertTrue(compare.quo_user_total_occupation(params))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid,iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, uid)
        self.assertEqual(db_iface.interface, iface)
        min_ts=timeuuid.min_uuid_from_time(ts).hex
        self.assertEqual(db_iface.content, min_ts)
        ts=2
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=1))
        self.assertTrue(compare.quo_user_total_occupation(params))
        db_iface=cassapiiface.get_user_iface_deny(uid=uid,iface=iface)
        self.assertIsNone(db_iface)
        self.assertTrue(cassapisegment.delete_user_segment_quotes(sid=segment))

