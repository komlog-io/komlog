from komcass import api as cassapi
import exceptions as wsex
import crypt
#from komdb import api
#from komdb import exceptions as dbex
#import exceptions as wsex

def authenticate(data, context, extra_vars):
    """
    The purpose of these functions is to authenticate the client who queries the web service
    """
    globals()[context.lower()](data, extra_vars)

def wsupload_sample(data, extra_vars):
    """
    data:
            - username
            - password
            - agentid
            - datasourceid
            - date
            - filecontent
    We need to:
        - authenticate user
        - authenticate agent
        - confirm datasource belonging
    """
    '''
    sql_session=extra_vars['sql_session']
    try:
        user = api.User(username=data.username, session=sql_session)
        if user.validate(data.password):
            agents = user.getAgents(sql_session)
            for agent in agents:
                if agent.validate(data.agentid):
                    datasources = agent.getDatasources(sql_session)
                    for ds in datasources:
                        if int(ds.did) == int(data.datasourceid):
                            return True
    except Exception, e:
        raise wsex.AuthenticationError
    else:
        raise wsex.AuthenticationError
    '''
    cf=extra_vars['cf']
    try:
        useruidr=cassapi.get_useruidrelation(data.username,cf)
        if useruidr:
            userinfo=cassapi.get_userinfo(useruidr.uid,{},cf)
            if userinfo:
                http_passwd=data.password
                db_hpasswd=userinfo.password
                salt=db_hpasswd[:8]
                if crypt.crypt(http_passwd,salt) == db_hpasswd:
                    useragentr=cassapi.get_useragentrelation(userinfo.uid,cf)
                    if useragentr:
                        for aid in useragentr.aids:
                            agentinfo=cassapi.get_agentinfo(aid,{},cf)
                            if agentinfo:
                                http_agentkey=data.agentid
                                db_agentkey=agentinfo.agentkey
                                if http_agentkey == db_agentkey:
                                    agentdsr=cassapi.get_agentdsrelation(agentinfo.aid,cf)
                                    if agentdsr:
                                        for did in agentdsr.dids:
                                            if str(did) == data.datasourceid:
                                                print 'Auth: Validated'
                                                return True
    except Exception as e:
        print str(e)
        raise wsex.AuthenticationError
    else:
        print 'Auth: Not Validated'
        raise wsex.AuthenticationError

def wsdownload_config(data, extra_vars):
    """
    data:
            - username
            - password
            - agentid
    We need to:
        - authenticate user
        - authenticate agent
    """
    '''
    sql_session=extra_vars['sql_session']
    try:
        user = api.User(username=data.username,session=sql_session)
        if user.validate(data.password):
            agents = user.getAgents(sql_session)
            for agent in agents:
                if agent.validate(data.agentid):
                    return True
            If we get here, means agent not found. To make it simple, we create it.
            aid = api.create_agent(data.username, 'Agent '+data.agentid, data.agentid, sql_session)
            if aid>0:
                return True
            else:
                raise wsex.AuthenticationError
                
    except:
        raise wsex.AuthenticationError
    else:
        raise wsex.AuthenticationError
    '''
    cf=extra_vars['cf']
    print 'Auth: Init'
    try:
        useruidr=cassapi.get_useruidrelation(data.username,cf)
        if useruidr:
            userinfo=cassapi.get_userinfo(useruidr.uid,{},cf)
            if userinfo:
                http_passwd=data.password
                db_hpasswd=userinfo.password
                salt=db_hpasswd[:8]
                print crypt.crypt(http_passwd,salt)
                print db_hpasswd
                if crypt.crypt(http_passwd,salt) == db_hpasswd:
                    useragentr=cassapi.get_useragentrelation(userinfo.uid,cf)
                    if useragentr:
                        for aid in useragentr.aids:
                            agentinfo=cassapi.get_agentinfo(aid,{},cf)
                            if agentinfo:
                                http_agentkey=data.agentid
                                db_agentkey=agentinfo.agentkey
                                if http_agentkey == db_agentkey:
                                    print 'Auth: Validated'
                                    return True
    except Exception as e:
        print str(e)
        raise wsex.AuthenticationError
    else:
        print 'auth: Not Validated'
        raise wsex.AuthenticationError


