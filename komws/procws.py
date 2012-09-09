from komws import exceptions as wsex
from komdb import api as dbapi
from komdb import exceptions as dbex
from komfs import api as fsapi


def process(data, context):
    """
    The purpose of these functions is to process the service call
    """
    print "Proc Dispatch"
    globals()[context.lower()](data)

def wsupload_sample(data):
    """
    data:
            - username
            - password
            - agentid
            - datasourceid
            - date
            - filecontent
    We need to:
            - Register this sample on db
            - Copy the sample (filecontent) to the destfile
    """
    print "DATOS RECIBIDOS"
    print data
    try:
        sid = dbapi.create_sample(data.datasourceid, data.date)
        if sid > 0:
            fsapi.create_sample(sid, data.filecontent)
        else:
            raise wsex.ProcessingError()
    except:
        raise wsex.ProcessingError()
    else:
        return True


