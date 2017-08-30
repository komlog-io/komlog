import uuid
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time.timeuuid import TimeUUID
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.errors import Errors
from komlog.komlibs.interface.websocket.model.types import Messages

class WSocketIfaceResponse:
    def __init__(self, status, error=Errors.OK):
        self.status = status
        self.error = error
        self._ws_messages=[]
        self._imc_messages={'routed':{},'unrouted':[]}

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if args.is_valid_int(value):
            self._status=value
        else:
            raise exceptions.ResponseValidationException(error=Errors.E_IWSMR_PR_IS)

    @property
    def ws_messages(self):
        return self._ws_messages

    @ws_messages.setter
    def ws_messages(self, value):
        raise TypeError

    @property
    def imc_messages(self):
        return self._imc_messages

    @imc_messages.setter
    def imc_messages(self, value):
        raise TypeError

    def add_ws_message(self, msg):
        self._ws_messages.append(msg)
        return True

    def add_imc_message(self, msg, dest=None):
        if dest is not None:
            try:
                self._imc_messages['routed'][dest].append(msg)
            except KeyError:
                self._imc_messages['routed'][dest]=[msg]
        else:
            self._imc_messages['unrouted'].append(msg)
        return True

class GenericResponse:
    _action_ = Messages.GENERIC_RESPONSE

    def __init__(self, status, error, reason=None, irt=None, v=0, seq=None):
        self.v = v
        self.seq = seq if seq else TimeUUID()
        self.status=status
        self.error=error
        self.reason=reason
        self.irt = irt

    @property
    def action(self):
        return self._action_

    @action.setter
    def action(self, value):
        raise TypeError('Action cannot be modified')

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        if hasattr(self, '_v'):
            raise TypeError('Version cannot be modified')
        elif args.is_valid_int(value):
            self._v = value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSMR_GR_IV)

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
            raise exceptions.MessageValidationException(error=Errors.E_IWSMR_GR_ISEQ)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if args.is_valid_int(value):
            self._status=value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSMR_GR_IS)

    @property
    def irt(self):
        return self._irt

    @irt.setter
    def irt(self, value):
        if value is None or args.is_valid_message_sequence(value):
            self._irt = value
        else:
            raise exceptions.MessageValidationException(error=Errors.E_IWSMR_GR_IIRT)

    def to_dict(self):
        ''' returns a JSON serializable dict '''
        return {
            'v':self.v,
            'action':self.action.value,
            'seq':self.seq.hex,
            'irt':self.irt.hex if self.irt != None else None,
            'payload':{
                'status':self.status,
                'error':self.error.value,
                'reason':self.reason
            }
        }

