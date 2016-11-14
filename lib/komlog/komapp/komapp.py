'''
Created on 31/12/2012

@author: jcazor
'''
import os
import signal
import time
import importlib
import traceback
import subprocess
from komlog.komfig import config, logging, options


class Komapp(object):
    def __init__(self, exec_file, conf_file, module, instance):
        self.exec_file = exec_file
        self.conf_file = conf_file
        self.module = module
        self.instance = instance
        if module is None and instance is None:
            self._process_name = 'komlog'
        else:
            self._process_name = '-'.join((module,instance))

    def signal_handler(self, signum, frame):
        if signum == signal.SIGTERM:
            logging.logger.info('SIGTERM received, terminating')
            self.shutdown()
        else:
            logging.logger.info('signal '+str(signum)+' received, ignoring')

    def start(self):
        signal.signal(signal.SIGTERM,self.signal_handler)
        signal.signal(signal.SIGINT,self.signal_handler)
        self.load_conf_file()
        if logging.initialize_logging(self._process_name):
            logging.logger.info('Configuration file loaded successfully')
        if self.module != None and self.instance != None:
            self.start_module()
        elif self.module is None and self.instance is None:
            self.spawn_modules()
        else:
            logging.logger.error('Invalid parameters.')
            logging.logger.error('Pass module and instance parameters or none of them')
            exit(-1)

    def load_conf_file(self):
        path, filename = os.path.split(self.conf_file)
        if os.path.exists(path):
            if os.path.isdir(path):
                if os.path.isfile(self.conf_file):
                    if not config.initialize_config(self.conf_file):
                        exit(-1)
                else:
                    print('Not a file: '+self.conf_file)
                    exit(-1)
            else:
                print('Not a directory: '+self.path)
                exit(-1)
        else:
            print('Directory not found: '+self.path)
            exit(-1)

    def start_module(self):
        module_name = '.'.join(('komlog.komapp.modules',self.module))
        try:
            m = importlib.import_module(module_name)
        except:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            raise
        self._mod_obj = m.get_module(instance=int(self.instance))
        self._mod_obj.start()

    def spawn_modules(self):
        modules = []
        for module in config.get(options.MODULES).split(','):
            if str(config.get(options.MODULE_ENABLED, module)).lower() == 'yes':
                instances = config.get(options.MODULE_INSTANCES, module)
                if not instances:
                    modules.append((module,'0'))
                else:
                    instances = int(instances)
                    for i in range(0,instances):
                        modules.append((module,str(i)))
        procs = []
        for module in modules:
            args=[self.exec_file,'-c',self.conf_file,'-m',module[0],'-i',module[1]]
            proc = subprocess.Popen(args, start_new_session=True)
            procs.append(proc)
        if len(procs)>0:
            self.run = True
        while self.run:
            time.sleep(5)
            for i,proc in enumerate(procs):
                logging.logger.debug('Checking proc: '+str(proc.args))
                if proc.poll() != None:
                    logging.logger.error('Module death detected: '+str(proc.args))
                    if not str(config.get(options.RESTART_MODULES)).lower() == 'no':
                        logging.logger.error('Starting module: '+str(proc.args))
                        proc = subprocess.Popen(proc.args)
                        procs.pop(i)
                        procs.append(proc)
                    else:
                        procs.pop(i)
                        if len(procs)==0:
                            self.run=False
        for proc in procs:
            logging.logger.error('Sending Termination signal to process: '+str(proc.args))
            proc.send_signal(signal.SIGTERM)
        for proc in procs:
            try:
                logging.logger.info('Waiting process termination: '+str(proc.args))
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                logging.logger.error('Timeout expired waiting for process termination: '+str(proc.args)+' Killing it.')
                proc.kill()
        logging.logger.info('Exiting Komlog, bye bye.')

    def shutdown(self):
        if self.module:
            self._mod_obj.stop()
        else:
            self.run=False

