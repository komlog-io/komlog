import sections, options
import os
import glob
import time
import uuid
import dateutil.parser
from komdb import api as dbapi
from komdb import connection as dbcon
from komcass import api as cassapi
from komcass import connection as casscon
from komfs import api as fsapi
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
        
class Validation(modules.Module):
    def __init__(self, config, instance_number):
        super(Validation,self).__init__(config, self.__class__.__name__, instance_number)
        self.watchdir = self.config.safe_get(sections.VALIDATION, options.SAMPLES_INPUT_PATH)
        self.outputdir = self.config.safe_get(sections.VALIDATION, options.SAMPLES_OUTPUT_PATH)
        self.broker = self.config.safe_get(sections.VALIDATION, options.MESSAGE_BROKER)
        if not self.broker:
            self.broker = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)
            
    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Module started')
        if not self.watchdir:
            self.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.outputdir:
            self.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        elif not self.broker:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.message_bus = bus.MessageBus(self.broker, self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        
    def __loop(self):
        while True:
            files = filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*pspl')))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    try:
                        os.rename(f,f[:-5]+'.qspl')
                    except OSError:
                        #other instance took it firts
                        self.logger.error('File already treated by other module instance: '+f)
                    else:
                        fi = f[:-5]+'.qspl'
                        if self.validate(fi):
                            try:
                                self.logger.debug('File validated successfully: '+f)
                                fo = os.path.join(self.outputdir,os.path.basename(fi)[:-5]+'.vspl')
                                os.rename(fi, fo)
                                self.message_bus.sendMessage(messages.StoreSampleMessage(sample_file=fo))
                            except Exception:
                                self.logger.exception('Error sending: STORE_SAMPLE_MESSAGE')
                                os.rename(fo,fi)
                        else:
                            os.rename(fi,fi[:-5]+'.pspl')                                            
            else:
                time.sleep(5)
    
    def validate(self, filename):
        self.logger.debug('Validating '+filename)
        return True

class Storing(modules.Module):
    def __init__(self, config, instance_number):
        super(Storing,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.STORING,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.STORING,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.STORING,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['watchdir'] = self.config.safe_get(sections.STORING, options.SAMPLES_INPUT_PATH)
        self.params['outputdir'] = self.config.safe_get(sections.STORING, options.SAMPLES_OUTPUT_PATH)
        self.params['broker'] = self.config.safe_get(sections.STORING, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Storing module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['watchdir']:
            self.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.params['outputdir']:
            self.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cass_cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Storing module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype = message.type
            if mtype==messages.STORE_SAMPLE_MESSAGE:
                self.logger.debug('Message received: '+mtype)
                did,date=self.process_STORE_SAMPLE_MESSAGE(message)
                if did:
                    self.logger.debug('Message completed successfully: '+mtype)
                    if not self.message_bus.sendMessage(messages.MapVarsMessage(did=did,date=date)):
                        self.logger.error('Error sending Message: '+messages.MAP_VARS_MESSAGE)
                    self.logger.debug('Message sent: '+messages.MAP_VARS_MESSAGE)
                else:
                    self.logger.error('Error processing message: '+mtype)
            else:
                self.logger.error('Message Type not supported: '+mtype)
                self.message_bus.sendMessage(message)

    def process_STORE_SAMPLE_MESSAGE(self, message):
            f = message.sample_file
            try:
                os.rename(f,f[:-5]+'.wspl')
            except OSError:
            #other instance took it firts (it shouldn't because messages must be sent once)
                self.logger.error('File already treated by other module instance: '+f)
                return -1 
            else:
                filename = f[:-5]+'.wspl'
            
            self.logger.debug('Storing '+filename)
            datasourceid = filename.split('_')[1].split('.')[0]
            if datasourceid == str(152):
                datasourceid = uuid.UUID('7aaedfc9-3850-4752-957f-70f6ccd03d26')
            elif datasourceid == str(156):
                datasourceid = uuid.UUID('31da904f-26a1-4959-be3b-f819963110ab')
            else:
                datasourceid = uuid.UUID(datasourceid)
            date = dateutil.parser.parse(os.path.basename(filename).split('_')[0])
            udata = fsapi.get_file_content(filename)
            dsobj=cassapi.DatasourceData(did=datasourceid,date=date,content=udata)
            try:
                if cassapi.insert_datasourcedata(dsobj,self.cass_cf):
                    self.logger.debug(filename+' stored successfully : '+str(datasourceid)+' '+str(date))
                    fo = os.path.join(self.params['outputdir'],os.path.basename(filename)[:-5]+'.sspl')
                    os.rename(filename,fo)
                    return datasourceid,date
                else:
                    fo = filename[:-5]+'.xspl'
                    os.rename(filename,fo)
                    return None,None
            except Exception as e:
                cassapi.remove_datasourcedata(datasourceid,date,self.cass_cf)
                self.logger.exception('Exception inserting sample: '+str(e))
                fo = filename[:-5]+'.xspl'
                os.rename(filename,fo)
                return None,None


