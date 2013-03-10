import sections, options
import re
import json
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komlibs.textman import variables


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
                if self.process_MAP_VARS_MESSAGE(message):
                    self.logger.debug('Mesage completed successfully: '+mtype)
                    pass
            else:
                self.logger.error('Message Type not supported: '+mtype)
                self.message_bus.sendMessage(message)
    
    def process_MAP_VARS_MESSAGE(self, message):
        did=message.did
        date=message.date
        varlist=[]
        dsdata=cassapi.get_datasourcedata(did,date,self.cf)
        if not dsdata==None:
            ds_content=dsdata.content
            varlist = variables.get_varlist(ds_content)
            mapcontentlist=[]
            mapvarcontentlist=[]
            for var in varlist:
                content=var.__dict__
                mapcontentlist.append(content)
                mapvarcontentlist.append(content['s'])
            mapcontentjson=json.dumps(mapcontentlist)
            mapvarcontentjson=json.dumps(mapvarcontentlist)
            dsmobj=cassapi.DatasourceMap(did=did,date=date,content=mapcontentjson)
            dsmvobj=cassapi.DatasourceMapVars(did=did,date=date,content=mapvarcontentjson)
            try:
                if cassapi.insert_datasourcemap(dsmobj,dsmvobj,self.cf):
                    self.logger.debug('Map created for did: '+str(did))
                return True
            except Exception as e:
                #rollback
                self.logger.exception('Exception creating Map for did '+str(did)+': '+str(e))
                cassapi.remove_datasourcemap(dsmobj.did,dsmobj.date,self.cf)
                return False
        else:
            self.logger.error('Datasource data not found: '+str(did)+' '+str(date))
            return False

