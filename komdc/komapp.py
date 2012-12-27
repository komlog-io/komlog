'''
Created on 26/12/2012

@author: jcazor
'''
import os
from komfig import config, komlogger
import options, sections, modules, time
from multiprocessing import Process



class Komapp(object):
    def __init__(self,conf_file):
        self.path, self.conf_file = os.path.split(conf_file)
        self.config = None
        self.modules = []
        self.processes = []
        
    def start(self):
        self.__load_conf_file()
        self.logger = komlogger.getLogger(self.config.conf_file, __name__)
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
                    self.config = config.Config(self.path, self.conf_file)
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
        for module in self.config.safe_get(sections.MAIN,options.MODULES):
            mod_section='module_'+module
            if str(self.config.safe_get(mod_section, options.MODULE_ENABLED)).lower() == 'yes':
                modobj = getattr(modules,module[0].upper()+module[1:])(self.config)
                modules_enabled.append(modobj)
        self.modules = modules_enabled
        
    def __start_modules(self, module=None):
        if not module:
            for i,module in enumerate(self.modules):
                p = Process(target=module.start,name=module.__class__.__name__)
                self.logger.info('Starting module: '+str(p))
                p.start()
                self.processes.insert(i,p)
        else:
            i = self.modules.index(module)
            if not self.processes[i].is_alive():
                p = Process(target=module.start,name=module.__class__.__name__)
                p.start()
                self.logger.info('Starting module: '+str(p))
                self.processes.pop(i)
                self.processes.insert(i,p)
            else:
                self.logger.error('Trying to start an already running module')
            
    def __loop(self):
        while True:
            time.sleep(10)
            for i, process in enumerate(self.processes):
                self.logger.debug('Checking Module: '+str(i))
                if not process.is_alive():
                    self.logger.error('Module death detected: '+str(process.pid)+', starting it')
                    self.__start_modules(self.modules[i])
            