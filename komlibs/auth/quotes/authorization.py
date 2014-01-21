#coding:utf-8

'''
This library implements authorization mechanisms based on user quotas


@author: jcazor
@date: 2013/12/08
'''

import deny
from komcass import api as cassapi


def authorize_new_agent(username,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    interfaces=deny.interfaces['User_AgentCreation']
    if not cassapi.get_userifacedeny(useruidr.uid,session,interfaces):
        return True
    return False

def authorize_get_agent_config(username,aid,session):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_ds_data(username,did,session):
    ''' Not quotes authorization needed '''
    return True

def authorize_post_ds_data(username,aid,did,session):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_ds_config(username,did,session):
    ''' Not quotes authorization needed '''
    print 'Yo salgo bien'
    return True

def authorize_put_ds_config(username,aid,did,session):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datasource(username,aid,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatasourceCreation'])
    interfaces.append(deny.interfaces['Agent_DatasourceCreation']+str(aid))
    if not cassapi.get_userifacedeny(useruidr.uid,session,interfaces):
        return True
    return False

def authorize_get_dp_data(username,pid,session):
    ''' Not quotes authorization needed '''
    return True

def authorize_get_dp_config(username,pid,session):
    ''' Not quotes authorization needed '''
    return True

def authorize_new_datapoint(username,did,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatapointCreation'])
    #aqui deberiamos añadir tb el agent_dtpcreation, pero obtener el aid seria lento...
    interfaces.append(deny.interfaces['Ds_DatapointCreation']+str(did))
    if not cassapi.get_userifacedeny(useruidr.uid,session,interfaces):
        return True
    return False

def authorize_new_graph(username,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    interfaces=[]
    interfaces.append(deny.interfaces['User_GraphCreation'])
    if not cassapi.get_userifacedeny(useruidr.uid,session,interfaces):
        return True
    return False

def authorize_get_graph_config(username,gid,session):
    ''' Not quotes authorization needed '''
    return True

