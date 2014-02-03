#coding: utf-8
''' 
This file implements some CARD operations

@author: jcazor
@date: 2014/02/03

'''

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
