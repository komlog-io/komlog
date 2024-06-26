import asyncio
import os
import uuid
import json
import tornado.web
import urllib.parse
from tornado.escape import json_decode
from tornado.template import Template
from komlog.komimc import api as msgapi
from komlog.komlibs.interface.web.api import agent
from komlog.komlibs.interface.web.api import user
from komlog.komlibs.interface.web.api import datasource
from komlog.komlibs.interface.web.api import datapoint
from komlog.komlibs.interface.web.api import widget
from komlog.komlibs.interface.web.api import snapshot
from komlog.komlibs.interface.web.api import dashboard
from komlog.komlibs.interface.web.api import circle
from komlog.komlibs.interface.web.api import login
from komlog.komlibs.interface.web.api import uri
from komlog.komlibs.interface.web.api import events
from komlog.komlibs.interface.web import status
from komlog.komlibs.general.time import timeuuid
from komlog.komfig import logging, config, options
from komlog.komws2 import auth

class KomlogHandler (tornado.web.RequestHandler):

    def static_url(self, path, include_host=None, **kwargs):
        static_path = config.get(options.WEB_STATIC_PATH)
        cdn_url = config.get(options.WEB_CDN_URL)
        if static_path and cdn_url:
            url = urllib.parse.urljoin(base=static_path, url=path)
            return urllib.parse.urljoin(base=cdn_url, url=url)
        elif static_path:
            return urllib.parse.urljoin(base=static_path, url=path)
        elif cdn_url:
            return urllib.parse.urljoin(base=cdn_url, url=path)
        else:
            return path

class AgentsHandler(KomlogHandler):

    @auth.authenticated
    def post(self):
        try:
            req_data=json_decode(self.request.body)
            pubkey=req_data['pubkey']
            version=req_data['version']
            agentname=req_data['agentname']
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=agent.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def get(self):
        response=agent.get_agents_config_request(passport=self.passport, dids_flag=False)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class AgentConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self,aid):
        response=agent.get_agent_config_request(passport=self.passport, aid=aid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self,aid):
        try:
            data=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=agent.update_agent_config_request(passport=self.passport, aid=aid, data=data)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, aid):
        response=agent.delete_agent_request(passport=self.passport, aid=aid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class AgentSuspendHandler(KomlogHandler):

    @auth.authenticated
    def post(self, aid):
        response=agent.suspend_agent_request(passport=self.passport, aid=aid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class AgentActivateHandler(KomlogHandler):

    @auth.authenticated
    def post(self, aid):
        response=agent.activate_agent_request(passport=self.passport, aid=aid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class DatasourceDataHandler(KomlogHandler):

    @auth.authenticated
    def get(self,did):
        try:
            seq=self.get_argument('seq',default=None)
            start_date=self.get_argument('its',default=None) # start date
            end_date=self.get_argument('ets',default=None) # end date
            tid=self.get_argument('t',default=None)
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=datasource.get_datasource_data_request(passport=self.passport, did=did, start_date=start_date, end_date=end_date, seq=seq, tid=tid)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DatasourceConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self,did):
        response=datasource.get_datasource_config_request(passport=self.passport, did=did)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self, did):
        try:
            content=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=datasource.update_datasource_config_request(passport=self.passport, did=did, content=content)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, did):
        response=datasource.delete_datasource_request(passport=self.passport, did=did)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class DatasourcesHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=datasource.get_datasources_config_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class UsersHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=user.get_user_config_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class UserConfirmationHandler(KomlogHandler):

    def get(self):
        #Aquí llega a traves de un enlace generado dinámicamente durante el alta
        try:
            code=self.get_argument('c') #confirmation cod3 
            email=self.get_argument('e') #email
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=user.confirm_user_request(email=email,code=code)
            if response.status == status.WEB_STATUS_OK:
                self.redirect(self.get_login_url())
            else:
                self.set_status(response.status)
                self.write(json.dumps(response.data))

class UserUpgradeHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=user.get_user_upgrade_info_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self):
        try:
            data=json_decode(self.request.body)
            segment = data.get('s')
            token = data.get('t')
        except ValueError:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad Parameters'}))
        else:
            response=user.upgrade_user_segment_request(passport=self.passport, segment=segment, token=token)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DatapointDataHandler(KomlogHandler):

    @auth.authenticated
    def get(self,pid):
        try:
            start_date=self.get_argument('its',default=None) #sd : start date
            end_date=self.get_argument('ets',default=None) #ed : end date
            tid=self.get_argument('t',default=None) #ticket id
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=datapoint.get_datapoint_data_request(passport=self.passport, pid=pid, start_date=start_date, end_date=end_date,tid=tid)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DatapointConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self,pid):
        response=datapoint.get_datapoint_config_request(passport=self.passport, pid=pid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self, pid):
        try:
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad Parameters'}))
        else:
            response=datapoint.update_datapoint_config_request(passport=self.passport, pid=pid, data=data)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, pid):
        response=datapoint.delete_datapoint_request(passport=self.passport, pid=pid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class DatapointsHandler(KomlogHandler):

    @auth.authenticated
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
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=datapoint.new_datasource_datapoint_request(passport=self.passport, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DatapointPositivesHandler(KomlogHandler):

    @auth.authenticated
    def post(self, pid):
        try:
            data=json_decode(self.request.body)
            sequence=data['seq']
            position=data['p']
            length=data['l']
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=datapoint.mark_positive_variable_request(passport=self.passport, pid=pid, sequence=sequence, position=position, length=length)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DatapointNegativesHandler(KomlogHandler):

    @auth.authenticated
    def post(self, pid):
        try:
            data=json_decode(self.request.body)
            sequence=data['seq']
            position=data['p']
            length=data['l']
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=datapoint.mark_negative_variable_request(passport=self.passport, pid=pid, sequence=sequence, position=position, length=length)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DatapointDatasourceHandler(KomlogHandler):

    @auth.authenticated
    def delete(self, pid):
        response=datapoint.dissociate_datapoint_from_datasource_request(passport=self.passport, pid=pid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class UserConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        self.xsrf_token
        self.render('config.html', page_title='Config - Komlog')

    @auth.authenticated
    def put(self):
        try:
            data=json_decode(self.request.body)
        except ValueError:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=user.update_user_config_request(passport=self.passport, data=data)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self):
        response=user.delete_user_request(passport=self.passport)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class UserHomeHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        self.xsrf_token
        self.render('home.html', page_title='Home - Komlog')

class LoginHandler(KomlogHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self):
        self.render('login.html',page_title='Login - Komlog', response=None)

    def post(self):
        try:
            username=self.get_argument('u',None)
            password=self.get_argument('p',None)
            pubkey=self.get_argument('k',None)
            challenge=self.get_argument('c',None)
            signature=self.get_argument('s',None)
            pv=self.get_argument('pv',None)
        except Exception:
            self.redirect(self.get_login_url())
        else:
            response=login.login_request(username=username, password=password, pubkey=pubkey, challenge=challenge, signature=signature, pv=pv)
            if getattr(response,'cookie',None):
                encrypted = auth.encryptCookie(response.cookie)
                self.set_secure_cookie('kid', encrypted, expires_days=6, httponly=True, domain='.'+config.get(options.ROOT_DOMAIN), secure=True)
                del response.cookie
            if isinstance(response.data, dict) and 'redirect' in response.data:
                self.redirect(response.data['redirect'])
            else:
                if pubkey is not None:
                    self.set_status(response.status)
                    self.write(json.dumps(response.data))
                    self.set_header('Content-Type','application/json; charset="utf-8"')
                else:
                    self.render('login.html',page_title='Login - Komlog', response=response)

class LogoutHandler(KomlogHandler):

    def get(self):
        self.clear_all_cookies(domain='.'+config.get(options.ROOT_DOMAIN))
        ctype=self.request.headers.get('Content-Type')
        if not ctype or ctype.find('application/json')<0:
            self.redirect(self.get_login_url())

class WidgetsHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=widget.get_widgets_config_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=widget.new_widget_request(passport=self.passport, data=data)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class WidgetConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self,wid):
        response=widget.get_widget_config_request(passport=self.passport, wid=wid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self, wid):
        try:
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad Parameters'}))
        else:
            response=widget.update_widget_config_request(passport=self.passport, wid=wid, data=data)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, wid):
        response=widget.delete_widget_request(passport=self.passport, wid=wid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class WidgetDatapointsHandler(KomlogHandler):

    @auth.authenticated
    def post(self, wid, pid):
        response=widget.add_datapoint_request(passport=self.passport, wid=wid, pid=pid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, wid, pid):
        response=widget.delete_datapoint_request(passport=self.passport, wid=wid, pid=pid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class WidgetRelatedHandler(KomlogHandler):
    
    @auth.authenticated
    def get(self, wid):
        response=widget.get_related_widgets_request(passport=self.passport, wid=wid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class WidgetSnapshotsHandler(KomlogHandler):

    @auth.authenticated
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
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=snapshot.new_snapshot_request(passport=self.passport, wid=wid, user_list=user_list, cid_list=cid_list, its=its, ets=ets, seq=seq)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DashboardsHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=dashboard.get_dashboards_config_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=dashboard.new_dashboard_request(passport=self.passport, data=data)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class DashboardConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self,bid):
        response=dashboard.get_dashboard_config_request(passport=self.passport, bid=bid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self, bid):
        try:
            data=json_decode(self.request.body)
        except TypeError:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad Parameters'}))
        else:
            response=dashboard.update_dashboard_config_request(passport=self.passport, bid=bid, data=data)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, bid):
        response=dashboard.delete_dashboard_request(passport=self.passport, bid=bid)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class DashboardWidgetsHandler(KomlogHandler):

    @auth.authenticated
    def post(self, bid, wid):
        response=dashboard.add_widget_request(passport=self.passport, bid=bid, wid=wid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, bid, wid):
        response=dashboard.delete_widget_request(passport=self.passport, bid=bid, wid=wid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class SnapshotConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self, nid):
        try:
            tid=self.get_argument('t',default=None) #ticket id
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=snapshot.get_snapshot_config_request(passport=self.passport, nid=nid, tid=tid)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, nid):
        response=snapshot.delete_snapshot_request(passport=self.passport, nid=nid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class CirclesHandler(KomlogHandler):

    @auth.authenticated
    def post(self):
        try:
            req_data=json_decode(self.request.body)
            circlename=req_data['circlename']
            members=req_data['members'] if 'members' in req_data else None
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=circle.new_users_circle_request(passport=self.passport, circlename=circlename, members_list=members)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def get(self):
        response=circle.get_users_circles_config_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class CircleConfigHandler(KomlogHandler):

    @auth.authenticated
    def get(self, cid):
        response=circle.get_users_circle_config_request(passport=self.passport, cid=cid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def put(self,cid):
        try:
            data=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=circle.update_circle_request(passport=self.passport, cid=cid, data=data)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, cid):
        response=circle.delete_circle_request(passport=self.passport, cid=cid)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class CircleMembersHandler(KomlogHandler):

    @auth.authenticated
    def post(self, cid, member):
        response=circle.add_user_to_circle_request(passport=self.passport, cid=cid, member=member)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, cid, member):
        response=circle.delete_user_from_circle_request(passport=self.passport, cid=cid, member=member)
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class UriHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        try:
            req_uri=self.get_argument('uri',default=None) #uri
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=uri.get_uri_request(passport=self.passport, uri=req_uri)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class SharedUriHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=uri.get_uris_shared_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self):
        try:
            data=json_decode(self.request.body)
            req_uri=data['uri'] if 'uri' in data else None
            users = data['users'] if 'users' in data else None
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=uri.unshare_uri_request(passport=self.passport, uri=req_uri, users=users)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            req_uri=data['uri'] if 'uri' in data else None
            users = data['users'] if 'users' in data else None
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=uri.share_uri_request(passport=self.passport, uri=req_uri, users=users)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class SharedWithMeUriHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        response=uri.get_uris_shared_with_me_request(passport=self.passport)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class UserEventsHandler(KomlogHandler):

    @auth.authenticated
    def get(self):
        try:
            ets=self.get_argument('ets',default=None) #end_date
            its=self.get_argument('its',default=None) #end_date
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=events.get_user_events_request(passport=self.passport, ets=ets, its=its)
            self.set_status(response.status)
            self.write(json.dumps(response.data))

class UserEventsResponsesHandler(KomlogHandler):

    @auth.authenticated
    def post(self, seq):
        try:
            req_data=json_decode(self.request.body)
        except Exception:
            self.set_status(400)
            self.write(json.dumps({'message':'Bad parameters'}))
        else:
            response=events.event_response_request(passport=self.passport, seq=seq, data=req_data)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.set_status(response.status)
            self.write(json.dumps(response.data))

    @auth.authenticated
    def delete(self, seq):
        response=events.disable_event_request(passport=self.passport, seq=seq)
        self.set_status(response.status)
        self.write(json.dumps(response.data))

class AppRootHandler(KomlogHandler):

    def get(self):
        self.render('root.html', page_title='Komlog')

class InviteHandler(KomlogHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self):
        self.render('invite_get.html', page_title='Komlog')

    def post(self):
        email=self.get_argument('email',default=None)
        response=user.register_invitation_request(email=email)
        self.render('invite_post.html', page_title='Komlog', response=response)

class SignupHandler(KomlogHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self):
        invitation=self.get_argument('i',default=None) #i : invitation id
        if invitation==None:
            self.redirect('/invite')
        else:
            response=user.check_invitation_request(invitation=invitation)
            self.render('signup_get.html', page_title='Signup - Komlog', response=response)

    def post(self):
        username=self.get_argument('username',default=None)
        password=self.get_argument('password',default=None)
        email=self.get_argument('email',default=None)
        invitation=self.get_argument('i',default=None)
        segment=self.get_argument('s',default=None)
        token=self.get_argument('t',default=None)
        response=user.new_user_request(
            username=username,
            password=password,
            email=email,
            segment=segment,
            token=token,
            invitation=invitation,
            require_invitation=True
        )
        asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
        self.render('signup_post.html', page_title='Signup - Komlog', response=response, invitation=invitation)

class ForgetHandler(KomlogHandler):

    def check_xsrf_cookie(self):
        pass

    def get(self):
        code=self.get_argument('c',default=None) #c : code
        if code==None:
            self.render('forget_get.html', page_title='Forget - Komlog', reset=False)
        else:
            response=user.check_forget_code_request(code=code)
            self.render('forget_get.html', page_title='Forget - Komlog', reset=True, response=response)

    def post(self):
        account=self.get_argument('account',default=None)
        password=self.get_argument('password',default=None)
        code=self.get_argument('c',default=None) #c : code
        if account == None and password == None and code == None:
            self.redirect('/forget')
        elif account != None:
            response=user.register_forget_request(account=account)
            asyncio.ensure_future(msgapi.send_messages(response.imc_messages))
            self.render('forget_post.html', page_title='Forget - Komlog', reset=False, response=response)
        else:
            response=user.reset_password_request(code=code, password=password)
            self.render('forget_post.html', page_title='Forget - Komlog', reset=True, response=response)

class TermsHandler(KomlogHandler):

    def get(self):
        self.render('terms.html', page_title='Terms - Komlog')

class PrivacyHandler(KomlogHandler):

    def get(self):
        self.render('privacy.html', page_title='Privacy - Komlog')

class CookiesHandler(KomlogHandler):

    def get(self):
        self.render('cookies.html', page_title='Cookies - Komlog')

class PricingHandler(KomlogHandler):

    def get(self):
        self.render('pricing.html', page_title='Pricing - Komlog')

UUID_REGEX='[0-9a-fA-F]{32}'
USERNAME_REGEX='[0-9a-z\-_]+'

HANDLERS = [
    (r'/', AppRootHandler),
    (r'/home', UserHomeHandler),
    (r'/config/?', UserConfigHandler),
    (r'/login/?', LoginHandler),
    (r'/invite/?', InviteHandler),
    (r'/signup/?', SignupHandler),
    (r'/forget/?', ForgetHandler),
    (r'/logout/?', LogoutHandler),
    (r'/terms/?', TermsHandler),
    (r'/privacy/?', PrivacyHandler),
    (r'/cookies/?', CookiesHandler),
    (r'/pricing/?', PricingHandler),
    (r'/confirm/', UserConfirmationHandler),
    (r'/etc/ag/?', AgentsHandler),
    (r'/etc/ag/('+UUID_REGEX+')', AgentConfigHandler),
    (r'/etc/ag/('+UUID_REGEX+')/suspend/?', AgentSuspendHandler),
    (r'/etc/ag/('+UUID_REGEX+')/activate/?', AgentActivateHandler),
    (r'/etc/ds/?', DatasourcesHandler),
    (r'/etc/ds/('+UUID_REGEX+')', DatasourceConfigHandler),
    (r'/etc/dp/?', DatapointsHandler),
    (r'/etc/dp/('+UUID_REGEX+')', DatapointConfigHandler),
    (r'/etc/dp/('+UUID_REGEX+')/positives/?', DatapointPositivesHandler),
    (r'/etc/dp/('+UUID_REGEX+')/negatives/?', DatapointNegativesHandler),
    (r'/etc/dp/('+UUID_REGEX+')/ds/?', DatapointDatasourceHandler),
    (r'/etc/wg/?', WidgetsHandler),
    (r'/etc/wg/('+UUID_REGEX+')', WidgetConfigHandler),
    (r'/etc/wg/(?P<wid>'+UUID_REGEX+')/dp/(?P<pid>'+UUID_REGEX+')', WidgetDatapointsHandler),
    (r'/etc/wg/(?P<wid>'+UUID_REGEX+')/rel/?', WidgetRelatedHandler),
    (r'/etc/wg/(?P<wid>'+UUID_REGEX+')/sn/?', WidgetSnapshotsHandler),
    (r'/etc/db/?', DashboardsHandler),
    (r'/etc/db/('+UUID_REGEX+')', DashboardConfigHandler),
    (r'/etc/db/(?P<bid>'+UUID_REGEX+')/wg/(?P<wid>'+UUID_REGEX+')', DashboardWidgetsHandler),
    (r'/etc/sn/('+UUID_REGEX+')', SnapshotConfigHandler),
    (r'/etc/cr/?', CirclesHandler),
    (r'/etc/cr/('+UUID_REGEX+')', CircleConfigHandler),
    (r'/etc/cr/(?P<cid>'+UUID_REGEX+')/u/(?P<member>'+USERNAME_REGEX+')',CircleMembersHandler),
    (r'/etc/usr/?', UsersHandler),
    (r'/var/ds/('+UUID_REGEX+')', DatasourceDataHandler),
    (r'/var/dp/('+UUID_REGEX+')', DatapointDataHandler),
    (r'/var/uri/?', UriHandler),
    (r'/var/uri/shared/?', SharedUriHandler),
    (r'/var/uri/sharedwithme/?', SharedWithMeUriHandler),
    (r'/var/usr/ev/?', UserEventsHandler),
    (r'/var/usr/ev/('+UUID_REGEX+')', UserEventsResponsesHandler),
]

