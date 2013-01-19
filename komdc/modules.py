import sections, options
import os
import glob
import time
import dateutil.parser
from komdb import api as dbapi
from komdb import connection as dbcon
from komcass import api as cassapi
from komcass import connection as casscon
from komfig import komlogger
from komfs import api as fsapi
from komapp import modules
        
class Validation(modules.Module):
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

class Storing(modules.Module):
    def __init__(self, config):
        super(Storing,self).__init__(config, 'Storing')
        self.cass_keyspace = self.config.safe_get(sections.STORING,options.CASS_KEYSPACE)
        self.cass_servlist = self.config.safe_get(sections.STORING,options.CASS_SERVLIST).split(',')
        try:
            self.cass_poolsize = int(self.config.safe_get(sections.STORING,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.cass_poolsize = 5
        self.sql_uri = self.config.safe_get(sections.STORING, options.SQL_URI)
        self.watchdir = self.config.safe_get(sections.STORING, options.SAMPLES_INPUT_PATH)
        self.outputdir = self.config.safe_get(sections.STORING, options.SAMPLES_OUTPUT_PATH)
 
    def start(self):
        print 'Storing module started'
        self.logger.info('Storing module started')
        if not self.cass_keyspace or not self.cass_poolsize or not self.cass_servlist:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.watchdir:
            self.logger.error('Key '+options.SAMPLES_INPUT_PATH+' not found')
        elif not self.outputdir:
            self.logger.error('Key '+options.SAMPLES_OUTPUT_PATH+' not found')
        elif not self.sql_uri:
            self.logger.error('Key '+options.SQL_URI+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.cass_keyspace, server_list=self.cass_servlist, pool_size=self.cass_poolsize)
            self.samples_cf = casscon.SamplesCF(self.cass_pool.connection_pool)
            self.sql_connection = dbcon.Connection(self.sql_uri)
            self.__loop()
        self.logger.info('Storing module exiting')
    
    def __loop(self):
        while True:
            files = filter(os.path.isfile,glob.glob(os.path.join(self.watchdir,'*vspl')))
            files.sort(key=lambda x: os.path.getmtime(x))
            if len(files)>0:
                for f in files:
                    try:
                        os.rename(f,f[:-5]+'.wspl')
                    except OSError:
                        #other instance took it firts
                        self.logger.error('File already treated by other module instance: '+f)
                    else:
                        print 'Storing file: '+f
                        fi = f[:-5]+'.wspl'
                        if self.store(fi):
                            print 'File Stored successfully: '+f
                            os.rename(fi,os.path.join(self.outputdir,os.path.basename(fi)[:-5]+'.sspl'))
                        else:
                            os.rename(fi,fi[:-5]+'.vspl')
                                                
            else:
                time.sleep(5)
    
    def store(self, filename):
        self.logger.debug('Storing '+filename)
        datasourceid = filename.split('_')[1].split('.')[0]
        date = dateutil.parser.parse(os.path.basename(filename).split('_')[0])
        udata = fsapi.get_file_content(filename)
        print 'Get the file content before storing'
        # Register the sample
        try:
            sid = 0
            sid = dbapi.create_sample(datasourceid, date, self.sql_connection.session)
            print 'Sample created on pgsql: '+str(sid)
            if sid > 0:
                cassapi.create_sample(sid, udata, self.samples_cf)
                print 'Stored successfully on cassandra'
                self.logger.debug(filename+' stored successfully with sid: '+str(sid))
                return True
            else:
                print 'Error, sid<0'
                self.logger.error('Storing '+filename)
                return False
        except Exception as e:
            #rollback
            print 'Exception Storing: '+str(e)
            self.logger.exception('Exception storing sample '+filename+': '+str(e))
            try:
                if sid > 0:
                    dbapi.delete_sample(sid, self.sql_connection.session)
                cassapi.remove_sample(sid, self.samples_cf)
            except Exception as e:
                self.logger.exception('Exception in Rollback storing sample '+filename+': '+str(e))
                return False
            else:
                return False
        