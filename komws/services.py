from twisted.web import soap
import checkws, authws, procws, codes, exceptions


class Services(soap.SOAPPublisher):
    def __init__(self, sql_connection, data_dir):
        self.sql_connection = sql_connection
        self.data_dir = data_dir
        
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
        try:
            checkws.check(data, context)
        except exceptions.InvalidData:
            return codes.INVALID_DATA_ERROR

        try:
            authws.authenticate(data, context, self.sql_connection.session)
        except exceptions.AuthenticationError:
            return codes.AUTHENTICATION_ERROR

        try:
            procws.process(data, context, self.data_dir, self.sql_connection.session)
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
        try:
            print 'check called'
            checkws.check(data, context)
        except exceptions.InvalidData:
            return codes.INVALID_DATA_ERROR

        try:
            print 'auth called'
            authws.authenticate(data, context, self.sql_connection.session)
        except exceptions.AuthenticationError:
            return codes.AUTHENTICATION_ERROR

        try:
            print 'proc called'
            config = procws.process(data, context, self.sql_connection.session)
        except exceptions.ProcessingError:
            return codes.SERVICE_ERROR
        else:
            return(config)
        return codes.SERVICE_ERROR
    