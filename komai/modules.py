import sections, options
import re
import json
import dateutil.parser
from datetime import datetime,timedelta
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komlibs.textman import variables
from komlibs.ai import decisiontree

OK=1
ERROR=2

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
            if mtype==messages.MAP_VARS_MESSAGE:
                result,did,date=self.process_MAP_VARS_MESSAGE(message)
                if result:
                    self.logger.debug('Mesage completed successfully: '+mtype)
                    self.message_bus.sendMessage(messages.FillDatapointMessage(did=did,date=date))
                else:
                    self.logger.debug('Error procesing: '+mtype)
            elif mtype==messages.GDTREE_MESSAGE:
                result,pid,date=self.process_GDTREE_MESSAGE(message)
                print result,pid,date
                print type(pid),type(date)
                if result:
                    self.logger.debug('Message completed successfully: '+mtype)
                    self.message_bus.sendMessage(messages.FillDatapointMessage(pid=pid,date=date))
                else:
                    self.logger.debug('Error procesing: '+mtype)
            elif mtype==messages.FILL_DATAPOINT_MESSAGE:
                result,subresult=self.process_FILL_DATAPOINT_MESSAGE(message)
                if result:
                    self.logger.debug('Message completed successfully: '+mtype)
                else:
                    self.logger.debug('Error procesing: '+mtype)
            else:
                self.logger.error('Message Type not supported: '+mtype)
                self.message_bus.sendMessage(message)
    
    def process_MAP_VARS_MESSAGE(self, message):
        '''
        Los pasos son los siguientes:
        - Obtenemos el datasource del mensaje
        - Obtenemos el contenido
        - extraemos las variables que contiene, con la informacion necesaria para ser identificadas univocamente
        - almacenamos esta informacion en bbdd, por un lado todo el contenido de las variables recien extraido, y por otro el listado completo de variables de cada datasource, para acelerar las busquedas
        '''
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
                return True,did,date
            except Exception as e:
                #rollback
                self.logger.exception('Exception creating Map for did '+str(did)+': '+str(e))
                cassapi.remove_datasourcemap(dsmobj.did,dsmobj.date,self.cf)
                return False,None,None
        else:
            self.logger.error('Datasource data not found: '+str(did)+' '+str(date))
            return False,None,None

    def process_GDTREE_MESSAGE(self, message):
        '''
        Los pasos son los siguientes:
        - Obtenemos el pid del mensaje
        - Obtenemos la informacion del datapoint
        - creamos un listado con las muestras que contienen variables positivas o negativas (confirmadas o descartadas por el usuario)
        - por cada una de las muestras, obtenemos las variables y las clasificamos segun la info obtenida del datapoint
        - En base a la clasificacion obtenida, creamos el arbol de decision
        - lo almacenamos en bbdd
        '''
        pid=message.pid
        mdate=message.date
        dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
        did=dtpinfo.did
        samples_to_get=[]
        positives=dtpinfo.dbcols['positives']
        negatives=dtpinfo.dbcols['negatives']
        dtree_training_set=[]
        for positive in positives:
            date,var=positive.split('_')
            samples_to_get.append({'date':dateutil.parser.parse(date),
                                   'var':var,'result':True})
        for negative in negatives:
            date,var=negative.split('_')
            samples_to_get.append({'date':dateutil.parser.parse(date),
                                   'var':var,'result':False})
        dsmaps=[]
        for sample in samples_to_get:
            dsmap=cassapi.get_datasourcemap(did=did,session=self.cf,date=sample['date'])
            varlist=variables.get_varlist(jsoncontent=dsmap.content)
            for var in varlist:
                if str(var.s)==sample['var']:
                    var.h['result']=sample['result']
                else:
                    var.h['result']=False
                dtree_training_set.append(var.h)
        dtree=decisiontree.DecisionTree(rawdata=dtree_training_set)
        dtpinfo.dbcols['dtree']=dtree.get_jsontree()
        if cassapi.update_dtp(dtpinfo,self.cf):
            return True,pid,mdate
        else:
            return False,ERROR,mdate

    def process_FILL_DATAPOINT_MESSAGE(self, message):
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
        pid=message.pid
        did=message.did
        date=message.date #depending on the received param, date will be the date of the did or date of the sample whose pid was monitored or modified
        dsmaps=[]
        dtps=[]
        pidonly_flag=False
        if pid:
            pidonly_flag=True
            print 'ENTRO AQUI????'
            print pid
            dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
            if not dtpinfo:
                self.logger.info('Datapoint info not found: '+str(pid))
                return True,OK
            did=dtpinfo.did
            dtree=decisiontree.DecisionTree(jsontree=json.dumps(dtpinfo.dbcols['dtree']))
            if not dtree:
                self.logger.info('Datapoint Decision tree not found: '+str(pid))
                return True,OK
            dtps.append((dtpinfo,dtree))
            dsinfo=cassapi.get_dsinfo(did,{},self.cf)
            if not dsinfo:
                self.logger.info('Datasource info not found: '+str(dtpinfo.pid))
                return True,OK
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
                return True,OK
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
                        dtp_data=cassapi.DatapointData(pid=dtpinfo.pid,date=dsmap.date,content=var.c)
                        if cassapi.insert_datapointdata(dtp_data,self.cf):
                            dsmapdtps[str(dtpinfo.pid)]=var.s
                            dtplist.remove(dtp)
                            break
                        else:
                            self.logger.error('Error inserting datapoint data: %s_%s' %(dtpinfo.pid,dsmap.date))
                            break
            dsmapdtpsobj=None
            if pidonly_flag:
                dsmapdtpsobj=cassapi.get_datasourcemapdtps(did,dsmap.date,self.cf)
                if dsmapdtpsobj:
                    content=json.loads(dsmapdtpsobj.jsoncontent)
                    for key,value in content.iteritems():
                        content[key]=value
                    dsmapdtpsobj.jsoncontent=json.dumps(content)
                else:
                    dsmapdtpsobj=cassapi.DatasourceMapDtps(did,date=dsmap.date,jsoncontent=json.dumps(dsmapdtps))
            else:
                dsmapdtpsobj=cassapi.DatasourceMapDtps(did,date=dsmap.date,jsoncontent=json.dumps(dsmapdtps))
            if not cassapi.insert_datasourcemapdtps(dsmapdtpsobj,self.cf):
                self.logger.error('Error inserting Datasource Datapoint Map: %s_%s' %(did,dsmap.date))
                break
        return True,OK


