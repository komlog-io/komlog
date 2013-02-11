from twisted.web import soap
import checkws, authws, procws, codes, exceptions


class Services(soap.SOAPPublisher):
    def __init__(self, sql_connection, data_dir, logger):
        self.sql_connection = sql_connection
        self.data_dir = data_dir
        self.logger = logger
        
    """Here we publish our methods"""
    def soap_wsUploadSample(self,data):
        """data:
            - username
            - password
            - agentid
            - datasourceid
            - date
            - filecontent
        """
        
        context='wsupload_sample'
        self.logger.debug('Service called: '+context)
        self.logger.debug('Received data: '+str(data))
        extras = {'dir':self.data_dir,'sql_session':self.sql_connection.session}
        try:
            self.logger.debug('check')
            checkws.check(data, context)
        except exceptions.InvalidData:
            return codes.INVALID_DATA_ERROR

        try:
            print 'auth'
            authws.authenticate(data, context, extras)
        except exceptions.AuthenticationError:
            return codes.AUTHENTICATION_ERROR

        try:
            print 'proc'
            procws.process(data, context, extras)
        except exceptions.ProcessingError:
            return codes.SERVICE_ERROR
        else:
            return(codes.SERVICE_OK)
        return codes.SERVICE_ERROR
    
    def soap_wsDownloadConfig(self, data):
        """ Service to download agent configuration
            By now, configuration means datasource configuration
            this service return the necesary parameters to
            make the agent start getting data.
            data:
                - username
                - password
                - agentid
        """
        context='wsdownload_config'
        self.logger.debug('Service called: '+context)
        self.logger.debug('Received data: '+str(data))
        extras = {'sql_session':self.sql_connection.session}
        try:
            self.logger.debug('check called')
            checkws.check(data, context)
        except exceptions.InvalidData:
            return codes.INVALID_DATA_ERROR

        try:
            self.logger.debug('auth called')
            authws.authenticate(data, context, extras)
            self.logger.debug('auth finished')
        except exceptions.AuthenticationError:
            return codes.AUTHENTICATION_ERROR

        try:
            self.logger.debug('proc called')
            config = procws.process(data, context, extras)
            self.logger.debug('proc finished')
        except exceptions.ProcessingError:
            self.logger.debug('Service Response: SERVICE_ERROR (ProcessingError)')
            return codes.SERVICE_ERROR
        else:
            self.logger.debug('Service Response: '+str(config))
            return config
        self.logger.debug('Service Response: SERVICE_ERROR')
        return codes.SERVICE_ERROR
    