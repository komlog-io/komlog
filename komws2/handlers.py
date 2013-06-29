#!/usr/bin/env python
#coding: utf-8

import tornado.web
from tornado.template import Template
from tornado.escape import json_encode,json_decode,xhtml_escape
from komcass import api as cassapi
from komfs import api as fsapi
import os
import uuid
import datetime

class AgentCreationHandler(tornado.web.RequestHandler):
    def post(self):
        #Durante la validación, es necesario determinar como buscar agentes en función de su key, para ver si el agente que se intenta crear ya está dado de alta
        #suponemos que aquí llega una vez ha validado que el agente no existe y es necesario crearlo
        data=json_decode(self.request.body)
        aid=uuid.UUID4()
        uid='X' #obten el uid del usuario autenticado
        aginfo=cassapi.AgentInfo(aid,agentname=data.ag_name,agentkey=data.ag_pubkey,version=data.ag_version,uid=uid,state='ps')
        if register_agent(aginfo, self.application.cf):
            self.set_status(200)
            response={'aid':str(aid)}
            self.write(json_encode(response))
        else:
            self.status(500)
            self.write(json_encode({'Message':'Internal error'}))

class AgentConfigHandler(tornado.web.RequestHandler):
    def get(self,p_aid):
        aid=uuid.UUID(p_aid)
        agentinfo=cassapi.get_agentinfo(aid,{},self.application.cf)
        if agentinfo:
            agentname=agentinfo.agentname
            state=agentinfo.state
            version=agentinfo.version
            agentdsr=cassapi.get_agentdsrelation(aid,self.application.cf)
            dids=[]
            if agentdsr:
                for did in agentdsr.dids:
                    dids.append(str(did))
            response={'aid':p_aid,'ag_name':agentname,'ag_state':state,'ag_version':version,'dids':dids}
            self.write(json_encode(response))
        else:
            self.set_status(404)
            self.write(json_encode({'Message': 'Agent not found'}))

class DatasourceDataHandler(tornado.web.RequestHandler):
    def get(self,p_did):
        print self._headers
        did=uuid.UUID(p_did)
        dsinfo=cassapi.get_dsinfo(did,{'last_received':u'','last_mapped':u''},self.application.cf)
        if dsinfo:
            last_received=dsinfo.last_received
            last_mapped=dsinfo.last_mapped
            dsdata=cassapi.get_datasourcedata(did,last_received,self.application.cf)
            print last_received,last_mapped
            detectedvars=[]
            if last_mapped and last_mapped==last_received:
                dsmapvars=cassapi.get_datasourcemapvars(did,last_received,self.application.cf)
                if dsmapvars:
                    detectedvars=dsmapvars.content
            location=None
            response={'did':p_did,'ds_content':dsdata.content,'ds_date':last_received.isoformat(),'ds_location':location,'ds_vars':detectedvars}
            self.write(json_encode(response))
        else:
            self.set_status(404)
            self.write(json_encode({'Message': 'Agent not found'}))
    def post(self,p_did):
        did=uuid.UUID(p_did)
        dsinfo=cassapi.get_dsinfo(did,{},self.application.cf)
        if dsinfo:
            ctype=self.request.headers.get('Content-Type')
            if ctype.find('application/json')>=0:
                now=datetime.datetime.utcnow().isoformat()
                requestdata={'received':now,'did':p_did,'json_content':self.request.body}
                try:
                    requestdata_json=json_encode(requestdata)
                except Exception as e:
                    self.set_status(400)
                else:
                    dest_dir=self.application.dest_dir
                    file_name=now+'_'+str(p_did)+'.pspl'
                    dest_file=os.path.join(dest_dir,file_name)
                    if fsapi.create_sample(dest_file,requestdata_json):
                        self.set_status(202)
                    else:
                        self.set_status(500)
        else:
            self.set_status(404)

class DatasourceConfigHandler(tornado.web.RequestHandler):
    def get(self,p_did):
        did=uuid.UUID(p_did)
        dsinfo=cassapi.get_dsinfo(did,{},self.application.cf)
        if dsinfo:
            ds_name=dsinfo.dsname
            last_received=dsinfo.last_received.isoformat() if dsinfo.last_received else None
            ds_type=dsinfo.dstype
            #params=dsinfo.get_params() #La key del diccionario se establece en el api de bbdd, en cambio las keys del json de la respuesta se establecen aquí... Estamos definiendo keys de la respuesta en sitios diferentes, no me gusta esto a nivel de diseño.
            params={'script_name':'sar.sh','min':'*','hour':'*','dow':'*','month':'*','dom':'*'}
            response={'did':p_did,'ds_name':ds_name,'last_received':last_received,'ds_type':ds_type,'ds_params':params}
            self.write(json_encode(response))
        else:
            self.set_status(404)
            self.write(json_encode({'Message': 'Agent not found'}))
    def put(self, p_did):
        did=uuid.UUID(p_did)
        dsinfo=cassapi.get_dsinfo(did,{},self.application.cf)
        if dsinfo:
            try:
                requestdata=json.loads(self.request.body)
                #ahora hay que ver si las keys de la peticion son correctas, antes de modificar el valor de dsinfo
                for key,value in requestdata.iteritems():
                    dsinfo.key=value
                cassapi.update_ds(dsinfo,self.application.cf)
            except Exception as e:
                print 'Exception updating datasource: '+str(e)
                self.set_status(500)
            else:
                self.set_status(200)

class UserConfigHandler(tornado.web.RequestHandler):
    def get(self,username):
        useruidr=cassapi.get_useruidrelation(username,self.application.cf)
        if not useruidr:
            self.set_status(404)
            self.write(json_encode({'Message': 'User not found'}))
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
            self.write(json_encode({'Message': 'User not found'}))
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

