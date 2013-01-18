from komdb import connection as dbcon
import sections, options, services
from komapp import modules
import time
from twisted.internet import reactor
from twisted.web import server
import sys



class Soapserver(modules.Module):
    def __init__(self, config):
        super(Soapserver,self).__init__(config, 'SOAPServer')
        self.sql_uri = self.config.safe_get(sections.SOAPSERVER, options.SQL_URI)
        self.listen_port = self.config.safe_get(sections.SOAPSERVER, options.LISTEN_PORT)
        self.listen_addr = self.config.safe_get(sections.SOAPSERVER, options.LISTEN_ADDR)
        self.data_dir = self.config.safe_get(sections.SOAPSERVER, options.DATA_DIR)
        
    def start(self):
        self.logger.info('SOAPServer module started')
        if not self.sql_uri:
            self.logger.error('Key '+options.SQL_URI+' not found, stablishing default: localhost')
            self.sql_uri='localhost'
        if not self.listen_addr:
            self.logger.error('Key '+options.LISTEN_ADDR+' not found, stablishing default: *')
            self.listen_addr=''
        if not self.listen_port:
            self.logger.error('Key '+options.LISTEN_PORT+' not found, stablishing default: 8000')
            self.listen_port=8000
        if not self.data_dir:
            self.logger.critical('Key '+options.DATA_DIR+' not found, exiting')
            sys.exit()
        self.sql_connection = dbcon.Connection(self.sql_uri)
        self.__loop()
        self.logger.info('SOAPServer module exiting')
    
    def __loop(self):
        while True:
            self.logger.info('Starting web server')
            reactor.listenTCP(int(self.listen_port),server.Site(services.Services(self.sql_connection, self.data_dir)),interface=self.listen_addr)
            reactor.run()
            self.logger.critical('Detected web server failure, restarting in 3 seconds')
            time.sleep(3)