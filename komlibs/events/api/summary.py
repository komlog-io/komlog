'''

Methods for generating Event Summaries

'''

import uuid, json
from komfig import logger
from komcass.api import events as cassapievents
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import snapshot as cassapisnapshot
from komlibs.events import errors, exceptions
from komlibs.events.model import types
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.gestaccount.widget import types as widget_types
from komlibs.numeric import aggregate

def get_user_event_graph_summary_data(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAS_GUEGSD_IUID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAS_GUEGSD_IDATE)
    summary=cassapievents.get_user_event_graph_summary(uid=uid, date=date)
    return summary.summary if summary else None

def generate_user_event_graph_summary_data(event_type, parameters):
    try:
        return _generate_user_event_graph_summary_data_funcs[event_type](parameters)
    except Exception as e:
        logger.logger.debug('Exception generating summary: '+str(e))
        return None

def _generate_graph_summary_data_UENNSS(parameters):
    if not 'nid' in parameters:
        raise exceptions.BadParametersException(error=errors.E_EAS_GGSDUENNSS_NPNF)
    if args.is_valid_uuid(parameters['nid']):
        nid=parameters['nid']
    elif args.is_valid_hex_uuid(parameters['nid']):
        nid=uuid.UUID(parameters['nid'])
    else:
        raise exceptions.BadParametersException(error=errors.E_EAS_GGSDUENNSS_INID)
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.SummaryCreationException(error=errors.E_EAS_GGSDUENNSS_NIDNF)
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
                'data':aggregated_data\
            })
        if dp_with_data>0:
            return summary
        else:
            return None
    else:
        return None

_generate_user_event_graph_summary_data_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:lambda x:None,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_generate_graph_summary_data_UENNSS,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:lambda x:None,
}

