import sections, options
import re
import json
import uuid
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komlibs.textman import variables
from komlibs.ai import decisiontree


NOTFOUND=1
ALREADYMONITORED=2
DBERROR=3
PENDINGDTREEGENERATION=4

class Gestconsole(modules.Module):
    def __init__(self, config, instance_number):
        super(Gestconsole,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.GESTCONSOLE,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.GESTCONSOLE,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.GESTCONSOLE,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['broker'] = self.config.safe_get(sections.GESTCONSOLE, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Gestconsole module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Gestconsole module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            if mtype==messages.MON_VAR_MESSAGE:
                result,pid,date=self.process_MON_VAR_MESSAGE(message)
                if result:
                    self.logger.debug('Message completed successfully: '+mtype)
                    self.message_bus.sendMessage(messages.GenerateDTreeMessage(pid=pid,date=date))
                else:
                    self.logger.error('Error processing message: '+mtype+' Error: '+str(pid))
                    #self.message_bus.sendMessage(message)
            else:
                self.logger.error('Message Type not supported: '+mtype)
                self.message_bus.sendMessage(message)
    
    def process_MON_VAR_MESSAGE(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Comprobamos que la variable no pertenezca a un datapoint existente
        - Registramos el nuevo datapoint, marcando la variable como muestra positiva
        '''
        did=message.did
        date=message.date
        var=message.var
        name=message.name
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            return False,NOTFOUND,date
        try:
            index=dsmapvar.content.index(var)
        except ValueError:
            return False,NOTFOUND,date
        dsmap=cassapi.get_datasourcemap(did=did,session=self.cf,date=date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=var)
        dsdtprelation=cassapi.get_dsdtprelation(did,self.cf)
        if dsdtprelation:
            for pid in dsdtprelation.dtps:
                dtpinfo=cassapi.get_dtpinfo(pid,{'dtree':u''},self.cf)
                if not dtpinfo:
                    return False,PENDINGDTREEGENERATION,date
                try:
                    stored_dtree=dtpinfo.dbcols['dtree']
                    dtree=decisiontree.DecisionTree(jsontree=json.dumps(stored_dtree))
                    if dtree.evaluate_row(varlist[0].h):
                        return False,ALREADYMONITORED,date
                except KeyError:
                    pass
        else:
            dsdtprelation=cassapi.DsDtpRelation(did=did)
        pid=uuid.uuid4()
        print pid
        newdtp=cassapi.DatapointInfo(pid,name=name,positives=(str(date)+'_'+str(var),),did=did)
        if cassapi.register_dtp(newdtp,dsdtprelation,self.cf):
            return True,newdtp.pid,date
        else:
            return False,DBERROR,date

