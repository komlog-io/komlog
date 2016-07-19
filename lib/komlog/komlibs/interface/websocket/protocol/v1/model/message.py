
import decimal
import pandas as pd
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Messages

VERSION = 1

class KomlogMessage:

    def __new__(cls, *args, **kwargs):
        if cls is KomlogMessage:
            raise TypeError('<KomlogMessage> cannot be instantiated directly')
        return object.__new__(cls)

    def __init__(self, action):
        self._v = VERSION
        self._action = action

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        raise TypeError('Action cannot be modified')

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        raise TypeError('Version cannot be modified')

    @classmethod
    def load_from_dict(cls, msg):
        ''' create instance from JSON loaded dict.
            Must be implemented in derived classes. '''
        raise NotImplementedError

    def to_dict(self):
        ''' returns JSON serializable dict.
            Must be implemented in derived classes.'''
        raise NotImplementedError

class SendDsData(KomlogMessage):

    def __init__(self, uri=None, ts=None, content=None):
        if uri is not None:
            self.uri=uri
        if ts is not None:
            self.ts=ts
        if content is not None:
            self.content=content
        super().__init__(action=Messages.SEND_DS_DATA)

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
            and args.is_valid_int(msg['v']) and msg['v']==VERSION
            and args.is_valid_string(msg['action']) and msg['action']==Messages.SEND_DS_DATA.value
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

    def __init__(self, uri=None, ts=None, content=None):
        if uri is not None:
            self.uri=uri
        if ts is not None:
            self.ts=ts
        if content is not None:
            self.content=content
        super().__init__(action=Messages.SEND_DP_DATA)

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
            and args.is_valid_int(msg['v']) and msg['v']==VERSION
            and args.is_valid_string(msg['action']) and msg['action']==Messages.SEND_DP_DATA.value
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

    def __init__(self, ts=None, uris=None):
        if ts is not None:
            self.ts=ts
        if uris is not None:
            self.uris=uris
        super().__init__(action=Messages.SEND_MULTI_DATA)

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
            and args.is_valid_int(msg['v']) and msg['v']==VERSION
            and args.is_valid_string(msg['action']) and msg['action']==Messages.SEND_MULTI_DATA.value
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

    def __init__(self, uri=None):
        if uri is not None:
            self.uri=uri
        super().__init__(action=Messages.HOOK_TO_URI)

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
            and args.is_valid_int(msg['v']) and msg['v']==VERSION
            and args.is_valid_string(msg['action']) and msg['action']==Messages.HOOK_TO_URI.value
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

    def __init__(self, uri=None):
        if uri is not None:
            self.uri=uri
        super().__init__(action=Messages.UNHOOK_FROM_URI)

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
            and args.is_valid_int(msg['v']) and msg['v']==VERSION
            and args.is_valid_string(msg['action']) and msg['action']==Messages.UNHOOK_FROM_URI.value
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

