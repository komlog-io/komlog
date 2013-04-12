from komdb import connection as dbcon
import sections, options, services
from komapp import modules
from komcass import api as cassapi
from komcass import connection as casscon
from komfig import komlogger
import time
from twisted.internet import reactor
from twisted.web import server
import sys



class Soapserver(modules.Module):
    def __init__(self, config, instance_number):
        super(Soapserver,self).__init__(config, 'SOAPServer', instance_number)
        self.params={}
        #self.sql_uri = self.config.safe_get(sections.SOAPSERVER, options.SQL_URI)
        self.params['cass_keyspace'] = self.config.safe_get(sections.SOAPSERVER,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.SOAPSERVER,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.SOAPSERVER,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        
        self.listen_port = self.config.safe_get(sections.SOAPSERVER, options.LISTEN_PORT)
        self.listen_addr = self.config.safe_get(sections.SOAPSERVER, options.LISTEN_ADDR)
        self.data_dir = self.config.safe_get(sections.SOAPSERVER, options.DATA_DIR)
        
    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('SOAPServer module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
            sys.exit()
        if not self.listen_addr:
            self.logger.error('Key '+options.LISTEN_ADDR+' not found, stablishing default: *')
            self.listen_addr=''
        if not self.listen_port:
            self.logger.error('Key '+options.LISTEN_PORT+' not found, stablishing default: 8000')
            self.listen_port=8000
        if not self.data_dir:
            self.logger.critical('Key '+options.DATA_DIR+' not found, exiting')
            sys.exit()
        self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
        self.cass_cf = casscon.CF(self.cass_pool)
        self.__loop()
        self.logger.info('SOAPServer module exiting')
    
    def __loop(self):
        while True:
            self.logger.info('Starting web server')
            reactor.listenTCP(int(self.listen_port),server.Site(services.Services(self.cass_cf, self.data_dir, self.logger)),interface=self.listen_addr)
            reactor.run()
            self.logger.critical('Detected web server failure, restarting in 3 seconds')
            time.sleep(3)
