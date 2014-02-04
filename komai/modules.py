#coding:utf-8

import sections, options
import re
import json
import dateutil.parser
import operator
from datetime import datetime,timedelta
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komimc import codes as msgcodes
from komlibs.textman import variables
from komlibs.numeric import weight
from komlibs.ai import decisiontree
from komlibs.gestaccount import cards as gestcard


class Textmining(modules.Module):
    def __init__(self, config, instance_number):
        super(Textmining,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.TEXTMINING,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.TEXTMINING,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.TEXTMINING,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['broker'] = self.config.safe_get(sections.TEXTMINING, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Textmining module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Textmining module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                messages.process_msg_result(msgresult,self.message_bus,self.logger)
            except AttributeError:
                self.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                self.logger.exception('Exception processing message: '+str(e))

    def process_msg_MAPVARS(self, message):
        '''
        Los pasos son los siguientes:
        - Obtenemos el datasource del mensaje
        - Obtenemos el contenido
        - extraemos las variables que contiene, con la informacion necesaria para ser identificadas univocamente
        - almacenamos esta informacion en bbdd, por un lado todo el contenido de las variables recien extraido, y por otro el listado completo de variables de cada datasource, para acelerar las busquedas
        '''
        msgresult=messages.MessageResult(message)
        did=message.did
        date=message.date
        varlist=[]
        dsdata=cassapi.get_datasourcedata(did,date,self.cf)
        if dsdata:
            ds_content=dsdata.content
            varlist = variables.get_varlist(ds_content)
            mapcontentlist=[]
            mapvarcontentlist=[]
            for var in varlist:
                content=var.__dict__
                mapcontentlist.append(content)
                mapvarcontentlist.append((content['s'],content['l']))
            mapcontentjson=json.dumps(mapcontentlist)
            mapvarcontentjson=json.dumps(mapvarcontentlist)
            dsmobj=cassapi.DatasourceMap(did=did,date=date,content=mapcontentjson)
            dsmvobj=cassapi.DatasourceMapVars(did=did,date=date,content=mapvarcontentjson)
            try:
                if cassapi.insert_datasourcemap(dsmobj,dsmvobj,self.cf):
                    self.logger.debug('Map created for did: '+str(did))
                dsinfo=cassapi.DatasourceInfo(did,last_mapped=date)
                cassapi.update_ds(dsinfo,self.cf)
                newmsg=messages.FillDatapointMessage(did=did,date=date)
                msgresult.add_msg_originated(newmsg)
                msgresult.retcode=msgcodes.SUCCESS
            except Exception as e:
                #rollback
                self.logger.exception('Exception creating Map for did '+str(did)+': '+str(e))
                cassapi.remove_datasourcemap(dsmobj.did,dsmobj.date,self.cf)
                msgresult.retcode=msgcodes.ERROR
        else:
            self.logger.error('Datasource data not found: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
        return msgresult
            

    def process_msg_GDTREE(self, message):
        '''
        Los pasos son los siguientes:
        - Obtenemos el pid del mensaje
        - Obtenemos la informacion del datapoint
        - creamos un listado con las muestras que contienen variables positivas o negativas (confirmadas o descartadas por el usuario)
        - por cada una de las muestras, obtenemos las variables y las clasificamos segun la info obtenida del datapoint
        - En base a la clasificacion obtenida, creamos el arbol de decision
        - lo almacenamos en bbdd
        '''
        msgresult=messages.MessageResult(message)
        pid=message.pid
        mdate=message.date
        dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
        if not dtpinfo:
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        did=dtpinfo.did
        dates_to_get=[]
        positive_samples={}
        negative_samples={}
        dtp_positives=cassapi.get_dtp_dtree_positives(pid,self.cf)
        dtp_negatives=cassapi.get_dtp_dtree_negatives(pid,self.cf)
        dtree_training_set=[]
        if dtp_positives:
            positive_samples=dtp_positives.positives
            for date,positive in positive_samples.iteritems():
                dates_to_get.append(date)
        if dtp_negatives:
            negative_samples=dtp_negatives.negatives
            for date,negative_array in negative_samples.iteritems():
                dates_to_get.append(date)
        dates_to_get=sorted(set(dates_to_get))
        dsmaps=[]
        for date in dates_to_get:
            dsmap=cassapi.get_datasourcemap(did=did,session=self.cf,date=date)
            varlist=variables.get_varlist(jsoncontent=dsmap.content)
            if positive_samples.has_key(date):
                positive=positive_samples[date]
                for var in varlist:
                    if str(var.s)==positive[0]:
                        var.h['result']=True
                    else:
                        var.h['result']=False
                    dtree_training_set.append(var.h)
            if negative_samples.has_key(date) and not positive_samples.has_key(date):
                negative_list=negative_samples[date]
                for var in varlist:
                    if str(var.s) in negative_list:
                        var.h['result']=False
                        dtree_training_set.append(var.h)
        dtree=decisiontree.DecisionTree(rawdata=dtree_training_set)
        dtpinfo.dbcols['dtree']=dtree.get_jsontree()
        if cassapi.update_dtp(dtpinfo,self.cf):
            newmsg=messages.FillDatapointMessage(pid=pid,date=mdate)
            msgresult.add_msg_originated(newmsg)
            msgresult.retcode=msgcodes.SUCCESS
        else:
            msgresult.retcode=msgcodes.ERROR
        return msgresult

    def process_msg_FILDTP(self, message):
        '''
        Los pasos son los siguientes:
        - Obtenemos el pid o el did y date
        - Si recibimos did y date:
          - Lista de variables: las de la fecha recibida
          - lista de dtrees: la de todos los datapoint asociados al datasource
          - lista de muestras: la de la fecha
        - Si recibimos el pid:
          - lista de variables: las de todas las muestras a almacenar
          - lista de dtree: el del datapoint recibido
          - lista de muestras: DE MOMENTO VAMOS A ALMACENAR DESDE UN MES ATRAS
        - loop:
          - por cada muestra:
            - por cada variable:
              - por cada dtree:
                evalua variable
                if true:
                    almacena_valor
                    break
        '''
        msgresult=messages.MessageResult(message)
        pid=message.pid
        did=message.did
        date=message.date #depending on the received param, date will be the date of the did or date of the sample whose pid was monitored or modified
        dsmaps=[]
        dtps=[]
        pidonly_flag=False
        if pid:
            pidonly_flag=True
            dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
            if not dtpinfo:
                self.logger.error('Datapoint not found: '+str(pid))
                msgresult.retcode=msgcodes.ERROR
                return msgresult
            did=dtpinfo.did
            dtree=decisiontree.DecisionTree(jsontree=json.dumps(dtpinfo.dbcols['dtree']))
            if not dtree:
                self.logger.error('Datapoint Decision tree not found: '+str(pid))
                msgresult.retcode=msgcodes.ERROR
                return msgresult
            dtps.append((dtpinfo,dtree))
            dsinfo=cassapi.get_dsinfo(did,{},self.cf)
            if not dsinfo:
                self.logger.error('Datasource not found: '+str(dtpinfo.pid))
                msgresult.retcode=msgcodes.ERROR
                return msgresult
            end_date=dsinfo.last_received
            if not end_date:
                end_date=datetime.utcnow()
            if date > end_date:
                init_date=end_date-timedelta(days=1)
            else:
                init_date=date
            #obtenemos los datos
            dsmaps=cassapi.get_datasourcemap(did=did,session=self.cf,fromdate=init_date,todate=end_date)
        else:
            dsmaps.append(cassapi.get_datasourcemap(did=did,session=self.cf,date=date))
            dsdtpr=cassapi.get_dsdtprelation(did,self.cf)
            if dsdtpr:
                pids=dsdtpr.dtps
            else:
                self.logger.info('Datasource has no datapoints: '+str(did))
                msgresult.retcode=msgcodes.NOOP
                return msgresult
            for pid in pids:
                dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
                dtree=decisiontree.DecisionTree(jsontree=json.dumps(dtpinfo.dbcols['dtree']))
                dtps.append((dtpinfo,dtree))
        for dsmap in dsmaps:
            varlist=variables.get_varlist(jsoncontent=dsmap.content)
            dtplist=list(dtps)
            dsmapdtps={}
            for var in varlist:
                for dtp in dtplist:
                    dtpinfo,dtree=dtp
                    if dtree.evaluate_row(var.h):
                        value,separator=variables.get_numericvalueandseparator(dtpinfo,varlist,var)
                        dtp_data=cassapi.DatapointData(pid=dtpinfo.pid,date=dsmap.date,content=value)
                        if cassapi.insert_datapointdata(dtp_data,self.cf):
                            dsmapdtps[str(dtpinfo.pid)]=var.s
                            dtplist.remove(dtp)
                            ''' Update datapoint separator info '''
                            if not dtpinfo.get_decimalseparator():
                                if separator:
                                    dtpinfo.set_decimalseparator(separator)
                                    cassapi.update_dtp(dtpinfo,self.cf)
                            break
                        else:
                            self.logger.error('Error inserting datapoint data: %s_%s' %(dtpinfo.pid,dsmap.date))
                            break
            dsmapdtpsobj=None
            if pidonly_flag:
                dsmapdtpsobj=cassapi.get_datasourcemapdtps(did,dsmap.date,self.cf)
                if dsmapdtpsobj:
                    content=json.loads(dsmapdtpsobj.jsoncontent)
                    for key,value in dsmapdtps.iteritems():
                        content[key]=value
                    dsmapdtpsobj.jsoncontent=json.dumps(content)
                else:
                    dsmapdtpsobj=cassapi.DatasourceMapDtps(did,date=dsmap.date,jsoncontent=json.dumps(dsmapdtps))
            else:
                dsmapdtpsobj=cassapi.DatasourceMapDtps(did,date=dsmap.date,jsoncontent=json.dumps(dsmapdtps))
            if not cassapi.insert_datasourcemapdtps(dsmapdtpsobj,self.cf):
                self.logger.error('Error inserting Datasource Datapoint Map: %s_%s' %(did,dsmap.date))
                break
        newmsg=messages.UpdateCardMessage(did=did,date=date)
        msgresult.add_msg_originated(newmsg)
        msgresult.retcode=msgcodes.SUCCESS
        return msgresult

    def process_msg_UPDGRW(self,message):
        '''
        This function associates each graph with the datasources
        it should be related with, and determines the importance (weight) of
        the graph to the datasource
        procedure:
        1) select all datapoints associated with the graph
        2) for each datapoint, select its datasource
        3) Group datapoints by datasource
        4) apply relevance measurement algorithm
        5) store results
        '''
        msgresult=messages.MessageResult(message)
        gid=message.gid
        graphinfo=cassapi.get_graphinfo(gid,self.cf)
        if not graphinfo:
            self.logger.error('Graph info not found: '+str(gid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        datasources={}
        for pid in graphinfo.get_datapoints():
            dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
            try:
                did=dtpinfo.did
                datasources[did].append(pid)
            except KeyError:
                datasources[did]=[]
                datasources[did].append(pid)
            except Exception:
                pass
        weights=weight.relevanceweight(datasources)
        graphdsw=cassapi.get_graphdatasourceweight(gid,self.cf)
        if graphdsw:
            cassapi.delete_graphdatasourceweight(graphdsw,self.cf)
        graphdsw=cassapi.GraphDatasourceWeight(gid)
        graphdsw.set_data(weights)
        if not cassapi.insert_graphdatasourceweight(graphdsw,self.cf):
            self.logger.error('Error inserting GraphDatasourceWeight: '+str(gid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        for did in datasources.keys():
            dsgw=cassapi.DatasourceGraphWeight(did)
            dsgw.add_graph(gid,weights[did])
            cassapi.insert_datasourcegraphweight(dsgw,self.cf)
        self.logger.info('Graph Weight updated successfully: '+str(gid))
        msgresult.retcode=msgcodes.SUCCESS
        return msgresult

class Cardmanager(modules.Module):
    def __init__(self, config, instance_number):
        super(Cardmanager,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.CARDMANAGER,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.CARDMANAGER,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.CARDMANAGER,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['broker'] = self.config.safe_get(sections.CARDMANAGER, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Cardmanager module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Cardmanager module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                messages.process_msg_result(msgresult,self.message_bus,self.logger)
            except AttributeError:
                self.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                self.logger.exception('Exception processing message: '+str(e))

    def process_msg_UPDCARD(self, message):
        msgresult=messages.MessageResult(message)
        did=message.did
        date=message.date
        force=message.force
        dscard=cassapi.get_datasourcecard(did,self.cf)
        dsinfo=cassapi.get_dsinfo(did,{},self.cf)
        if not dsinfo:
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        if not dscard:
            dscard=cassapi.DatasourceCard(did)
            force=True
        aginfo=cassapi.get_agentinfo(dsinfo.aid,{},self.cf)
        if not aginfo:
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        if not force:
            last_date=dsinfo.last_mapped
            td=timedelta(minutes=15)
            if date-td>last_date:
                force=True
        if not force:
            msgresult.retcode=msgcodes.NOOP
            return msgresult
        dscard.uid=dsinfo.uid
        dscard.aid=dsinfo.aid
        dscard.ds_name=dsinfo.dsname
        dscard.ag_name=aginfo.agentname
        dscard.ds_date=date
        dscard.empty_graphs()
        dscard.empty_datapoints()
        dscard.empty_anomalies()
        dsgraphw=cassapi.get_datasourcegraphweight(did,self.cf)
        graph_msgs=[]
        pids=[]
        if dsgraphw:
            sorted_by_w=sorted(dsgraphw.gids.iteritems(),key=operator.itemgetter(1))
            num_graphs=len(sorted_by_w)
            max_gids=2
            c_gid=0
            for i in reversed(range(num_graphs)):
                if c_gid<max_gids:
                    gid=sorted_by_w[i][0]
                    dscard.add_graph(gid)
                    graph_msg=messages.PlotStoreMessage(gid=gid,end_date=date)
                    graph_msgs.append(graph_msg)
                    c_gid+=1
            gids=dscard.get_graphs()
            max_pids=5
            c_pid=0
            for gid in gids:
                if c_pid<max_pids:
                    gdtpr=cassapi.get_graphdatapointrelation(gid,self.cf)
                    if gdtpr:
                        for pid in gdtpr.pids:
                            if c_pid<max_pids:
                                pids.append(pid)
                                c_pid+=1
                            else:
                                break
                else:
                    break
        else:
            dsdtpr=cassapi.get_dsdtprelation(did,self.cf)
            max_pids=5
            c_pid=0
            for pid in dsdtpr.dtps:
                if c_pid<max_pids:
                    pids.append(pid)
                    c_pid+=1
                else:
                    break
        for pid in pids:
            dtpinfo=cassapi.get_dtpinfo(pid,{'name':'','default_color':''},self.cf)
            dtpdata=cassapi.get_datapointdata(pid,self.cf,date=date)
            if dtpdata and dtpinfo:
                if not dtpinfo.dbcols.has_key('default_color'):
                    dtpinfo.dbcols['default_color']='#FF00FF'
                dscard.add_datapoint(dtpinfo.dbcols['name'],dtpdata.content,dtpinfo.dbcols['default_color'])
        priority=gestcard.calculate_card_priority(dscard)
        userdscard=cassapi.UserDsCard(dscard.uid)
        agentdscard=cassapi.AgentDsCard(dscard.aid)
        if dscard.priority==None:
            ''' No existia anteriormente, solo insertamos '''
            dscard.priority=priority
            userdscard.add_card(dscard.did,dscard.priority)
            agentdscard.add_card(dscard.did,dscard.priority)
            cassapi.insert_userdscard(userdscard,self.cf)
            cassapi.insert_agentdscard(agentdscard,self.cf)
        elif not priority==dscard.priority:
            ''' existia anteriormente, con prioridad diferente, borramos los anteriores e insertamos'''
            userdscard.add_card(dscard.did,dscard.priority)
            agentdscard.add_card(dscard.did,dscard.priority)
            cassapi.delete_userdscard(userdscard,self.cf)
            cassapi.delete_agentdscard(agentdscard,self.cf)
            dscard.priority=priority
            userdscard.add_card(dscard.did,dscard.priority)
            agentdscard.add_card(dscard.did,dscard.priority)
            cassapi.insert_userdscard(userdscard,self.cf)
            cassapi.insert_agentdscard(agentdscard,self.cf)
        else:
            ''' existia anteriormente con la misma prioridad. no hacemos nada '''
            pass
        if cassapi.insert_datasourcecard(dscard,self.cf):
            msgresult.retcode=msgcodes.SUCCESS
            for msg in graph_msgs:
                msgresult.add_msg_originated(msg)
        else:
            cassapi.delete_userdscard(userdscard,self.cf)
            cassapi.delete_agentdscard(agentdscard,self.cf)
            cassapi.delete_datasourcecard(dscard,self.cf)
            msgresult.retcode=msgcodes.ERROR
        return msgresult

