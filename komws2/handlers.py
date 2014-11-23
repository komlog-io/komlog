#coding: utf-8

import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
from komlibs.ifaceops import ifaceops
from komfig import logger
from komws2 import auth
import os
import uuid
import datetime
import dateutil.parser
import json

class BaseHandler(tornado.web.RequestHandler):
    
    @auth.userauthenticated
    def get_current_user(self):
        return self.get_secure_cookie('komlog_user')

class AgentsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        #Aquí llega una vez ha validado
        try:
            req_data=json_decode(self.request.body)
            ag_pubkey=req_data['ag_pubkey']
            ag_version=req_data['ag_version']
            ag_name=req_data['ag_name']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.new_agent_operation(username=self.user, agentname=ag_name, pubkey=ag_pubkey, version=ag_version)
            self.set_status(status)
            self.write(json_encode(data))

    @auth.userauthenticated
    def get(self):
        status,data=ifaceops.get_agents_config_operation(username=self.user)
        self.set_status(status)
        self.write(json_encode(data))

class AgentConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_aid):
        aid=uuid.UUID(p_aid)
        status,data=ifaceops.get_agent_config_operation(username=self.user, aid=aid)
        self.set_status(status)
        self.write(json_encode(data))

    @auth.userauthenticated
    def put(self,p_aid):
        aid=uuid.UUID(p_aid)
        data=json_decode(self.request.body)
        status,data=ifaceops.update_agent_config_operation(username=self.user, aid=aid, data=data)
        self.set_status(status)
        self.write(json_encode(data))

class DatasourceDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_did):
        did=uuid.UUID(p_did)
        status,data=ifaceops.get_datasource_data_operation(username=self.user, did=did)
        self.set_status(status)
        self.write(json_encode(data))

    @auth.agentauthenticated
    def post(self,p_did):
        try:
            logger.logger.debug('POST DatasourceData Init')
            did=uuid.UUID(p_did)
            aid=uuid.UUID(self.agent)
            ctype=self.request.headers.get('Content-Type')
            content=self.request.body.decode('utf-8')
            dest_dir=self.application.dest_dir
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            if ctype.find('application/json')>=0:
                status,data=ifaceops.upload_datasource_data_operation(username=self.user, aid=aid, did=did, content=content, destination=dest_dir)
                self.set_status(status)
                self.write(json_encode(data))
            else:
                self.set_status(400)
                self.write(json_encode({'message':'Bad Request'}))

class DatasourceConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_did):
        did=uuid.UUID(p_did)
        status,data=ifaceops.get_datasource_config_operation(username=self.user, did=did)
        self.set_status(status)
        self.write(json_encode(data))

    @auth.userauthenticated
    def put(self, p_did):
        did=uuid.UUID(p_did)
        content=json_decode(self.request.body)
        status,data=ifaceops.update_datasource_config_operation(username=self.user, did=did, content=content)
        self.set_status(status)
        self.write(json_encode(data))

class DatasourcesHandler(tornado.web.RequestHandler):

    @auth.agentauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            aid=uuid.UUID(self.agent)
            ds_name=data['ds_name']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.new_datasource_operation(username=self.user, aid=aid, datasourcename=ds_name)
            self.set_status(status)
            self.write(json_encode(data))

    @auth.userauthenticated
    def get(self):
        status,data=ifaceops.get_datasources_config_operation(username=self.user)
        self.set_status(status)
        self.write(json_encode(data))

class UsersHandler(tornado.web.RequestHandler):
    def post(self):
        #suponemos que aquí llega una vez ha validado capcha o algo asi
        try:
            data=json_decode(self.request.body)
            username=''+data['username']
            password=''+data['password']
            email=''+data['email']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.new_user_operation(username,password,email)
            self.set_status(status)
            self.write(json_encode(data))

class UserConfirmationHandler(tornado.web.RequestHandler):

    def get(self):
        #Aquí llega a traves de un enlace generado dinámicamente durante el alta
        try:
            code=self.get_argument('c') #confirmation cod3 
            email=self.get_argument('e') #email
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.confirm_user_operation(email,code)
            self.set_status(status)
            self.write(json_encode(data))

class DatapointDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_pid):
        try:
            pid=uuid.UUID(p_pid)
            end_date=self.get_argument('ed',default=None) #ed : end date
            start_date=self.get_argument('sd',default=None) #sd : start date
            end_date=dateutil.parser.parse(end_date) if end_date else None
            start_date=dateutil.parser.parse(start_date) if start_date else None
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.get_datapoint_data_operation(username=self.user, pid=pid, start_date=start_date, end_date=end_date)
            self.set_status(200)
            self.write(json_encode(data))

class DatapointConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_pid):
        try:
            pid=uuid.UUID(p_pid)
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))
        else:
            status,data=ifaceops.get_datapoint_config_operation(username=self.user, pid=pid)
            self.set_status(status)
            self.write(json_encode(data))

    @auth.userauthenticated
    def put(self, p_pid):
        try:
            pid=uuid.UUID(p_pid)
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        else:
            status,data=ifaceops.update_datapoint_config_operation(username=self.user, pid=pid, data=data)
            self.set_status(status)
            self.write(json_encode(data))

class DatapointsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            dsdate=data['ds_date']
            did=data['did']
            cs=data['cs'] #char start
            vl=data['vl'] #var length
            dpname=data['dtp_name'] #dp name
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.new_datapoint_operation(username=self.user, did=did, datasourcedate=dsdate, position=pos, length=vl, datapointname=dpname)
            self.set_status(status)
            self.write(json_encode(data))

class UserConfigHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        status,data=ifaceops.get_user_config_operation(username=self.user)
        self.render('config.html',userdata=data,page_title='Komlog')

class UserProfileHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        status,data=ifaceops.get_user_profile_operation(username=self.user)
        self.render('profile.html',data=data,page_title='Komlog')

    @auth.userauthenticated
    def put(self):
        try:
            data=json_decode(self.request.body)
        except ValueError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.update_user_profile_operation(username=self.user, data=data)
            self.set_status(status)
            self.write(json_encode(data))

class UserHomeHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        self.render('home.html', page_title='Komlog')

class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            errorcode=self.get_argument("error")
        except:
            errorcode=""
        self.render('login.html',errorcode=errorcode)

    def post(self):
        error="?error=1"
        try:
            username=self.get_argument('username')
            password=self.get_argument('password')
            agentid=self.get_argument('agent',None)
            signature=self.get_argument('signature',None)
        except Exception:
            self.redirect(self.get_login_url()+error)
        else:
            status,data=ifaceops.login_operation(username=username, password=password, agentid=agentid, signature=signature)
            if status==ifaceops.STATUS_OK:
                self.set_secure_cookie('komlog_user',username,httponly=True)#, secure=True)
                if agentid:
                    self.set_secure_cookie('komlog_agent',agentid, httponly=True)#, secure=True)
                    self.redirect('/etc/agent/'+agentid)
                else:
                    self.redirect('/home') 
            else:
                self.clear_cookie('komlog_user')
                self.clear_cookie('komlog_agent')
                self.redirect(self.get_login_url()+error)

class LogoutHandler(tornado.web.RequestHandler):

    def get(self):
        self.clear_cookie("komlog_user")
        self.clear_cookie("komlog_agent")
        self.redirect(self.get_login_url())

class WidgetsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        status,data=ifaceops.get_widgets_config_operation(username=self.user)
        self.set_status(status)
        self.write(json_encode(data))

class WidgetConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_wid):
        try:
            wid=uuid.UUID(p_wid)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            status,data=ifaceops.get_widget_config_operation(username=self.user, wid=wid)
            self.set_status(status)
            self.write(json_encode(data))

class DashboardsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        status,data=ifaceops.get_dashboards_config_operation(username=self.user)
        self.set_status(status)
        self.write(json_encode(data))

class DashboardConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_bid):
        try:
            bid=uuid.UUID(p_bid)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        status,data=ifaceops.get_dashboard_config_operation(username=self.user, bid=bid)
        self.set_status(status)
        self.write(json_encode(data))

UUID4_REGEX='[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
HANDLERS = [(r"/login/?", LoginHandler),
            (r"/logout/?", LogoutHandler),
            (r"/etc/ag/?", AgentsHandler),
            (r"/etc/ag/("+UUID4_REGEX+")", AgentConfigHandler),
            (r"/etc/ds/?", DatasourcesHandler),
            (r"/etc/ds/("+UUID4_REGEX+")", DatasourceConfigHandler),
            (r"/etc/dp/?", DatapointsHandler),
            (r"/etc/dp/("+UUID4_REGEX+")", DatapointConfigHandler),
            (r"/etc/wg/?", WidgetsHandler),
            (r"/etc/wg/("+UUID4_REGEX+")", WidgetConfigHandler),
            (r"/etc/db/?", DashboardsHandler),
            (r"/etc/db/("+UUID4_REGEX+")", DashboardConfigHandler),
            (r"/etc/usr/confirm/", UserConfirmationHandler),
            (r"/etc/usr/?", UsersHandler),
            (r"/var/ds/("+UUID4_REGEX+")", DatasourceDataHandler),
            (r"/var/dp/("+UUID4_REGEX+")", DatapointDataHandler),
            (r"/home/config", UserConfigHandler),
            (r"/home/profile", UserProfileHandler),
            (r"/home", UserHomeHandler)
]

