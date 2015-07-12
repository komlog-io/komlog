#coding: utf-8

import os
import uuid
import json
import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
from komlibs.interface.web.api import agent
from komlibs.interface.web.api import user
from komlibs.interface.web.api import datasource
from komlibs.interface.web.api import datapoint
from komlibs.interface.web.api import widget
from komlibs.interface.web.api import login
from komlibs.interface.web.api import uri
from komlibs.interface.web import status
from komlibs.general.time import timeuuid
from komfig import logger
from komws2 import auth

class BaseHandler(tornado.web.RequestHandler):
    
    @auth.userauthenticated
    def get_current_user(self):
        return self.get_secure_cookie('komlog_user')

class AgentsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            req_data=json_decode(self.request.body)
            pubkey=req_data['pubkey']
            version=req_data['version']
            agentname=req_data['agentname']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=agent.new_agent_request(username=self.user, agentname=agentname, pubkey=pubkey, version=version)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def get(self):
        response=agent.get_agents_config_request(username=self.user)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class AgentConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,aid):
        response=agent.get_agent_config_request(username=self.user, aid=aid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def put(self,aid):
        try:
            data=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=agent.update_agent_config_request(username=self.user, aid=aid, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, aid):
        response=agent.delete_agent_request(username=self.user, aid=aid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class DatasourceDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,did):
        try:
            seq=self.get_argument('seq',default=None)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datasource.get_datasource_data_request(username=self.user, did=did, seq=seq)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.agentauthenticated
    def post(self,did):
        try:
            aid=self.agent
            ctype=self.request.headers.get('Content-Type')
            content=self.request.body.decode('utf-8')
            dest_dir=self.application.dest_dir
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            if ctype.find('application/json')>=0:
                response=datasource.upload_datasource_data_request(username=self.user, aid=aid, did=did, content=content, destination=dest_dir)
                self.set_status(response.status)
                self.write(json_encode(response.data))
            else:
                self.set_status(400)
                self.write(json_encode({'message':'Bad Request'}))

class DatasourceConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,did):
        response=datasource.get_datasource_config_request(username=self.user, did=did)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def put(self, did):
        try:
            content=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datasource.update_datasource_config_request(username=self.user, did=did, content=content)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, did):
        response=datasource.delete_datasource_request(username=self.user, did=did)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class DatasourcesHandler(tornado.web.RequestHandler):

    @auth.agentauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            datasourcename=data['datasourcename']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datasource.new_datasource_request(username=self.user, aid=self.agent, datasourcename=datasourcename)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def get(self):
        response=datasource.get_datasources_config_request(username=self.user)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class UsersHandler(tornado.web.RequestHandler):
    def post(self):
        #suponemos que aquí llega una vez ha validado capcha o algo asi
        try:
            data=json_decode(self.request.body)
            username=data['username']
            password=data['password']
            email=data['email']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=user.new_user_request(username=username,password=password,email=email)
            self.set_status(response.status)
            self.write(json_encode(response.data))

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
            response=user.confirm_user_request(email=email,code=code)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class DatapointDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,pid):
        try:
            start_date=self.get_argument('its',default=None) #sd : start date
            end_date=self.get_argument('ets',default=None) #ed : end date
            iseq=self.get_argument('iseq',default=None)
            eseq=self.get_argument('eseq',default=None)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datapoint.get_datapoint_data_request(username=self.user, pid=pid, start_date=start_date, end_date=end_date,iseq=iseq,eseq=eseq)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class DatapointConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,pid):
        response=datapoint.get_datapoint_config_request(username=self.user, pid=pid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def put(self, pid):
        try:
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        else:
            response=datapoint.update_datapoint_config_request(username=self.user, pid=pid, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, pid):
        response=datapoint.delete_datapoint_request(username=self.user, pid=pid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class DatapointsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            sequence=data['seq']
            did=data['did']
            position=data['p']
            length=data['l']
            datapointname=data['datapointname'] #dp name
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datapoint.new_datapoint_request(username=self.user, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class DatapointPositivesHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self, pid):
        try:
            data=json_decode(self.request.body)
            sequence=data['seq']
            position=data['p']
            length=data['l']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datapoint.mark_positive_variable_request(username=self.user, pid=pid, sequence=sequence, position=position, length=length)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class DatapointNegativesHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self, pid):
        try:
            data=json_decode(self.request.body)
            sequence=data['seq']
            position=data['p']
            length=data['l']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=datapoint.mark_negative_variable_request(username=self.user, pid=pid, sequence=sequence, position=position, length=length)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class UserConfigHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        response=user.get_user_config_request(username=self.user)
        self.render('config.html',userdata=response.data,page_title='Komlog')

    @auth.userauthenticated
    def put(self):
        try:
            data=json_decode(self.request.body)
        except ValueError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=user.update_user_config_request(username=self.user, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self):
        response=user.delete_user_request(username=self.user)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class UserHomeHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        self.render('home.html', page_title='Komlog')

class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            errorcode=self.get_argument('error')
        except:
            errorcode=''
        self.render('login.html',errorcode=errorcode)

    def post(self):
        error='?error=1'
        try:
            username=self.get_argument('username')
            password=self.get_argument('password')
            agentid=self.get_argument('agent',None)
            signature=self.get_argument('signature',None)
        except Exception:
            self.redirect(self.get_login_url()+error)
        else:
            response=login.login_request(username=username, password=password, agentid=agentid, signature=signature)
            logger.logger.debug('LOGIN RESULT: '+str(response.__dict__))
            if response.status==status.WEB_STATUS_OK:
                self.set_secure_cookie('komlog_user',username,httponly=True)#, secure=True)
                if agentid:
                    aid=uuid.UUID(agentid)
                    self.set_secure_cookie('komlog_agent',agentid, httponly=True)#, secure=True)
                    self.redirect('/etc/ag/'+aid.hex)
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
        response=widget.get_widgets_config_request(username=self.user)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
        except Exception as e:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=widget.new_widget_request(username=self.user, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class WidgetConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,wid):
        response=widget.get_widget_config_request(username=self.user, wid=wid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def put(self, wid):
        try:
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        else:
            response=widget.update_widget_config_request(username=self.user, wid=wid, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, wid):
        response=widget.delete_widget_request(username=self.user, wid=wid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class WidgetDatapointsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self, wid, pid):
        response=widget.add_datapoint_request(username=self.user, wid=wid, pid=pid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, wid, pid):
        response=widget.delete_datapoint_request(username=self.user, wid=wid, pid=pid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class WidgetSnapshotsHandler(tornado.web.RequestHandler):
    
    @auth.userauthenticated
    def post(self, wid):
        try:
            data=json_decode(self.request.body)
            its=data['its'] if 'its' in data else None
            ets=data['ets'] if 'ets' in data else None
            seq=data['seq'] if 'seq' in data else None
            user_list=data['ul'] if 'ul' in data else None
            cid_list=data['cl'] if 'cl' in data else None
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=snapshot.new_snapshot_request(username=self.user, wid=wid, user_list=user_list, cid_list=cid_list, its=its, ets=ets, seq=seq)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class DashboardsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        response=dashboard.get_dashboards_config_request(username=self.user)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class DashboardConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,bid):
        response=dashboard.get_dashboard_config_request(username=self.user, bid=bid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def put(self, bid):
        try:
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        else:
            response=dashboard.update_dashboard_config_request(username=self.user, bid=bid, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, bid):
        response=dashboard.delete_dashboard_request(username=self.user, bid=bid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class DashboardWidgetsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self, bid, wid):
        response=dashboard.add_widget_request(username=self.user, bid=bid, wid=wid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, bid, wid):
        response=dashboard.delete_widget_request(username=self.user, bid=bid, wid=wid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class SnapshotConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self, nid):
        response=snapshot.get_snapshot_config_request(username=self.user, nid=nid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, nid):
        response=snapshot.delete_snapshot_request(username=self.user, nid=nid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class CirclesHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            req_data=json_decode(self.request.body)
            circlename=req_data['circlename']
            members=req_data['members'] if 'members' in req_data else None
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=circle.new_circle_request(username=self.user, circlename=circlename, members_list=members)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def get(self):
        response=circle.get_users_circles_config_request(username=self.user)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class CircleConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self, cid):
        response=circle.get_users_circle_config_request(username=self.user, cid=cid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def put(self,cid):
        try:
            data=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=circle.update_circle_request(username=self.user, cid=cid, data=data)
            self.set_status(response.status)
            self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, cid):
        response=circle.delete_circle_request(username=self.user, cid=cid)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class CircleMembersHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self, cid, member):
        response=circle.add_user_to_circle_request(username=self.user, cid=cid, member=member)
        self.set_status(response.status)
        self.write(json_encode(response.data))

    @auth.userauthenticated
    def delete(self, cid, member):
        response=circle.delete_user_from_circle_request(username=self.user, cid=cid, member=member)
        self.set_status(response.status)
        self.write(json_encode(response.data))

class UriHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        try:
            req_uri=self.get_argument('uri',default=None) #uri
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=uri.get_uri_request(username=self.user, uri=req_uri)
            self.set_status(response.status)
            self.write(json_encode(response.data))

class UserEventsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        try:
            end_date=self.get_argument('ets',default=None) #end_date
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            response=events.get_user_events_request(username=self.user, end_date=end_date)
            self.set_status(response.status)
            self.write(json_encode(response.data))

UUID4_REGEX='[0-9a-fA-F]{32}'
USERNAME_REGEX='[0-9a-z\-_]+'

HANDLERS = [(r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/etc/ag/?', AgentsHandler),
            (r'/etc/ag/('+UUID4_REGEX+')', AgentConfigHandler),
            (r'/etc/ds/?', DatasourcesHandler),
            (r'/etc/ds/('+UUID4_REGEX+')', DatasourceConfigHandler),
            (r'/etc/dp/?', DatapointsHandler),
            (r'/etc/dp/('+UUID4_REGEX+')', DatapointConfigHandler),
            (r'/etc/dp/('+UUID4_REGEX+')/positives/?', DatapointPositivesHandler),
            (r'/etc/dp/('+UUID4_REGEX+')/negatives/?', DatapointNegativesHandler),
            (r'/etc/wg/?', WidgetsHandler),
            (r'/etc/wg/('+UUID4_REGEX+')', WidgetConfigHandler),
            (r'/etc/wg/(?P<wid>'+UUID4_REGEX+')/dp/(?P<pid>'+UUID4_REGEX+')', WidgetDatapointsHandler),
            (r'/etc/wg/(?P<wid>'+UUID4_REGEX+')/sn/?', WidgetSnapshotsHandler),
            (r'/etc/db/?', DashboardsHandler),
            (r'/etc/db/('+UUID4_REGEX+')', DashboardConfigHandler),
            (r'/etc/db/(?P<bid>'+UUID4_REGEX+')/wg/(?P<wid>'+UUID4_REGEX+')', DashboardWidgetsHandler),
            (r'/etc/sn/('+UUID4_REGEX+')', SnapshotConfigHandler),
            (r'/etc/cr/?', CirclesHandler),
            (r'/etc/cr/('+UUID4_REGEX+')', CircleConfigHandler),
            (r'/etc/cr/(?P<cid>'+UUID4_REGEX+')/u/(?P<member>'+USERNAME_REGEX+')',CircleMembersHandler),
            (r'/etc/usr/confirm/', UserConfirmationHandler),
            (r'/etc/usr/?', UsersHandler),
            (r'/var/ds/('+UUID4_REGEX+')', DatasourceDataHandler),
            (r'/var/dp/('+UUID4_REGEX+')', DatapointDataHandler),
            (r'/var/uri/?', UriHandler),
            (r'/var/usr/ev/?', UserEventsHandler),
            (r'/home/config', UserConfigHandler),
            (r'/home', UserHomeHandler),
            ]

