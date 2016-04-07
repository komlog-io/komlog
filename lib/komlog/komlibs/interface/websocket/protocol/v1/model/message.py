from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Message

class SendDsDataMessage:
    def __init__(self, message):
        self._action=None
        self._v=None
        self._payload=None
        if args.is_valid_dict(message)\
            and 'v' in message\
            and 'action' in message\
            and 'payload' in message:
            self.v=message['v']
            self.action=message['action']
            self.payload=message['payload']
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDDM_IMT)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if args.is_valid_string(value) and value==Message.SEND_DS_DATA:
            self._action=value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDDM_IA)

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        if args.is_valid_int(value) and value==1:
            self._v=value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDDM_IV)

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        if args.is_valid_dict(value)\
            and 'uri' in value\
            and args.is_valid_uri(value['uri'])\
            and 'ts' in value\
            and args.is_valid_timestamp(value['ts'])\
            and 'content' in value\
            and args.is_valid_datasource_content(value['content']):
            self._payload={
                'uri':value['uri'],
                'ts':value['ts'],
                'content':value['content']
            }
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSPV1MM_SDDM_IPL)

