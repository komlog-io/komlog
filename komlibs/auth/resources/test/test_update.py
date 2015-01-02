import unittest
import uuid
from komlibs.auth.resources import update
from komcass.api import permission as cassapiperm
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.dashboard import api as dashboardapi


class AuthResourcesUpdateTest(unittest.TestCase):
    ''' komlog.auth.resources.update tests '''
    
    def setUp(self):
        username = 'test_komlibs.auth.resources.authorization_user'
        password = 'password'
        email = 'test_komlibs.auth.resources.update_user@komlog.org'
        self.user = userapi.create_user(username=username, password=password, email=email)
        

    def test_update_user_agent_perms_no_uid(self):
        ''' update_user_agent_perms should fail if no uid is passed'''
        params={'aid':uuid.uuid4()}
        self.assertFalse(update.update_user_agent_perms(params))

    def test_update_user_agent_perms_no_aid(self):
        ''' update_user_agent_perms should fail if no aid is passed'''
        params={'uid':self.user.uid}
        self.assertFalse(update.update_user_agent_perms(params))

    def test_update_user_agent_perms_success(self):
        ''' update_user_agent_perms should succeed if agent belongs to user'''
        user=self.user
        agentname='test_update_user_agent_perms_success_agent'
        pubkey='dummy'
        version='tests'
        agent=agentapi.create_agent(username=user.username, agentname=agentname, pubkey=pubkey, version=version)
        params={'uid':user.uid,'aid':agent.aid}
        self.assertTrue(update.update_user_agent_perms(params))

    def test_update_user_agent_perms_failure(self):
        ''' update_user_agent_perms should fail if agent does not belong to user'''
        user=self.user
        params={'uid':user.uid,'aid':uuid.uuid4()}
        self.assertFalse(update.update_user_agent_perms(params))

    def test_update_user_datasource_perms_no_uid(self):
        ''' update_user_datasource_perms should fail if no uid is passed'''
        params={'did':uuid.uuid4()}
        self.assertFalse(update.update_user_datasource_perms(params))

    def test_update_user_datasource_perms_no_did(self):
        ''' update_user_datasource_perms should fail if no did is passed'''
        params={'uid':self.user.uid}
        self.assertFalse(update.update_user_datasource_perms(params))

    def test_update_user_datasource_perms_success(self):
        ''' update_user_datasource_perms should succeed if datasource belongs to user'''
        user=self.user
        agentname='test_update_user_datasource_perms_success_agent'
        pubkey='dummy'
        version='tests'
        agent=agentapi.create_agent(username=user.username, agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test_update_user_datasource_perms_success_datasource'
        datasource=datasourceapi.create_datasource(username=user.username, aid=agent.aid, datasourcename=datasourcename)
        params={'uid':user.uid,'did':datasource.did}
        self.assertTrue(update.update_user_datasource_perms(params))

    def test_update_user_datasource_perms_failure(self):
        ''' update_user_datasource_perms should fail if datasource does not belong to user'''
        user=self.user
        params={'uid':user.uid,'did':uuid.uuid4()}
        self.assertFalse(update.update_user_datasource_perms(params))

    def test_update_agent_datasource_perms_no_aid(self):
        ''' update_agent_datasource_perms should fail if no aid is passed'''
        params={'did':uuid.uuid4()}
        self.assertFalse(update.update_agent_datasource_perms(params))

    def test_update_agent_datasource_perms_no_did(self):
        ''' update_agent_datasource_perms should fail if no did is passed'''
        params={'aid':self.user.uid}
        self.assertFalse(update.update_agent_datasource_perms(params))

    def test_update_agent_datasource_perms_success(self):
        ''' update_agent_datasource_perms should succeed if datasource belongs to agent'''
        user=self.user
        agentname='test_update_agent_datasource_perms_success_agent'
        pubkey='dummy'
        version='tests'
        agent=agentapi.create_agent(username=user.username, agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test_update_agent_datasource_perms_success_datasource'
        datasource=datasourceapi.create_datasource(username=user.username, aid=agent.aid, datasourcename=datasourcename)
        params={'aid':agent.aid,'did':datasource.did}
        self.assertTrue(update.update_agent_datasource_perms(params))

    def test_update_agent_datasource_perms_failure(self):
        ''' update_agent_datasource_perms should fail if datasource does not belong to agent'''
        user=self.user
        agentname='test_update_agent_datasource_perms_failure_agent'
        pubkey='dummy'
        version='tests'
        agent=agentapi.create_agent(username=user.username, agentname=agentname, pubkey=pubkey, version=version)
        params={'aid':agent.aid,'did':uuid.uuid4()}
        self.assertFalse(update.update_agent_datasource_perms(params))

    def test_update_user_datapoint_perms_no_uid(self):
        ''' update_user_datapoint_perms should fail if no uid is passed'''
        params={'pid':uuid.uuid4()}
        self.assertFalse(update.update_user_datapoint_perms(params))

    def test_update_user_datapoint_perms_no_pid(self):
        ''' update_user_datapoint_perms should fail if no pid is passed'''
        params={'uid':self.user.uid}
        self.assertFalse(update.update_user_datapoint_perms(params))

    def test_update_user_datapoint_perms_success(self):
        ''' update_user_datapoint_perms should succeed if datapoint belongs to user'''
        user=self.user
        agentname='test_update_user_datapoint_perms_success_agent'
        pubkey='dummy'
        version='tests'
        agent=agentapi.create_agent(username=user.username, agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test_update_user_datapoint_perms_success_datasource'
        datasource=datasourceapi.create_datasource(username=user.username, aid=agent.aid, datasourcename=datasourcename)
        datapointname='test_update_user_datapoint_perms_success_datapoint'
        position='1'
        length='1'
        datapoint=datapointapi.create_datapoint(did=datasource.did, datapointname=datapointname, position=position, length=length, date=datasource.creation_date)
        params={'uid':user.uid,'pid':datapoint.pid}
        self.assertTrue(update.update_user_datapoint_perms(params))

    def test_update_user_datapoint_perms_failure(self):
        ''' update_user_datapoint_perms should fail if datapoint does not belong to user'''
        user=self.user
        params={'uid':user.uid,'pid':uuid.uuid4()}
        self.assertFalse(update.update_user_datapoint_perms(params))

    def test_update_user_widget_perms_no_uid(self):
        ''' update_user_widget_perms should fail if no uid is passed'''
        params={'wid':uuid.uuid4()}
        self.assertFalse(update.update_user_widget_perms(params))

    def test_update_user_widget_perms_no_wid(self):
        ''' update_user_widget_perms should fail if no wid is passed'''
        params={'uid':self.user.uid}
        self.assertFalse(update.update_user_widget_perms(params))

    def test_update_user_widget_perms_success(self):
        ''' update_user_widget_perms should succeed if widget belongs to user'''
        user=self.user
        agentname='test_update_user_widget_perms_success_agent'
        pubkey='dummy'
        version='tests'
        agent=agentapi.create_agent(username=user.username, agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test_update_user_widget_perms_success_datasource'
        datasource=datasourceapi.create_datasource(username=user.username, aid=agent.aid, datasourcename=datasourcename)
        widget=widgetapi.new_widget_ds(username=user.username, did=datasource.did)
        params={'uid':user.uid,'wid':widget.wid}
        self.assertTrue(update.update_user_widget_perms(params))

    def test_update_user_widget_perms_failure(self):
        ''' update_user_widget_perms should fail if widget does not belong to user'''
        user=self.user
        params={'uid':user.uid,'wid':uuid.uuid4()}
        self.assertFalse(update.update_user_widget_perms(params))

    def test_update_user_dashboard_perms_no_uid(self):
        ''' update_user_dashboard_perms should fail if no uid is passed'''
        params={'bid':uuid.uuid4()}
        self.assertFalse(update.update_user_dashboard_perms(params))

    def test_update_user_dashboard_perms_no_bid(self):
        ''' update_user_dashboard_perms should fail if no bid is passed'''
        params={'uid':self.user.uid}
        self.assertFalse(update.update_user_dashboard_perms(params))

#TODO Faltaria crear funciones para probar la ejecucion correcta de update_user_dashboard_perms, pero todavia no existe funcion en el dashboardapi para crear un dashbaord.

    def test_update_user_dashboard_perms_failure(self):
        ''' update_user_dashboard_perms should fail if dashboard does not belong to user'''
        user=self.user
        params={'uid':user.uid,'bid':uuid.uuid4()}
        self.assertFalse(update.update_user_dashboard_perms(params))

