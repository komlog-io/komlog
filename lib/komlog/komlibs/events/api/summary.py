'''

Methods for generating Event Summaries

'''

import uuid, json
from komlog.komfig import logging
from komlog.komcass.api import events as cassapievents
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komlibs.events import exceptions
from komlog.komlibs.events.errors import Errors
from komlog.komlibs.events.model import types
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.widget import types as widget_types
from komlog.komlibs.numeric import aggregate

def get_user_event_data_summary(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_EAS_GUEDS_IUID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_EAS_GUEDS_IDATE)
    summary=cassapievents.get_user_event_data_summary(uid=uid, date=date)
    return summary.summary if summary else None

def generate_user_event_data_summary(event_type, parameters):
    try:
        return _generate_user_event_data_summary_funcs[event_type](parameters)
    except (KeyError,TypeError):
        return None

def _generate_data_summary_UENNSS(parameters):
    if not 'nid' in parameters:
        raise exceptions.BadParametersException(error=Errors.E_EAS_GDSUENNSS_NPNF)
    if args.is_valid_uuid(parameters['nid']):
        nid=parameters['nid']
    elif args.is_valid_hex_uuid(parameters['nid']):
        nid=uuid.UUID(parameters['nid'])
    else:
        raise exceptions.BadParametersException(error=Errors.E_EAS_GDSUENNSS_INID)
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.SummaryCreationException(error=Errors.E_EAS_GDSUENNSS_NIDNF)
    if snapshot.type == widget_types.DATASOURCE:
        ds_data=cassapidatasource.get_datasource_data(did=snapshot.did, fromdate=snapshot.interval_init, todate=snapshot.interval_end, count=1)
        if len(ds_data)==1:
            summary={
                'type':widget_types.DATASOURCE,\
                'ts':timeuuid.get_unix_timestamp(ds_data[0].date),\
                'widgetname':snapshot.widgetname,\
                'datasource':{'content':ds_data[0].content}\
            }
            return summary
        else:
            return None
    elif snapshot.type == widget_types.DATAPOINT:
        its=timeuuid.get_unix_timestamp(snapshot.interval_init)
        ets=timeuuid.get_unix_timestamp(snapshot.interval_end)
        dp_data=cassapidatapoint.get_datapoint_data(pid=snapshot.pid, fromdate=snapshot.interval_init, todate=snapshot.interval_end)
        summary={
            'type':widget_types.DATAPOINT,\
            'its':its,\
            'ets':ets,\
            'widgetname':snapshot.widgetname,\
            'datapoints':[]
        }
        if len(dp_data)>1:
            aggregated_data=aggregate.aggregate_timeseries_data(data=[[timeuuid.get_unix_timestamp(d['date']),float(d['value'])] for d in dp_data], bins=50, interval=[its,ets])
            summary['datapoints'].append({\
                'color':snapshot.datapoint_config.color,\
                'data':aggregated_data\
            })
            return summary
        else:
            return None
    elif snapshot.type == widget_types.MULTIDP:
        its=timeuuid.get_unix_timestamp(snapshot.interval_init)
        ets=timeuuid.get_unix_timestamp(snapshot.interval_end)
        summary={
            'type':widget_types.MULTIDP,\
            'its':its,\
            'ets':ets,\
            'widgetname':snapshot.widgetname,\
            'datapoints':[]\
        }
        dp_with_data=0
        for datapoint in snapshot.datapoints_config:
            dp_data=cassapidatapoint.get_datapoint_data(pid=datapoint.pid, fromdate=snapshot.interval_init, todate=snapshot.interval_end)
            dp_with_data+=1 if len(dp_data)>1 else 0
            aggregated_data=aggregate.aggregate_timeseries_data(data=[[timeuuid.get_unix_timestamp(d['date']),float(d['value'])] for d in dp_data], bins=50, interval=[its,ets])
            summary['datapoints'].append({\
                'color':datapoint.color,\
                'datapointname':datapoint.datapointname,\
                'data':aggregated_data\
            })
        if dp_with_data>0:
            return summary
        else:
            return None
    else:
        return None

def _generate_data_summary_UEIDPI(parameters):
    if not 'did' in parameters or not args.is_valid_uuid(parameters['did']):
        raise exceptions.BadParametersException(error=Errors.E_EAS_GDSUEIDPI_IDID)
    if not (
        'dates' in parameters
        and isinstance(parameters['dates'],list)
        and len(parameters['dates'])>0
        and all(args.is_valid_date(date) for date in parameters['dates'])):
        raise exceptions.BadParametersException(error=Errors.E_EAS_GDSUEIDPI_IDATES)
    summary={'data':[]}
    did=parameters['did']
    dates=set(parameters['dates'])
    for date in dates:
        ds_data = cassapidatasource.get_datasource_data_at(did=did, date=date)
        if ds_data == None or ds_data.content == None:
            raise exceptions.UserEventCreationException(error=Errors.E_EAS_GDSUEIDPI_DSDNF)
        variables = cassapidatasource.get_datasource_map_variables(did=did, date=date)
        if variables == None or len(variables.keys()) == 0:
            raise exceptions.UserEventCreationException(error=Errors.E_EAS_GDSUEIDPI_DSVNF)
        ts = timeuuid.get_unix_timestamp(date)
        seq = timeuuid.get_custom_sequence(date)
        summary['data'].append({'vars':list(variables.items()), 'content':ds_data.content, 'ts':ts, 'seq':seq})
    return summary

_generate_user_event_data_summary_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_generate_data_summary_UENNSS,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_generate_data_summary_UEIDPI,
}

