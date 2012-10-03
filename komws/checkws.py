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
    needed_keys = ['username','password','agentid','datasourceid','date','filecontent']
    try:
        if len(data)==len(needed_keys):
            for key in needed_keys:
                if hasattr(data,key):
                    continue
                else:
                    raise wsex.InvalidData()
        else:
            raise wsex.InvalidData()
    except:
        raise wsex.InvalidData()
    else:
        return True

def wsdownload_config(data):
    """
    data:
            - username
            - password
            - agentid
    """
    needed_keys = ['username','password','agentid']
    try:
        if len(data)==len(needed_keys):
            for key in needed_keys:
                if hasattr(data,key):
                    continue
                else:
                    raise wsex.InvalidData()
        else:
            raise wsex.InvalidData()
    except:
        raise wsex.InvalidData()
    else:
        return True

