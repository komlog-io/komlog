'''
Created on 31/12/2012

@author: jcazor
'''
import os
from komfig import config, logger
import options, sections, modules, time
from multiprocessing import Process



class Komapp(object):
    def __init__(self,conf_file):
        self.path, self.conf_file = os.path.split(conf_file)
        self.modules = []
        self.processes = []
        
    def start(self):
        self.__load_conf_file()
        if logger.initialize_logger(__name__):
            logger.logger.info('Configuration file loaded successfully')
        self.__load_modules()
        self.__start_modules()
        self.__loop()

    def __load_conf_file(self):
        """
        Load conf_file
        """
        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                if os.path.isfile(os.path.join(self.path, self.conf_file)):
                    if not config.initialize_config(os.path.join(self.path, self.conf_file)):
                        exit()
                else:
                    print "Not a file: "+os.path.join(self.path, self.conf_file)
                    exit()
            else:
                print "Not a directory: "+self.path
                exit()
        else:
            print "Directory not found: "+self.path
            exit()
       
    def __load_modules(self):
        modules_enabled = []
        for module in config.config.safe_get(sections.MAIN,options.MODULES).split(','):
            mod_section='module_'+module
            if str(config.config.safe_get(mod_section, options.MODULE_ENABLED)).lower() == 'yes':
                instances = config.config.safe_get(mod_section, options.MODULE_INSTANCES)
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
        
    def __start_modules(self, module=None):
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
            
    def __loop(self):
        while True:
            time.sleep(10)
            for i, process in enumerate(self.processes):
                logger.logger.debug('Checking Module: '+str(i))
                if not process.is_alive():
                    logger.logger.error('Module death detected: '+str(process.pid)+', starting it')
                    self.__start_modules(self.modules[i])
            
