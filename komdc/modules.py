import os
import glob
import time
from komcass import connection as casscon
from komfs import api as fsapi
from komapp import modules
from komfig import logger, config, options
from komimc import bus as msgbus
from komimc import api as msgapi
from komimc import messages as imcmessages
from komlibs import messages
        
class Validation(modules.Module):
    def __init__(self, instance_number):
        super(Validation,self).__init__(self.__class__.__name__, instance_number)
        self.watchdir = config.get(options.SAMPLES_RECEIVED_PATH)
        self.outputdir = config.get(options.SAMPLES_VALIDATED_PATH)
            
    def start(self):
        if not logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            exit()
        logger.logger.info('Module started')
        if not self.watchdir:
            logger.logger.error('Key '+options.SAMPLES_RECEIVED_PATH+' not found')
            exit()
        if not self.outputdir:
            logger.logger.error('Key '+options.SAMPLES_VALIDATED_PATH+' not found')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logger.logger.error('Error initializing broker session')
            exit()
        self.__loop()
        logger.logger.info('Module exiting')
        
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
                                msgapi.send_message(imcmessages.StoreSampleMessage(sample_file=fo))
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
        self.params['watchdir'] = config.get(options.SAMPLES_VALIDATED_PATH)
        self.params['outputdir'] = config.get(options.SAMPLES_STORED_PATH)

    def start(self):
        if not logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            exit()
        logger.logger.info('Module started')
        if not casscon.initialize_session():
            logger.logger.error('Error initializing cassandra session')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logger.logger.error('Error initializing broker session')
            exit()
        if not self.params['watchdir']:
            logger.logger.error('Key '+options.SAMPLES_VALIDATED_PATH+' not found')
            exit()
        if not self.params['outputdir']:
            logger.logger.error('Key '+options.SAMPLES_STORED_PATH+' not found')
            exit()
        self.__loop()
        logger.logger.info('Module exiting')
    
    def __loop(self):
        while True:
            message = msgapi.retrieve_message()
            try:
                msgresult=messages.process_message(message)
                if msgresult:
                    msgapi.process_msg_result(msgresult)
                else:
                    logger.logger.error('msgresult is None: '+message.type)
            except AttributeError:
                logger.logger.exception('Exception processing message: '+message.type)
            except Exception as e:
                logger.logger.exception('Exception processing message: '+str(e))

