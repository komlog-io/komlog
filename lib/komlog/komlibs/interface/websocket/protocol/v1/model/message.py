import decimal
import pandas as pd
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Messages

class Catalog(type):
    def __init__(cls, name, bases, dct):
        if hasattr(cls, '_action_'):
            cls._catalog_[cls._action_.value]=cls
        super().__init__(name, bases, dct)

class KomlogMessage(metaclass=Catalog):
    _version_ = 1
    _catalog_ = {}

    def __new__(cls, *args, **kwargs):
        if cls is KomlogMessage:
            raise TypeError('<KomlogMessage> cannot be instantiated directly')
        return object.__new__(cls)

    @property
    def action(self):
        return self._action_

    @action.setter
    def action(self, value):
        raise TypeError('Action cannot be modified')

    @property
    def v(self):
        return self._version_

    @v.setter
    def v(self, value):
        raise TypeError('Version cannot be modified')

    @classmethod
    def load_from_dict(cls, msg):
        if cls is KomlogMessage:
            if isinstance(msg, dict) and 'action' in msg:
                try:
                    return cls._catalog_[msg['action']].load_from_dict(msg)
                except KeyError:
                    raise TypeError('Unknown message type')
            raise TypeError('Message not supported')
        else:
            raise NotImplementedError

class SendDsData(KomlogMessage):
    _action_ = Messages.SEND_DS_DATA

    def __init__(self, uri, ts, content):
        self.uri=uri
        self.ts=ts
        self.content=content

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if args.is_valid_uri(uri):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDSD_IURI)

    @property
    def ts(self):
        return self._ts

    @ts.setter
    def ts(self, ts):
        if args.is_valid_isodate(ts):
            self._ts=pd.Timestamp(ts,tz='utc') if pd.Timestamp(ts).tz is None else pd.Timestamp(ts)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDSD_ITS)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if args.is_valid_datasource_content(content):
            self._content=content
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDSD_ICNT)

    @classmethod
    def load_from_dict(cls, msg):
        ''' create instance from JSON loaded dict '''
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 'ts' in msg['payload']
            and 'content' in msg['payload']):
            uri=msg['payload']['uri']
            ts=msg['payload']['ts']
            content=msg['payload']['content']
            return cls(uri=uri, ts=ts, content=content)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDSD_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'uri':self.uri,
                'ts':self.ts.isoformat(),
                'content':self.content
            }
        }

class SendDpData(KomlogMessage):
    _action_ = Messages.SEND_DP_DATA

    def __init__(self, uri, ts, content):
        self.uri=uri
        self.ts=ts
        self.content=content

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if args.is_valid_uri(uri):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDPD_IURI)

    @property
    def ts(self):
        return self._ts

    @ts.setter
    def ts(self, ts):
        if args.is_valid_isodate(ts):
            self._ts=pd.Timestamp(ts,tz='utc') if pd.Timestamp(ts).tz is None else pd.Timestamp(ts)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDPD_ITS)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if args.is_valid_datapoint_content(content):
            self._content=decimal.Decimal(content)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDPD_ICNT)

    @classmethod
    def load_from_dict(cls, msg):
        ''' create instance from JSON loaded dict '''
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 'ts' in msg['payload']
            and 'content' in msg['payload']):
            uri=msg['payload']['uri']
            ts=msg['payload']['ts']
            content=msg['payload']['content']
            return cls(uri=uri, ts=ts, content=content)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDPD_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'uri':self.uri,
                'ts':self.ts.isoformat(),
                'content':str(self.content)
            }
        }

class SendMultiData(KomlogMessage):
    _action_ = Messages.SEND_MULTI_DATA

    def __init__(self, ts, uris):
        self.ts=ts
        self.uris=uris

    @property
    def uris(self):
        return self._uris

    @uris.setter
    def uris(self, uris):
        if (isinstance(uris,list)
            and all(isinstance(item,dict) for item in uris)
            and all('uri' in item for item in uris)
            and all(args.is_valid_uri(item['uri']) for item in uris)
            and all('type' in item for item in uris)
            and all(item['type'] in (vertex.DATASOURCE,vertex.DATAPOINT) for item in uris)
            and all('content' in item for item in uris)
            and all(args.is_valid_datasource_content(item['content']) for item in uris if item['type'] == vertex.DATASOURCE)
            and all(args.is_valid_datapoint_content(item['content']) for item in uris if item['type'] == vertex.DATAPOINT)):
            ds_uris=[{'uri':item['uri'],'type':item['type'],'content':item['content']} for item in uris if item['type'] == vertex.DATASOURCE]
            dp_uris=[{'uri':item['uri'],'type':item['type'],'content':decimal.Decimal(item['content'])} for item in uris if item['type'] == vertex.DATAPOINT]
            self._uris=ds_uris+dp_uris
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SMTD_IURIS)

    @property
    def ts(self):
        return self._ts

    @ts.setter
    def ts(self, ts):
        if args.is_valid_isodate(ts):
            self._ts=pd.Timestamp(ts,tz='utc') if pd.Timestamp(ts).tz is None else pd.Timestamp(ts)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SMTD_ITS)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'ts' in msg['payload']
            and 'uris' in msg['payload']):
            ts=msg['payload']['ts']
            uris=msg['payload']['uris']
            return cls(ts=ts, uris=uris)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SMTD_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        ds_uris=[{'uri':item['uri'],'type':item['type'],'content':item['content']} for item in self._uris if item['type'] == vertex.DATASOURCE]
        dp_uris=[{'uri':item['uri'],'type':item['type'],'content':str(item['content'])} for item in self._uris if item['type'] == vertex.DATAPOINT]
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'ts':self.ts.isoformat(),
                'uris':ds_uris+dp_uris
            }
        }

class HookToUri(KomlogMessage):
    _action_  = Messages.HOOK_TO_URI

    def __init__(self, uri):
        self.uri=uri

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if args.is_valid_uri(uri):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_HTU_IURI)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']):
            uri=msg['payload']['uri']
            return cls(uri=uri)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_HTU_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'uri':self.uri
            }
        }

class UnHookFromUri(KomlogMessage):
    _action_ = Messages.UNHOOK_FROM_URI

    def __init__(self, uri):
        self.uri=uri

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if args.is_valid_uri(uri):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_UHFU_IURI)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']):
            uri=msg['payload']['uri']
            return cls(uri=uri)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_UHFU_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'uri':self.uri
            }
        }

class RequestDataInterval(KomlogMessage):
    _action_ = Messages.REQUEST_DATA_INTERVAL

    def __init__(self, uri, start, end):
        self.uri = uri
        self.start = start
        self.end = end 

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if args.is_valid_uri(uri):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDI_IURI)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if args.is_valid_isodate(start):
            self._start=pd.Timestamp(start,tz='utc') if pd.Timestamp(start).tz is None else pd.Timestamp(start)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDI_ISTART)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if args.is_valid_isodate(end):
            self._end=pd.Timestamp(end,tz='utc') if pd.Timestamp(end).tz is None else pd.Timestamp(end)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDI_IEND)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 'start' in msg['payload']
            and 'end' in msg['payload']):
            uri=msg['payload']['uri']
            start=msg['payload']['start']
            end=msg['payload']['end']
            return cls(uri=uri, start=start, end=end)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDI_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'uri':self.uri,
                'start':self.start.isoformat(),
                'end':self.end.isoformat(),
            }
        }

class SendDataInterval(KomlogMessage):
    _action_ = Messages.SEND_DATA_INTERVAL

    def __init__(self, uri, start, end, data):
        self.uri = uri
        self.start = start
        self.end = end 
        self.data = data

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (isinstance(uri,dict)
            and 'uri' in uri
            and args.is_valid_uri(uri['uri'])
            and 'type' in uri
            and uri['type'] in (vertex.DATASOURCE,vertex.DATAPOINT)):
            self._uri={'uri':uri['uri'],'type':uri['type']}
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_IURI)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if args.is_valid_isodate(start):
            self._start=pd.Timestamp(start,tz='utc') if pd.Timestamp(start).tz is None else pd.Timestamp(start)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_ISTART)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if args.is_valid_isodate(end):
            self._end=pd.Timestamp(end,tz='utc') if pd.Timestamp(end).tz is None else pd.Timestamp(end)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_IEND)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if (isinstance(data, list)
            and all(
                isinstance(item,tuple)
                and len(item)==2
                and args.is_valid_isodate(item[0])
                and isinstance(item[0],str)
                and pd.Timestamp(item[0]).tz is not None
                and isinstance(item[1],str) for item in data)
            ):
            self._data=data
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_IDATA)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 'start' in msg['payload']
            and 'end' in msg['payload']
            and 'data' in msg['payload']):
            uri=msg['payload']['uri']
            start=msg['payload']['start']
            end=msg['payload']['end']
            data=msg['payload']['data']
            return cls(uri=uri, start=start, end=end, data=data)
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'payload':{
                'uri':self.uri,
                'start':self.start.isoformat(),
                'end':self.end.isoformat(),
                'data':self.data
            }
        }

