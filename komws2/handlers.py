#!/usr/bin/env python
#coding: utf-8

import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
from komcass import api as cassapi
from komfs import api as fsapi
from komlibs.gestaccount import agents as agapi
from komlibs.gestaccount import datasources as dsapi
from komlibs.gestaccount import exceptions as gestexcept
import os
import uuid
import datetime

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
            self.write(json_encode({'message': 'Agent not found'}))
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

