import uuid
import decimal
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.model import message, response
from komlog.komlibs.interface.websocket.model.types import Messages
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors

class MessagesVersionCatalog(message.MessagesCatalog):
    _version_ = 1

    def __new__(cls, *args, **kwargs):
        if cls is MessagesVersionCatalog:
            raise TypeError('<MessagesVersionCatalog> cannot be instantiated directly')
        return object.__new__(cls)

    def __init__(self, seq=None, irt=None):
        self.seq = seq if seq else uuid.uuid1().hex[0:20]
        self.irt = irt

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, value):
        if hasattr(self, '_seq'):
            raise TypeError('Sequence cannot be modified')
        elif args.is_valid_message_sequence(value):
            self._seq = value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_MVC_ISEQ)

    @property
    def irt(self):
        return self._irt

    @irt.setter
    def irt(self, value):
        if value is None or args.is_valid_message_sequence(value):
            self._irt = value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_MVC_IIRT)

    @classmethod
    def catalog(cls):
        return cls._catalog_[cls._version_]

    @classmethod
    def get_message(cls, action, **kwargs):
        if cls is MessagesVersionCatalog:
            if isinstance(action,str):
                try:
                    return cls._catalog_[cls._version_][action](**kwargs)
                except KeyError:
                    pass
        return None

class GenericResponse(response.GenericResponse):
    def __init__(self, status, irt, error=Errors.OK, reason=None, seq=None):
        super().__init__(status=status, error=error, reason=reason, v=1, seq=seq, irt=irt)

class SendDsData(MessagesVersionCatalog):
    _action_ = Messages.SEND_DS_DATA

    def __init__(self, uri, t, content, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
        self.uri=uri
        self.t=t
        self.content=content

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (args.is_valid_uri(uri) or args.is_valid_global_uri(uri)):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDSD_IURI)

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        if args.is_valid_date(t):
            self._t=t
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
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 't' in msg['payload'] and args.is_valid_hex_date(msg['payload']['t'])
            and 'content' in msg['payload']):
            uri=msg['payload']['uri']
            t=uuid.UUID(msg['payload']['t'])
            content=msg['payload']['content']
            return cls(uri=uri, t=t, content=content, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDSD_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                'uri':self.uri,
                't':self.t.hex,
                'content':self.content
            }
        }

class SendDpData(MessagesVersionCatalog):
    _action_ = Messages.SEND_DP_DATA

    def __init__(self, uri, t, content, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
        self.uri=uri
        self.t=t
        self.content=content

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (args.is_valid_uri(uri) or args.is_valid_global_uri(uri)):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDPD_IURI)

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        if args.is_valid_date(t):
            self._t=t
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
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 't' in msg['payload'] and args.is_valid_hex_date(msg['payload']['t'])
            and 'content' in msg['payload']):
            uri=msg['payload']['uri']
            t=uuid.UUID(msg['payload']['t'])
            content=msg['payload']['content']
            return cls(uri=uri, t=t, content=content, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDPD_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                'uri':self.uri,
                't':self.t.hex,
                'content':str(self.content)
            }
        }

class SendMultiData(MessagesVersionCatalog):
    _action_ = Messages.SEND_MULTI_DATA

    def __init__(self, t, uris, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
        self.t=t
        self.uris=uris

    @property
    def uris(self):
        return self._uris

    @uris.setter
    def uris(self, uris):
        if (isinstance(uris,list)
            and all(isinstance(item,dict) for item in uris)
            and all('uri' in item for item in uris)
            and all((args.is_valid_uri(item['uri']) or args.is_valid_global_uri(item['uri'])) for item in uris)
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
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        if args.is_valid_date(t):
            self._t=t
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SMTD_ITS)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 't' in msg['payload'] and args.is_valid_hex_date(msg['payload']['t'])
            and 'uris' in msg['payload']):
            t=uuid.UUID(msg['payload']['t'])
            uris=msg['payload']['uris']
            return cls(t=t, uris=uris, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SMTD_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        ds_uris=[{'uri':item['uri'],'type':item['type'],'content':item['content']} for item in self._uris if item['type'] == vertex.DATASOURCE]
        dp_uris=[{'uri':item['uri'],'type':item['type'],'content':str(item['content'])} for item in self._uris if item['type'] == vertex.DATAPOINT]
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                't':self.t.hex,
                'uris':ds_uris+dp_uris
            }
        }

class HookToUri(MessagesVersionCatalog):
    _action_  = Messages.HOOK_TO_URI

    def __init__(self, uri, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
        self.uri=uri

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (args.is_valid_uri(uri) or args.is_valid_global_uri(uri)):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_HTU_IURI)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']):
            uri=msg['payload']['uri']
            return cls(uri=uri, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_HTU_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                'uri':self.uri
            }
        }

class UnHookFromUri(MessagesVersionCatalog):
    _action_ = Messages.UNHOOK_FROM_URI

    def __init__(self, uri, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
        self.uri=uri

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (args.is_valid_uri(uri) or args.is_valid_global_uri(uri)):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_UHFU_IURI)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']):
            uri=msg['payload']['uri']
            return cls(uri=uri, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_UHFU_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                'uri':self.uri
            }
        }

class RequestData(MessagesVersionCatalog):
    _action_ = Messages.REQUEST_DATA

    def __init__(self, uri, start=None, end=None, count=None, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
        self.uri = uri
        self.start = start
        self.end = end
        self.count = count
        if count is None and (start is None or end is None):
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDT_ECOIN)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (args.is_valid_uri(uri) or args.is_valid_global_uri(uri)):
            self._uri=uri
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDT_IURI)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start is None:
            self._start = None
        elif args.is_valid_date(start):
            self._start=start
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDT_ISTART)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if end is None:
            self._end = None
        elif args.is_valid_date(end):
            self._end=end
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDT_IEND)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        if count is None:
            self._count = None
        elif args.is_valid_int(count):
            self._count=count
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDT_ICOUNT)

    @classmethod
    def load_from_dict(cls, msg):
        if (isinstance(msg,dict)
            and 'v' in msg
            and 'action' in msg
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 'start' in msg['payload'] and (msg['payload']['start'] is None or args.is_valid_hex_date(msg['payload']['start']))
            and 'end' in msg['payload'] and (msg['payload']['end'] is None or args.is_valid_hex_date(msg['payload']['end']))
            and 'count' in msg['payload']):
            uri=msg['payload']['uri']
            start=uuid.UUID(msg['payload']['start']) if msg['payload']['start'] else None
            end=uuid.UUID(msg['payload']['end']) if msg['payload']['end'] else None
            count=msg['payload']['count']
            return cls(uri=uri, start=start, end=end, count=count, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_RQDT_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                'uri':self.uri,
                'start':self._start.hex if self._start else None,
                'end':self._end.hex if self._end else None,
                'count':self._count,
            }
        }

class SendDataInterval(MessagesVersionCatalog):
    _action_ = Messages.SEND_DATA_INTERVAL

    def __init__(self, uri, start, end, data, seq=None, irt=None):
        super().__init__(seq=seq, irt=irt)
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
            and (args.is_valid_uri(uri['uri']) or args.is_valid_global_uri(uri['uri']))
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
        if args.is_valid_date(start):
            self._start=start
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_ISTART)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if args.is_valid_date(end):
            self._end=end
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
                and args.is_valid_hex_date(item[0])
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
            and 'seq' in msg
            and 'irt' in msg
            and 'payload' in msg
            and args.is_valid_int(msg['v']) and msg['v']==cls._version_
            and args.is_valid_string(msg['action']) and msg['action']==cls._action_.value
            and args.is_valid_dict(msg['payload'])
            and 'uri' in msg['payload']
            and 'start' in msg['payload'] and args.is_valid_hex_date(msg['payload']['start'])
            and 'end' in msg['payload'] and args.is_valid_hex_date(msg['payload']['end'])
            and 'data' in msg['payload']):
            uri=msg['payload']['uri']
            start=uuid.UUID(msg['payload']['start'])
            end=uuid.UUID(msg['payload']['end'])
            data=msg['payload']['data']
            return cls(uri=uri, start=start, end=end, data=data, seq=msg['seq'], irt=msg['irt'])
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDI_ELFD)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq,
            'irt':self.irt,
            'payload':{
                'uri':self.uri,
                'start':self.start.hex,
                'end':self.end.hex,
                'data':self.data
            }
        }

