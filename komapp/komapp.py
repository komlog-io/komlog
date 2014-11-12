'''
Created on 31/12/2012

@author: jcazor
'''
import os
import signal
import time
from komfig import config, logger, options
from komapp import modules
from multiprocessing import Process

class Komapp(object):
    def __init__(self,conf_file, program_name):
        self.path, self.conf_file = os.path.split(conf_file)
        self._program_name=program_name
        self.modules = []
        self.processes = []
        self.run = True
        
    def signal_handler(self, signum, frame):
        if signum == signal.SIGTERM:
            logger.logger.info('SIGTERM received, terminating')
            self.run = False
        else:
            logger.logger.info('signal '+str(signum)+' received, ignoring')

    def start(self):
        signal.signal(signal.SIGTERM,self.signal_handler)
        self.load_conf_file()
        if logger.initialize_logger(self._program_name):
            logger.logger.info('Configuration file loaded successfully')
        self.load_modules()
        self.start_modules()
        self.loop()
        self.terminate()

    def load_conf_file(self):
        """
        Load conf_file
        """
        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                if os.path.isfile(os.path.join(self.path, self.conf_file)):
                    if not config.initialize_config(os.path.join(self.path, self.conf_file)):
                        exit()
                else:
                    print("Not a file: "+os.path.join(self.path, self.conf_file))
                    exit()
            else:
                print("Not a directory: "+self.path)
                exit()
        else:
            print("Directory not found: "+self.path)
            exit()
       
    def load_modules(self):
        modules_enabled = []
        for module in config.get(options.MODULES).split(','):
            if str(config.get(options.MODULE_ENABLED, module)).lower() == 'yes':
                instances = config.get(options.MODULE_INSTANCES, module)
                if not instances:
                    instances=1
                else:
                    instances=int(instances)
                try:
                    for c in modules.Module.__subclasses__():
                        if c.__name__ == module[0].upper()+module[1:]:
                            for i in range(instances):
                                modobj = (c(i),i)
                                modules_enabled.append(modobj)
                                modobj = None
                except NameError as e:
                    logger.logger.exception('Module not found: '+str(e))
        self.modules = modules_enabled
        
    def start_modules(self, module=None):
        if not module:
            for i,module in enumerate(self.modules):
                p = Process(target=module[0].start,name=module[0].__class__.__name__+'-'+str(module[1]))
                logger.logger.info('Starting module: '+str(p))
                p.start()
                self.processes.insert(i,p)
        else:
            i = self.modules.index(module)
            if not self.processes[i].is_alive():
                p = Process(target=module[0].start,name=module[0].__class__.__name__+'-'+str(module[1]))
                p.start()
                logger.logger.info('Starting module: '+str(p))
                self.processes.pop(i)
                self.processes.insert(i,p)
            else:
                logger.logger.error('Trying to start an already running module')
            
    def loop(self):
        while self.run:
            time.sleep(5)
            for i, process in enumerate(self.processes):
                logger.logger.debug('Checking Module: '+str(i))
                if not process.is_alive():
                    logger.logger.error('Module death detected: '+str(process.pid)+', starting it')
                    self.start_modules(self.modules[i])
            
    def terminate(self):
        for process in self.processes:
            logger.logger.info('Sending process SIGTERM signal: '+str(process))
            process.terminate()
        for process in self.processes:
            logger.logger.info('Waiting process '+str(process)+' end...')
            process.join()
            logger.logger.info('OK')
        logger.logger.info('Exiting')


