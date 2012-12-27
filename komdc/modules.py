import sections, options
import os
import glob
import time
import dateutil.parser
from komdb import api as dbapi
from komcass import api as cassapi
from komcass import connection as casscon

class __Module(object):
    def __init__(self, config):
        self.config = config
    
class Validation(__Module):
    def __init__(self, config):
        super(Validation,self).__init__(config)
        self.watchdir = self.config.safe_get(sections.VALIDATION, options.SAMPLES_INPUT_PATH)
        self.outputdir = self.config.safe_get(sections.VALIDATION, options.SAMPLES_OUTPUT_PATH)
            
    def start(self):
        print "Module started"
        if not self.watchdir:
            print 'Error: key '+options.SAMPLES_INPUT_PATH+' not found'
        elif not self.outputdir:
            print 'Error: key '+options.SAMPLES_OUTPUT_PATH+' not found'
        else:
            self.__loop()
        
    def __loop(self):
        while True:
            files = filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*pspl')))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    if self.validate(f):
                        os.rename(os.path.join(self.watchdir,f),os.path.join(self.outputdir,f[:-5]+'.vspl'))                    
            else:
                time.sleep(5)
    
    def validate(self, filename):
        return True

class Storing(__Module):
    def __init__(self, config):
        super(Storing,self).__init__(config)
        self.cass_keyspace = self.config.safe_get(sections.STORING,options.CASS_KEYSPACE)
        self.cass_servlist = self.config.safe_get(sections.STORING,options.CASS_SERVLIST)
        self.cass_poolsize = self.config.safe_get(sections.STORING,options.CASS_POOLSIZE)
        self.watchdir = self.config.safe_get(sections.STORING, options.SAMPLES_INPUT_PATH)
        self.outputdir = self.config.safe_get(sections.STORING, options.SAMPLES_OUTPUT_PATH)
 
    def start(self):
        print "Storing module started"
        if not self.cass_keyspace or not self.cass_poolsize or not self.cass_servlist:
            print 'Error: Cassandra connection configuration keys not found'
        elif not self.watchdir:
            print 'Error: key '+options.SAMPLES_INPUT_PATH+' not found'
        else:
            self.cass_pool = casscon.Pool(keyspace=self.cass_keyspace, server_list=self.cass_servlist, pool_size=self.cass_poolsize)
            self.samples_cf = casscon.SamplesCF(self.cass_pool)
            self.__loop()
        print "Storing module exiting"
    
    def __loop(self):
        while True:
            files = filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*vspl')))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    if self.store(f):
                        os.rename(os.path.join(self.watchdir,f),os.path.join(self.outputdir,f[:-5]+'.sspl'))                    
            else:
                time.sleep(5)
    
    def store(self, filename):
        print "Storing: "+filename
        datasourceid = filename.split('_')[1].split('.')[0]
        date = dateutil.parser.parse(os.path.basename(filename).split('_')[0])
        data = open(filename).read()
        # Register the sample
        sid = dbapi.create_sample(datasourceid, date)
        if sid > 0:
            sample = cassapi.Sample(str(sid), self.samples_cf, content=data)
            #column_family.insert(sample)
            sample.insert(self.samples_cf)
            return True
        else:
            return False
