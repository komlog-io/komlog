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
        print "Recibida peticion al servicio wsUploadSample"
        context='wsupload_sample'
        try:
            print "Inicio check"
            checkws.check(data, context)
        except exceptions.InvalidData:
            print "Excepcion en check"
            return codes.INVALID_DATA_ERROR

        try:
            print "Inicio auth"
            authws.authenticate(data, context)
        except exceptions.AuthenticationError:
            print "Excepcion en auth"
            return codes.AUTHENTICATION_ERROR

        try:
            print "Inicio proc"
            procws.process(data, context)
        except exceptions.ProcessingError:
            print "Excepcion en proc"
            return codes.SERVICE_ERROR
        else:
            print "Service OK"
            return(codes.SERVICE_OK)
        return codes.SERVICE_ERROR

if __name__ == '__main__':
    from twisted.internet import reactor
    reactor.listenTCP(8008,server.Site(Services()))
    reactor.run()
