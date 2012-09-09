from komws import exceptions as wsex

def check(data, context):
    """
    The purpose of these functions is to check whether the received data contains the
    necessary fields for each service
    """
    print "Check Dispatch"
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
    """
    print "Inicio wsupload_sample()"
    needed_keys = ['username','password','agentid','datasourceid','date','filecontent']
    try:
        print "Inicio try"
        print "Numero de elementos recibidos: "+str(len(data))
        print "Numero de elementos necesarios: "+str(len(needed_keys))
        if len(data)==len(needed_keys):
            print "Numero de elementos correcto"
            for key in needed_keys:
                if hasattr(data,key):
                    continue
                else:
                    print "No existe el elemento "+str(key)
                    raise wsex.InvalidData()
        else:
            print "Numero de elementos incorrecto: "+str(len(data))
            raise wsex.InvalidData()
    except:
        print "  Error en los datos recibidos"
        raise wsex.InvalidData()
    else:
        print "  Datos OK"
        return True

