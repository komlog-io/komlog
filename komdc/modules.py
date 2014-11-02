import sections, options
import os
import glob
import json
import time
import uuid
import dateutil.parser
from komcass.api import datasource as cassapidatasource
from komcass.model.orm import datasource as ormdatasource
from komcass import connection as casscon
from komfs import api as fsapi
from komapp import modules
from komfig import config, logger
from komimc import bus as msgbus
from komimc import api as msgapi
from komimc import messages
from komimc import codes as msgcodes
        
class Validation(modules.Module):
    def __init__(self, instance_number):
        super(Validation,self).__init__(self.__class__.__name__, instance_number)
        self.watchdir = config.config.safe_get(sections.VALIDATION, options.SAMPLES_INPUT_PATH)
        self.outputdir = config.config.safe_get(sections.VALIDATION, options.SAMPLES_OUTPUT_PATH)
        self.broker = config.config.safe_get(sections.VALIDATION, options.MESSAGE_BROKER)
        if not self.broker:
            self.broker = config.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)
            
    def start(self):
        if logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            logger.logger.info('Module started')
        if not self.watchdir:
            logger.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.outputdir:
            logger.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        elif not self.broker:
            logger.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            msgbus.initialize_msgbus(self.broker, self.name, self.instance_number, self.hostname)
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
                        logger.logger.error('File already treated by other module instance: '+f)
                    else:
                        fi = f[:-5]+'.qspl'
                        if self.validate(fi):
                            try:
                                logger.logger.debug('File validated successfully: '+f)
                                fo = os.path.join(self.outputdir,os.path.basename(fi)[:-5]+'.vspl')
                                os.rename(fi, fo)
                                msgapi.send_message(messages.StoreSampleMessage(sample_file=fo))
                            except Exception:
                                logger.logger.exception('Error sending: STORE_SAMPLE_MESSAGE')
                                os.rename(fo,fi)
                        else:
                            os.rename(fi,fi[:-5]+'.pspl')                                            
            else:
                time.sleep(5)
    
    def validate(self, filename):
        logger.logger.debug('Validating '+filename)
        return True

class Storing(modules.Module):
    def __init__(self, instance_number):
        super(Storing,self).__init__(self.__class__.__name__, instance_number)
        self.params={}
        self.params['cassandra_keyspace'] = config.config.safe_get(sections.STORING,options.CASSANDRA_KEYSPACE)
        self.params['cassandra_cluster'] = config.config.safe_get(sections.STORING,options.CASSANDRA_CLUSTER).split(',')
        self.params['watchdir'] = config.config.safe_get(sections.STORING, options.SAMPLES_INPUT_PATH)
        self.params['outputdir'] = config.config.safe_get(sections.STORING, options.SAMPLES_OUTPUT_PATH)
        self.params['broker'] = config.config.safe_get(sections.STORING, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = config.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        if logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            logger.logger.info('Storing module started')
        if not self.params['cassandra_keyspace'] or not self.params['cassandra_cluster']:
            logger.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['watchdir']:
            logger.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.params['outputdir']:
            logger.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        elif not self.params['broker']:
            logger.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            casscon.initialize_session(self.params['cassandra_cluster'],self.params['cassandra_keyspace'])
            msgbus.initialize_msgbus(self.params['broker'], self.name, self.instance_number, self.hostname)
            self.__loop()
        logger.logger.info('Storing module exiting')
    
    def __loop(self):
        while True:
            message = msgapi.retrieve_message()
            mtype = message.type
            logger.logger.debug('Message received: '+mtype)
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                msgapi.process_msg_result(msgresult)
            except AttributeError:
                logger.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                logger.logger.exception('Exception processing message: '+str(e))

    def process_msg_STOSMP(self, message):
            msgresult=messages.MessageResult(message)
            f = message.sample_file
            try:
                os.rename(f,f[:-5]+'.wspl')
            except OSError:
            #other instance took it firts (it shouldn't because messages must be sent once)
                logger.logger.error('File already treated by other module instance: '+f)
                msgresult.retcode=msgcodes.NOOP
            else:
                filename = f[:-5]+'.wspl'
                logger.logger.debug('Storing '+filename)
                metainfo = json.loads(fsapi.get_file_content(filename))
                dsinfo=json.loads(metainfo['json_content'])
                did=uuid.UUID(metainfo['did'])
                ds_content=dsinfo['ds_content']
                ds_date=dateutil.parser.parse(dsinfo['ds_date'])
                dsdobj=ormdatasource.DatasourceData(did=did,date=ds_date,content=ds_content)
                try:
                    if cassapidatasource.insert_datasource_data(dsdobj=dsdobj):
                        cassapidatasource.set_last_received(did=did, last_received=ds_date)
                        logger.logger.debug(filename+' stored successfully : '+str(did)+' '+str(ds_date))
                        fo = os.path.join(self.params['outputdir'],os.path.basename(filename)[:-5]+'.sspl')
                        os.rename(filename,fo)
                        newmsg=messages.MapVarsMessage(did=did,date=ds_date)
                        msgresult.add_msg_originated(newmsg)
                        msgresult.retcode=msgcodes.SUCCESS
                    else:
                        fo = filename[:-5]+'.xspl'
                        os.rename(filename,fo)
                        msgresult.retcode=msgcodes.ERROR
                except Exception as e:
                    cassapidatasource.delete_datasource_data(did=did, date=ds_date)
                    logger.logger.exception('Exception inserting sample: '+str(e))
                    fo = filename[:-5]+'.xspl'
                    os.rename(filename,fo)
                    msgresult.retcode=msgcodes.ERROR
            return msgresult

