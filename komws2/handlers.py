#!/usr/bin/env python
#coding: utf-8

import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
from komcass import api as cassapi
from komfs import api as fsapi
from komlibs.gestaccount import users as usrapi
from komlibs.gestaccount import agents as agapi
from komlibs.gestaccount import datasources as dsapi
from komlibs.gestaccount import datapoints as dpapi
from komlibs.gestaccount import graphs as graphapi
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount import cards as gestcards
from komlibs.auth import authorization
from komlibs.auth import exceptions as authexcept
import auth
import os
import uuid
import datetime
import dateutil.parser

class BaseHandler(tornado.web.RequestHandler):
    
    @auth.userauthenticated
    def get_current_user(self):
        return self.get_secure_cookie('komlog_user')

class AgentCreationHandler(tornado.web.RequestHandler):

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
                authorization.authorize_request(request='NewAgentRequest',username=self.user,session=self.application.cf)
                data=agapi.create_agent(self.user,ag_name,ag_pubkey,ag_version,self.application.cf,self.application.mb)
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

class AgentConfigHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def get(self,p_aid):
        try:
            aid=uuid.UUID(p_aid)
            authorization.authorize_request(request='GetAgentConfigRequest',username=self.user,session=self.application.cf,aid=aid)
            data=agapi.get_agentconfig(aid,self.application.cf,dids_flag=True)
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
            authorization.authorize_request('AgentUpdateConfigurationRequest',self.user, aid=aid, session=self.application.cf)
            data=json_decode(self.request.body)
            agapi.update_agent_config(self.user, aid, data, self.application.cf, self.application.mb)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
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
            authorization.authorize_request(request='GetDatasourceDataRequest',username=self.user,session=self.application.cf,did=did)
            data=dsapi.get_datasourcedata(did,self.application.cf)
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
        ctype=self.request.headers.get('Content-Type')
        content=self.request.body
        dest_dir=self.application.dest_dir
        if ctype.find('application/json')>=0:
            try:
                authorization.authorize_request(request='PostDatasourceDataRequest',username=self.user,session=self.application.cf,aid=self.agent,did=did)
                destfile=dsapi.upload_content(did,content,self.application.cf,dest_dir)
                self.set_status(202)
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
            except TypeError:
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
            authorization.authorize_request(request='GetDatasourceConfigRequest',username=self.user,session=self.application.cf,did=did)
            data=dsapi.get_datasourceconfig(did,self.application.cf)
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
            authorization.authorize_request(request='DatasourceUpdateConfigurationRequest',username=self.user,session=self.application.cf,did=did)
            data=json_decode(self.request.body)
            dsapi.update_datasourceconfig(did,self.application.cf,data)
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

class DatasourceCreationHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        #suponemos que aquí llega una vez ha validado
        try:
            data=json_decode(self.request.body)
            aid=uuid.UUID(data['aid'])
            ds_name=str(data['ds_name'])
            ds_type=str(data['ds_type'])
            ds_params=data['ds_params']
        except Exception as e:
            print 'Exception en el handler'
            print str(e)
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                authorization.authorize_request('NewDatasourceRequest',self.user,session=self.application.cf,aid=aid)
                data=dsapi.create_datasource(self.user,aid,ds_name,ds_type,ds_params,self.application.cf,self.application.mb)
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

class UserCreationHandler(tornado.web.RequestHandler):
    def post(self):
        #suponemos que aquí llega una vez ha validado capcha o algo asi
        try:
            data=json_decode(self.request.body)
            username=u''+data['username']
            password=u''+data['password']
            email=u''+data['email']
        except Exception as e:
            print 'Exception en el handler'
            print str(e)
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                print 'llamamos a usrapi.create_user'
                data=usrapi.create_user(username,password,email,self.application.cf,self.application.mb)
                print 'Datos recibidos',
                print data
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
        print 'Entramos en UserConfirmationHandler'
        #Aquí llega a traves de un enlace generado dinámicamente durante el alta
        code=self.get_argument('c') #confirmation cod3 
        print code
        email=self.get_argument('e') #email
        print email
        try:
            print 'llamamos a usrapi.confirm_user'
            data=usrapi.confirm_user(email,code,self.application.cf)
            print 'Datos recibidos',
            print data
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
            authorization.authorize_request(request='GetDatapointDataRequest',username=self.user,session=self.application.cf,pid=pid)
            strdate=self.get_argument('ld',default=None) #ld : last date
            date=dateutil.parser.parse(strdate) if strdate else datetime.datetime.utcnow()
            data=dpapi.get_datapointdata(pid,self.application.cf,todate=date)
            self.set_status(200)
            self.write(json_encode(data))
        except authexcept.AuthorizationException:
            self.set_status(403)
            self.write(json_encode({'message':'Access Denied'}))
        except gestexcept.DatapointDataNotFoundException as e:
            self.set_status(404)
            print 'Datos no encontrados'
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
            authorization.authorize_request(request='GetDatapointConfigRequest',username=self.user,session=self.application.cf,pid=pid)
            data=dpapi.get_datapointconfig(pid,self.application.cf)
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
            authorization.authorize_request(request='DatapointUpdateConfigurationRequest',username=self.user,session=self.application.cf,pid=pid)
            data=json_decode(self.request.body)
            dpapi.update_datapointconfig(pid,self.application.cf,data)
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

class DatapointCreationHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            dsdate=data['ds_date']
            did=data['did']
            cs=data['cs'] #char start
            vl=data['vl'] #var length
            dpname=data['ds_name'] #dp name
        except Exception:
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                authorization.authorize_request(request='NewDatapointRequest',username=self.user,session=self.application.cf,did=did)
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
        useruidr=cassapi.get_useruidrelation(self.current_user,self.application.cf)
        if not useruidr:
            self.set_status(404)
            self.write(json_encode({'message': 'User not found'}))
        useragentr=cassapi.get_useragentrelation(useruidr.uid,self.application.cf)
        data=[]
        if useragentr:
            for aid in useragentr.aids:
                agentinfo=cassapi.get_agentinfo(aid,{},self.application.cf)
                agentdsr=cassapi.get_agentdsrelation(aid,self.application.cf)
                aid_s=str(aid)
                agenturl='/etc/agent/'+aid_s
                dss=[]
                if agentdsr:
                    for did in agentdsr.dids:
                        dsinfo=cassapi.get_dsinfo(did,{},self.application.cf)
                        did_s=str(did)
                        dsurl='/etc/ds/'+did_s
                        dss.append({'ds_name':dsinfo.dsname,'did':did_s,'url':dsurl})
                data.append({'agentname':agentinfo.agentname,'aid':aid_s,'url':agenturl,'dss':dss})
        self.render('config.html',userdata=data,page_title='Komlog - Config',navitem=1)

    @auth.userauthenticated
    def put(self):
        try:
            authorization.authorize_request('UserUpdateConfigurationRequest',self.user, session=self.application.cf)
            data=json_decode(self.request.body)
            usrapi.update_user_configuration(self.user, data, self.application.cf, self.application.mb)
            self.set_status(200)
            self.write(json_encode({'message':'Operation completed'}))
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
            self.write(json_encode({'message':'Houston, had a problem, try it later please.'}))


class UserHomeHandler(BaseHandler):

    @auth.userauthenticated
    def get(self):
        useruidr=cassapi.get_useruidrelation(self.current_user,self.application.cf)
        if not useruidr:
            self.set_status(404)
            self.write(json_encode({'message': 'User not found'}))
        useragentr=cassapi.get_useragentrelation(useruidr.uid,self.application.cf)
        data=[]
        if useragentr:
            for aid in useragentr.aids:
                agentinfo=cassapi.get_agentinfo(aid,{},self.application.cf)
                agentdsr=cassapi.get_agentdsrelation(aid,self.application.cf)
                aid_s=str(aid)
                agenturl='/etc/agent/'+aid_s
                dss=[]
                if agentdsr:
                    for did in agentdsr.dids:
                        dsinfo=cassapi.get_dsinfo(did,{},self.application.cf)
                        did_s=str(did)
                        dsurl='/etc/ds/'+did_s
                        dss.append({'ds_name':dsinfo.dsname,'did':did_s,'url':dsurl})
                data.append({'agentname':agentinfo.agentname,'aid':aid_s,'url':agenturl,'dss':dss})
        ''' now obtain cards data'''
        cards=gestcards.get_homecards(uid=useruidr.uid, session=self.application.cf, msgbus=self.application.mb)
        self.render('home.html',userdata=data,cardsdata=cards, page_title='Komlog - Home',navitem=0)

class GraphCreationHandler(tornado.web.RequestHandler):

    @auth.userauthenticated
    def post(self):
        try:
            data=json_decode(self.request.body)
            graphname=data['graph_name']
            pid=uuid.UUID(data['pid'])
            dtpname=data['datapoint_name']
        except Exception as e:
            print 'Exception en el handler'
            print str(e)
            self.set_status(400)
            self.write(json_encode({'message':'Bad parameters'}))
        else:
            try:
                authorization.authorize_request(request='NewGraphRequest',username=self.user,session=self.application.cf,pid=pid)
                data=graphapi.create_graph(self.user,graphname,pid,dtpname,self.application.cf,self.application.mb)
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
            authorization.authorize_request(request='GetGraphConfigRequest',username=self.user,session=self.application.cf,gid=gid)
            data=graphapi.get_graphconfig(gid,self.application.cf)
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
            authorization.authorize_request(request='GraphUpdateConfigurationRequest',username=self.user,session=self.application.cf,gid=gid)
            data=json_decode(self.request.body)
            graphapi.update_graph_configuration(gid,self.application.cf,data)
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
        agentidsecret=self.get_argument("agentsecret",None)
        useruidr=cassapi.get_useruidrelation(username,self.application.cf)
        error=u"?error=1"
        if useruidr:
            userinfo=cassapi.get_userinfo(useruidr.uid,{'password':u''},self.application.cf)
            print userinfo.__dict__
            if userinfo.password==usrapi.get_hpassword(useruidr.uid,password):
                self.set_secure_cookie("komlog_user",username,httponly=True)#, secure=True)
                if not agentid:
                    self.redirect('/home') 
                else:
                    try:
                        aid=uuid.UUID(agentid)
                    except Exception:
                        self.set_status('400')
                    else:
                        agentinfo=cassapi.get_agentinfo(aid,{'agentkey'},self.application.cf)
                        agentid2=agapi.decrypt(agentinfo.agentkey,agentidsecret)
                        if agentid==agentid2:
                            self.set_secure_cookie('komlog_agent',agentid, httponly=True)#, secure=True)
                            self.redirect('/etc/ag/'+agentid+'/')

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
            authorization.authorize_request(request='GetPlotDataRequest',username=self.user,session=self.application.cf,gid=gid)
            image = graphapi.get_plotimage(username=self.user, session=self.application.cf, msgbus=self.application.mb, gid=gid)
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

