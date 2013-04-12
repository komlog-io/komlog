import exceptions as wsex

def check(data, context):
    """
    The purpose of these functions is to check whether the received data contains the
    necessary fields for each service
    """
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
            - encoding
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
    except Exception as e:
        print str(e)
        raise wsex.InvalidData()
    else:
        print 'Check: OK'
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
        print 'Check: OK'
        return True

