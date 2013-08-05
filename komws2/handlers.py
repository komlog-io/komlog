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
from komlibs.gestaccount import exceptions as gestexcept
import os
import uuid
import datetime
import dateutil.parser

class AgentCreationHandler(tornado.web.RequestHandler):

    def post(self):
        #suponemos que aquí llega una vez ha validado
        username=self.request.headers.get('username')
        password=self.request.headers.get('password')
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
                data=agapi.create_agent(username,ag_name,ag_pubkey,ag_version,self.application.cf)
                print data
                self.set_status(200)
                self.write(json_encode(data))
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

    def get(self,p_aid):
        try:
            aid=uuid.UUID(p_aid)
            data=agapi.get_agentconfig(aid,self.application.cf,dids_flag=True)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.AgentNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Agent Not Found'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class DatasourceDataHandler(tornado.web.RequestHandler):

    def get(self,p_did):
        try:
            did=uuid.UUID(p_did)
            data=dsapi.get_datasourcedata(did,self.application.cf)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.DatasourceNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message': 'Datasource not found'}))
        except Exception as e:
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    def post(self,p_did):
        did=uuid.UUID(p_did)
        ctype=self.request.headers.get('Content-Type')
        content=self.request.body
        dest_dir=self.application.dest_dir
        if ctype.find('application/json')>=0:
            try:
                destfile=dsapi.upload_content(did,content,self.application.cf,dest_dir)
                self.set_status(202)
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

    def get(self,p_did):
        try:
            did=uuid.UUID(p_did)
            data=dsapi.get_datasourceconfig(did,self.application.cf)
            print data
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.DatasourceNotFoundException:
            self.set_status(404)
            self.write(json_encode({'message':'Not Found'}))
        except TypeError:
            self.set_status(400)
            self.write(json_encode({'message':'Bad Request'}))
        except Exception as e:
            #self.application.logger.exception(str(e))
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

    def put(self, p_did):
        try:
            did=uuid.UUID(p_did)
            data=json_loads(self.request.body)
            new_dsinfo=dsapi.update_datasourceconfig(did,self.application.cf,data)
            self.set_status(200)
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

class DatasourceCreationHandler(tornado.web.RequestHandler):

    def post(self):
        #suponemos que aquí llega una vez ha validado
        username=self.request.headers.get('username')
        password=self.request.headers.get('password')
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
                data=dsapi.create_datasource(username,aid,ds_name,ds_type,ds_params,self.application.cf)
                print data
                self.set_status(200)
                self.write(json_encode(data))
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
        #suponemos que aquí llega una vez ha validado capcha o algo asi
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

    def get(self,p_pid):
        try:
            pid=uuid.UUID(p_pid)
            strdate=self.get_argument('ld',default=None) #ld : last date
            date=dateutil.parser.parse(strdate) if strdate else datetime.datetime.utcnow()
            data=dpapi.get_datapointdata(pid,self.application.cf,todate=date)
            self.set_status(200)
            self.write(json_encode(data))
        except gestexcept.DatapointDataNotFoundException as e:
            self.set_status(404)
            print 'Datos no encontrados'
            self.write(json_encode({'message': 'Datapoint data not found','last_date':e.last_date.isoformat()}))
        except Exception as e:
            print str(e)
            self.set_status(500)
            self.write(json_encode({'message':'Internal Error'}))

class DatapointCreationHandler(tornado.web.RequestHandler):

    def post(self):
        #suponemos que aquí llega una vez ha validado
        username=self.request.headers.get('username')
        password=self.request.headers.get('password')
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
                dpapi.create_datapoint(did=did,dsdate=dsdate,pos=cs,length=vl,name=dpname,msgbus=self.application.mb)
                self.set_status(200)
            except gestexcept.DatapointCreationException:
                self.set_status(500)
                self.write(json_encode({'message':'Error, try again later'}))
            except Exception as e:
                print str(e)
                self.set_status(500)
                self.write(json_encode({'message':'Error, try again later'}))

class UserConfigHandler(tornado.web.RequestHandler):
    def get(self,username):
        useruidr=cassapi.get_useruidrelation(username,self.application.cf)
        if not useruidr:
            self.set_status(404)
            self.write(json_encode({'message': 'User not found'}))
        userinfo='/home/'+username+'/info'
        userconfig='/home/'+username+'/config'
        userhome='/home/'+username
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
        self.render('config.html',username=username,userurl=userinfo,userdata=data,userhome=userhome,userconfig=userconfig)

class UserHomeHandler(tornado.web.RequestHandler):
    def get(self,username):
        useruidr=cassapi.get_useruidrelation(username,self.application.cf)
        if not useruidr:
            self.set_status(404)
            self.write(json_encode({'message': 'User not found'}))
        userinfo='/home/'+username+'/info'
        userconfig='/home/'+username+'/config'
        userhome='/home/'+username
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
        self.render('home.html',username=username,userurl=userinfo,userdata=data,userhome=userhome,userconfig=userconfig)

