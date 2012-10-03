from twisted.web import soap, server
from komws import checkws, authws, procws, codes, exceptions


class Services(soap.SOAPPublisher):
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
            authws.authenticate(data, context)
        except exceptions.AuthenticationError:
            return codes.AUTHENTICATION_ERROR

        try:
            procws.process(data, context)
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
            checkws.check(data, context)
        except exceptions.InvalidData:
            return codes.INVALID_DATA_ERROR

        try:
            authws.authenticate(data, context)
        except exceptions.AuthenticationError:
            return codes.AUTHENTICATION_ERROR

        try:
            config = procws.process(data, context)
        except exceptions.ProcessingError:
            return codes.SERVICE_ERROR
        else:
            return(config)
        return codes.SERVICE_ERROR        
            

if __name__ == '__main__':
    from twisted.internet import reactor
    reactor.listenTCP(8008,server.Site(Services()))
    reactor.run()
