import sections, options
import os
import glob
import time
import dateutil.parser
from komdb import api as dbapi
from komcass import api as cassapi
from komcass import connection as casscon
from komfig import komlogger
from komfs import api as fsapi

class __Module(object):
    def __init__(self, config, name):
        self.config = config
        self.logger = komlogger.getLogger(config.conf_file, name)
        
class Validation(__Module):
    def __init__(self, config):
        super(Validation,self).__init__(config, self.__class__.__name__)
        self.watchdir = self.config.safe_get(sections.VALIDATION, options.SAMPLES_INPUT_PATH)
        print self.watchdir
        self.outputdir = self.config.safe_get(sections.VALIDATION, options.SAMPLES_OUTPUT_PATH)
        print self.outputdir
            
    def start(self):
        self.logger.info('Module started')
        if not self.watchdir:
            self.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.outputdir:
            self.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        else:
            self.__loop()
        
    def __loop(self):
        while True:
            files = filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*pspl')))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    if self.validate(f):
                        os.rename(f,os.path.join(self.outputdir,os.path.basename(f)[:-5]+'.vspl'))                    
            else:
                time.sleep(5)
    
    def validate(self, filename):
        self.logger.debug('Validating '+filename)
        return True

class Storing(__Module):
    def __init__(self, config):
        super(Storing,self).__init__(config, self.__class__.__name__)
        self.cass_keyspace = self.config.safe_get(sections.STORING,options.CASS_KEYSPACE)
        self.cass_servlist = self.config.safe_get(sections.STORING,options.CASS_SERVLIST).split(',')
        print self.cass_servlist
        try:
            self.cass_poolsize = int(self.config.safe_get(sections.STORING,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.cass_poolsize = 5
        self.watchdir = self.config.safe_get(sections.STORING, options.SAMPLES_INPUT_PATH)
        self.outputdir = self.config.safe_get(sections.STORING, options.SAMPLES_OUTPUT_PATH)
 
    def start(self):
        self.logger.info('Storing module started')
        if not self.cass_keyspace or not self.cass_poolsize or not self.cass_servlist:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.watchdir:
            self.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.outputdir:
            self.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.cass_keyspace, server_list=self.cass_servlist, pool_size=self.cass_poolsize)
            self.samples_cf = casscon.SamplesCF(self.cass_pool.connection_pool)
            self.__loop()
        self.logger.info('Storing module exiting')
    
    def __loop(self):
        while True:
            files = filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*vspl')))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    if self.store(f):
                        os.rename(f,os.path.join(self.outputdir,os.path.basename(f)[:-5]+'.sspl'))                    
            else:
                time.sleep(5)
    
    def store(self, filename):
        self.logger.debug('Storing '+filename)
        datasourceid = filename.split('_')[1].split('.')[0]
        date = dateutil.parser.parse(os.path.basename(filename).split('_')[0])
        udata = fsapi.get_file_content(filename)
        # Register the sample
        sid = dbapi.create_sample(datasourceid, date)
        if sid > 0:
            sample = cassapi.Sample(str(sid), self.samples_cf, content=udata)
            #column_family.insert(sample)
            sample.insert(self.samples_cf)
            self.logger.debug(filename+' stored successfully with sid: '+str(sid))
            return True
        else:
            self.logger.error('Storing '+filename)
            return False
