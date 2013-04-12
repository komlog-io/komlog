import exceptions as wsex
#from komdb import api as dbapi
#from komdb import exceptions as dbex
from komcass import api as cassapi
from komfs import api as fsapi
import os



def process(data, context, extra_vars):
    """
    The purpose of these functions is to process the service call
    """
    return globals()[context.lower()](data, extra_vars)
    
def wsupload_sample(data, extra_vars):
    """
    data:
            - username
            - password
            - agentid
            - datasourceid
            - date (date string in iso format)
            - filecontent
    We need to:
            - Copy the sample (filecontent) to the destfile
    """
    try:
        name = data.date+'_'+str(data.datasourceid)+'.pspl'
        dir = extra_vars['dir']
        dest_file = os.path.join(dir,name) 
        fsapi.create_sample(dest_file, data.filecontent)
    except Exception as e:
        print str(e)
        raise wsex.ProcessingError()
    else:
        print 'Proc: OK'
        return True

def wsdownload_config(data, extra_vars):
    """
    data:
            - username
            - password
            - agentid
    We need to:
            - For each agent's datasource get its configuration
            - return all configuration to the agent            
    """
    '''
    try:
        user = dbapi.User(username=data.username, session=sql_session)
        for agent in user.getAgents(sql_session):
            if agent.validate(data.agentid):
                datasources = agent.getDatasources(sql_session)
                for datasource in datasources:
                    ds_config = datasource.getConfig(sql_session)
                    configuration.append(ds_config)
    except Exception as e:
        raise wsex.ProcessingError()
    else:
        return configuration
    '''
    configuration = []
    cf=extra_vars['cf']
    try:
        useruidr=cassapi.get_useruidrelation(data.username,cf)
        useragentr=cassapi.get_useragentrelation(useruidr.uid,cf)
        for aid in useragentr.aids:
            agentinfo=cassapi.get_agentinfo(aid,{},cf)
            if agentinfo.agentkey==data.agentid:
                agentdsr=cassapi.get_agentdsrelation(agentinfo.aid,cf)
                for did in agentdsr.dids:
                    dsinfo=cassapi.get_dsinfo(did,{},cf)
                    configuration.append({'command':dsinfo.script_name,'dow':dsinfo.day_of_week,'mon':dsinfo.month,'dom':dsinfo.day_of_month,\
                                          'hour':dsinfo.hour,'min':dsinfo.minute,'did':str(dsinfo.did)})
                    print 'Configuration added'
    except Exception as e:
        print str(e)
        raise wsex.ProcessingError()
    else:
        return configuration
      


