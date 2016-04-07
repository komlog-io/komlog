import os
import glob
import time
import signal
from komlog.komapp.modules import modules
from komlog.komfig import logging, config, options
from komlog.komimc import bus as msgbus
from komlog.komimc import api as msgapi
from komlog.komlibs.interface.imc.model import messages

class Validation(modules.Module):
    def __init__(self, instance_number):
        super(Validation,self).__init__(self.__class__.__name__, instance_number)
        self.watchdir = config.get(options.SAMPLES_RECEIVED_PATH)
        self.outputdir = config.get(options.SAMPLES_VALIDATED_PATH)
            
    def start(self):
        signal.signal(signal.SIGTERM,self.signal_handler)
        if not logging.initialize_logging(self.name+'_'+str(self.instance_number)):
            exit()
        logging.logger.info('Module started')
        if not self.watchdir:
            logging.logger.error('Key '+options.SAMPLES_RECEIVED_PATH+' not found')
            exit()
        if not self.outputdir:
            logging.logger.error('Key '+options.SAMPLES_VALIDATED_PATH+' not found')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logging.logger.error('Error initializing broker session')
            exit()
        self.loop()
        self.terminate()
        
    def loop(self):
        while self.run:
            logging.logger.debug('Looking for samples received...')
            files = list(filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*pspl'))))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    try:
                        os.rename(f,f[:-5]+'.qspl')
                    except OSError:
                        #other instance took it firts
                        logging.logger.error('File already treated by other module instance: '+f)
                    else:
                        fi = f[:-5]+'.qspl'
                        if self.validate(fi):
                            try:
                                logging.logger.debug('File validated successfully: '+fi)
                                fo = os.path.join(self.outputdir,os.path.basename(fi)[:-5]+'.vspl')
                                os.rename(fi, fo)
                                msgapi.send_message(messages.StoreSampleMessage(sample_file=fo))
                            except Exception:
                                logging.logger.exception('Error sending: STORE_SAMPLE_MESSAGE')
                                os.rename(fo,fi)
                        else:
                            os.rename(fi,fi[:-5]+'.pspl')                                            
            else:
                time.sleep(5)
    
    def validate(self, filename):
        logging.logger.debug('Validating '+filename)
        return True
