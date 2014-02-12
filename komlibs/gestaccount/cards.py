#coding: utf-8
''' 
This file implements some CARD operations

@author: jcazor
@date: 2014/02/03

'''
import operator
from komcass import api as cassapi

def calculate_card_priority(dscard):
    '''
    En un primer momento la prioridad la calculamos de la siguiente manera:
     - prioridad=(prioridad_anterior+(60*num_anomalias+10*num_graficos+5*num_datapoints))/2
    '''
    if dscard.priority:
        last_prio=int(dscard.priority,16)
    else:
        last_prio=0
    num_anomalies=len(dscard.get_anomalies())
    num_graphs=len(dscard.get_graphs())
    num_datapoints=len(dscard.get_datapoints())
    part_prio=60*num_anomalies+10*num_graphs+5*num_datapoints
    priority=(last_prio+part_prio)/2
    if priority>255:
        priority=255
    hex_prio=hex(255-priority).split('x')[1]
    if len(hex_prio)==1:
        hex_prio='0'+hex_prio
    return hex_prio.upper()

def get_homecards(session, msgbus, uid=None, aid=None):
    data=[]
    if aid:
        dscards=cassapi.get_agentdscard(aid,session,count=6)
    elif uid:
        dscards=cassapi.get_userdscard(uid,session,count=6)
    else:
        return data
    if not dscards:
        return data
    cards=dscards.get_cards()
    sorted_cards=sorted(cards.iteritems(),key=operator.itemgetter(1))
    for card in sorted_cards:
        dscard=cassapi.get_datasourcecard(card[0],session)
        if not dscard:
            continue
        else:
            cardinfo={}
            cardinfo['title']=dscard.ds_name
            cardinfo['did']=dscard.did
            cardinfo['subtitle']=dscard.ag_name
            cardinfo['aid']=dscard.aid
            cardinfo['date']=dscard.ds_date
            cardinfo['imgs']=dscard.get_graphs()
            cardinfo['table']=dscard.get_datapoints()
            cardinfo['news']=dscard.get_anomalies()
            data.append(cardinfo)
    return data



