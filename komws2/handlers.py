#!/usr/bin/env python
#coding: utf-8

import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komfs import api as fsapi
from komlibs.gestaccount import user as usrapi
from komlibs.gestaccount import agent as agapi
from komlibs.gestaccount import datasource as dsapi
from komlibs.gestaccount import datapoint as dpapi
from komlibs.gestaccount import widget as wgapi
from komlibs.gestaccount import dashboard as dbapi
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.auth import authorization
from komlibs.auth import exceptions as authexcept
import auth
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
            data=json_decode(self.request.body)
            ag_pubkey=data['ag_pubkey']
            ag_version=data['ag_version']
            ag_name=data['ag_name']
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                print 'autorizamos'
                authorization.authorize_request(request='NewAgentRequest',username=self.user)
                print 'creamos'
                data=agapi.create_agent(self.user,ag_name,ag_pubkey,ag_version,self.application.mb)
                print data
                self.set_status(200)
                self.write(json_encode(data))
            except authexcept.AuthorizationException:
                self.set_status(403)
                self.write(json_encode({'message':'Access Denied'}))
            except gestexcept.UserNotFoundException:
                self.set_status(404)
                self.write(json_encode({'message':'Not Found'}))
            except gestexcept.AgentCreationException:
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

    @auth.userauthenticated
    def get(self):
        try:
            data=agapi.get_agents_config(username=self.user,dids_flag=True)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'User not found'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class AgentConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_aid):
        try:
            aid=uuid.UUID(p_aid)
            authorization.authorize_request(request='GetAgentConfigRequest',username=self.user,aid=aid)
            data=agapi.get_agent_config(aid,dids_flag=True)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access denied'}))
        except gestexcept.AgentNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Agent Not Found'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    @auth.userauthenticated
    def put(self,p_aid):
        try:
            aid=uuid.UUID(p_aid)
            authorization.authorize_request('AgentUpdateConfigurationRequest',self.user, aid=aid)
            data=json_decode(self.request.body)
            agapi.update_agent_config(username=self.user,aid=aid,data=data,msgbus=self.application.mb)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
        except ValueError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except gestexcept.AgentNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Agent Not Found'}))
        except gestexcept.BadParametersException:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class DatasourceDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_did):
        try:
            did=uuid.UUID(p_did)
            authorization.authorize_request(request='GetDatasourceDataRequest',username=self.user,did=did)
            data=dsapi.get_datasource_data(did)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.DatasourceNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message': 'Datasource not found'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    @auth.agentauthenticated
    def post(self,p_did):
        did=uuid.UUID(p_did)
        aid=uuid.UUID(self.agent)
        ctype=self.request.headers.get('Content-Type')
        content=self.request.body
        dest_dir=self.application.dest_dir
        if ctype.find('application/json')>=0:
            try:
                authorization.authorize_request(request='PostDatasourceDataRequest',username=self.user,aid=aid,did=did)
                destfile=dsapi.upload_content(did,content,dest_dir)
                self.set_status(202)
                self.write(json_encode({'message':'Data received'}))
            except authexcept.AuthorizationException:
                self.set_status(403)
                self.write(json_encode({'message':'Access Denied'}))
            except gestexcept.DatasourceUploadContentException:
                print 'uploadexception'
                self.set_status(500)
                self.write(json_encode({'message':'Internal Error'}))
            except gestexcept.DatasourceNotFoundException:
                self.set_status(404)
                self.write(json_encode({'message':'Not Found'}))
            except TypeError as e:
                print str(e)
                self.set_status(400)
                self.write(json_encode({'message':'Bad Parameters'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Internal Error'}))
        else:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))

class DatasourceConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_did):
        try:
            did=uuid.UUID(p_did)
            authorization.authorize_request(request='GetDatasourceConfigRequest',username=self.user,did=did)
            data=dsapi.get_datasource_config(did)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.DatasourceNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    @auth.userauthenticated
    def put(self, p_did):
        try:
            did=uuid.UUID(p_did)
            authorization.authorize_request(request='DatasourceUpdateConfigurationRequest',username=self.user,did=did)
            data=json_decode(self.request.body)
            dsapi.update_datasourceconfig(did=did,data=data)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.BadParametersException:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        except KeyError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        except gestexcept.DatasourceUpdateException:
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))
        except gestexcept.DatasourceNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except Exception as e:
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class DatasourcesHandler(tornado.web.RequestHandler):

    @auth.agentauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            aid=uuid.UUID(self.agent)
            ds_name=data['ds_name']
        except Exception as e:
            print 'Exception en el handler'
            print str(e)
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                authorization.authorize_request('NewDatasourceRequest',self.user,aid=aid)
                data=dsapi.create_datasource(username=self.user,aid=aid,datasourcename=ds_name,msgbus=self.application.mb)
                self.set_status(200)
                self.write(json_encode(data))
            except authexcept.AuthorizationException:
                self.set_status(403)
                self.write(json_encode({'message':'Access Denied'}))
            except gestexcept.UserNotFoundException:
                self.set_status(404)
                self.write(json_encode({'message':'Not Found'}))
            except gestexcept.AgentNotFoundException:
                self.set_status(404)
                self.write(json_encode({'message':'Not Found'}))
            except gestexcept.BadParametersException:
                self.set_status(400)
                self.write(json_encode({'message':'Bad parameters'}))
            except gestexcept.DatasourceCreationException:
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

    @auth.userauthenticated
    def get(self):
        try:
            data=dsapi.get_datasources_config(self.user)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'User not found'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class UsersHandler(tornado.web.RequestHandler):
    def post(self):
        #suponemos que aquí llega una vez ha validado capcha o algo asi
        try:
            data=json_decode(self.request.body)
            username=u''+data['username']
            password=u''+data['password']
            email=u''+data['email']
        except Exception as e:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                data=usrapi.create_user(username,password,email,self.application.mb)
                self.set_status(200)
                self.write(json_encode(data))
            except gestexcept.UserAlreadyExistsException:
                self.set_status(404)
                self.write(json_encode({'message':'User Already Exists'}))
            except gestexcept.BadParametersException:
                self.set_status(400)
                self.write(json_encode({'message':'Bad parameters'}))
            except gestexcept.UserCreationException:
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class UserConfirmationHandler(tornado.web.RequestHandler):

    def get(self):
        #Aquí llega a traves de un enlace generado dinámicamente durante el alta
        code=self.get_argument('c') #confirmation cod3 
        email=self.get_argument('e') #email
        try:
            data=usrapi.confirm_user(email,code)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'User not Found'}))
        except gestexcept.BadParametersException:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except gestexcept.UserCreationException:
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class DatapointDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_pid):
        try:
            pid=uuid.UUID(p_pid)
            authorization.authorize_request(request='GetDatapointDataRequest',username=self.user,pid=pid)
            end_date=self.get_argument('ed',default=None) #ed : end date
            start_date=self.get_argument('sd',default=None) #sd : start date
            end_date=dateutil.parser.parse(end_date) if end_date else None
            start_date=dateutil.parser.parse(start_date) if start_date else None
            data=dpapi.get_datapoint_data(pid,end_date=end_date, start_date=start_date)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.DatapointDataNotFoundException as e:
            self.set_status(404)
            self.write(json_encode({'message': 'Datapoint data not found','last_date':e.last_date.isoformat()}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class DatapointConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_pid):
        try:
            pid=uuid.UUID(p_pid)
            authorization.authorize_request(request='GetDatapointConfigRequest',username=self.user,pid=pid)
            data=dpapi.get_datapoint_config(pid)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.DatapointNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    @auth.userauthenticated
    def put(self, p_pid):
        try:
            pid=uuid.UUID(p_pid)
            authorization.authorize_request(request='DatapointUpdateConfigurationRequest',username=self.user,pid=pid)
            data=json_decode(self.request.body)
            dpapi.update_datapointconfig(pid=pid,data=data)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.BadParametersException:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        except KeyError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Parameters'}))
        except gestexcept.DatapointUpdateException:
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))
        except gestexcept.DatapointNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except Exception as e:
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

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
            try:
                authorization.authorize_request(request='NewDatapointRequest',username=self.user,did=did)
                dpapi.create_datapoint(did=did,dsdate=dsdate,pos=cs,length=vl,name=dpname,msgbus=self.application.mb)
                self.set_status(200)
            except authexcept.AuthorizationException:
                self.set_status(403)
                self.write(json_encode({'message':'Access Denied'}))
            except gestexcept.DatapointCreationException:
                self.set_status(500)
                self.write(json_encode({'message':'Error, try again later'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Error, try again later'}))

class UserConfigHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        user=cassapiuser.get_user(username=self.user)
        if not user:
            self.set_status(404)
            self.write(json_encode({'message': 'User not found'}))
        agents=cassapiagent.get_agents(uid=user.uid)
        data=[]
        if agents:
            for agent in agents:
                datasources=cassapidatasource.get_datasources(aid=agent.aid)
                aid_s=str(agent.aid)
                agenturl='/etc/agent/'+aid_s
                dss=[]
                if datasources:
                    for datasource in datasources:
                        did_s=str(datasource.did)
                        dsurl='/etc/ds/'+did_s
                        dss.append({'ds_name':datasource.datasourcename,'did':did_s,'url':dsurl})
                data.append({'agentname':agent.agentname,'aid':aid_s,'url':agenturl,'dss':dss})
        self.render('config.html',userdata=data,page_title='Komlog')

class UserProfileHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        try:
            data=usrapi.get_userprofile(username=self.user)
            print 'TENEMOS LOS DATOS'
            print data
            self.render('profile.html',data=data,page_title='Komlog')
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

    @auth.userauthenticated
    def put(self):
        try:
            authorization.authorize_request('UserUpdateProfileRequest',self.user)
            data=json_decode(self.request.body)
            usrapi.update_userprofile(self.user, data, self.application.mb)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
        except ValueError:
            self.set_status(400)
            self.write(json_encode({'message':'Error in JSON data received'}))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except gestexcept.BadParametersException:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except Exception as e:
            print str(e)
            self.set_status(500)


class UserHomeHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        self.render('home.html', page_title='Komlog')

class GraphsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            graphname=data['graph_name']
            dtp_list=data['dtp_list']
            pids=[]
            for dtp in dtp_list:
                pids.append(uuid.UUID(dtp))
        except Exception as e:
            print 'Exception en el handler'
            print str(e)
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                for pid in pids:
                    authorization.authorize_request(request='NewGraphRequest',username=self.user,pid=pid)
                data=graphapi.create_graph(username=self.user,graphname=graphname,pids=pids,msgbus=self.application.mb)
                self.set_status(200)
                self.write(json_encode(data))
            except authexcept.AuthorizationException:
                self.set_status(403)
                self.write(json_encode({'message':'Access Denied'}))
            except gestexcept.BadParametersException:
                self.set_status(400)
                self.write(json_encode({'message':'Bad parameters'}))
            except gestexcept.GraphCreationException:
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class GraphConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_gid):
        try:
            gid=uuid.UUID(p_gid)
            authorization.authorize_request(request='GetGraphConfigRequest',username=self.user,gid=gid)
            data=graphapi.get_graphconfig(gid)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.GraphNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    @auth.userauthenticated
    def put(self,p_gid):
        try:
            gid=uuid.UUID(p_gid)
            authorization.authorize_request(request='GraphUpdateConfigurationRequest',username=self.user,gid=gid)
            data=json_decode(self.request.body)
            graphapi.update_graph_configuration(gid,data)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.GraphNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))
        except gestexcept.BadParametersException:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        except gestexcept.GraphUpdateException:
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            errorcode=self.get_argument("error")
        except:
            errorcode=""
        self.render('login.html',errorcode=errorcode)

    def post(self):
        username=self.get_argument("username")
        password=self.get_argument("password")
        agentid=self.get_argument("agent",None)
        signature=self.get_argument("signature",None)
        userinfo=cassapiuser.get_user(username=username)
        error=u"?error=1"
        if userinfo:
            if userinfo.password==usrapi.get_hpassword(userinfo.uid,password):
                self.set_secure_cookie("komlog_user",username,httponly=True)#, secure=True)
                if not agentid:
                    self.redirect('/home') 
                else:
                    try:
                        aid=uuid.UUID(agentid)
                    except Exception:
                        self.set_status('400')
                    else:
                        agentinfo=cassapiagent.get_agent(aid=aid)
                        if agentinfo:
                            if agapi.verify_signature(agentinfo.pubkey,agentid,signature):
                                self.set_secure_cookie('komlog_agent',agentid, httponly=True)#, secure=True)
                                self.redirect('/etc/agent/'+agentid)
                            else:
                                self.clear_cookie("komlog_user")
                                self.set_status(403)
                        else:
                            self.clear_cookie("komlog_user")
                            self.set_status(403)
            else:
                self.redirect(self.get_login_url()+error)
        else:
            self.redirect(self.get_login_url()+error)


class LogoutHandler(tornado.web.RequestHandler):

    def get(self):
        self.clear_cookie("komlog_user")
        self.clear_cookie("komlog_agent")
        self.redirect(self.get_login_url())

class PlotDataHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_gid):
        try:
            gid=uuid.UUID(p_gid)
            authorization.authorize_request(request='GetPlotDataRequest',username=self.user,gid=gid)
            image = graphapi.get_plotimage(username=self.user, msgbus=self.application.mb, gid=gid)
            self.set_header('Content-type', 'image/png')
            self.set_header('Content-length', len(image))
            self.set_status(200)
            self.write(image)
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.DatasourceNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message': 'Datasource not found'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class WidgetsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        try:
            data=wgapi.get_widgets_config(self.user)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'User not found'}))
        except gestexcept.WidgetNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not found widgets'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class WidgetConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_wid):
        try:
            wid=uuid.UUID(p_wid)
            authorization.authorize_request(request='GetWidgetConfigRequest',username=self.user,wid=wid)
            data=wgapi.get_widgetconfig(wid)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access denied'}))
        except gestexcept.WidgetNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Widget Not Found'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class DashboardsHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self):
        try:
            data=dbapi.get_dashboardsconfig(self.user)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.UserNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'User not found'}))
        except gestexcept.DashboardNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not found dashboards'}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))

class DashboardConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_bid):
        try:
            bid=uuid.UUID(p_bid)
            authorization.authorize_request(request='GetDashboardConfigRequest',username=self.user,bid=bid)
            data=dbapi.get_dashboardconfig(bid)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access denied'}))
        except gestexcept.DashboardNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Dashboard Not Found'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

