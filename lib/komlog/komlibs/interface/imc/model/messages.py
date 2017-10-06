'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

import uuid
import json
from enum import Enum, unique
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.general.time.timeuuid import TimeUUID
from komlog.komlibs.interface.imc import exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komfig import logging


#MESSAGE LIST
@unique
class Messages(Enum):
    # Datapoint related

    MAP_VARS_MESSAGE                        = 'MAPVARS'
    MON_VAR_MESSAGE                         = 'MONVAR'
    GDTREE_MESSAGE                          = 'GDTREE'
    NEG_VAR_MESSAGE                         = 'NEGVAR'
    POS_VAR_MESSAGE                         = 'POSVAR'

    # Datasource related

    FILL_DATAPOINT_MESSAGE                  = 'FILLDP'
    FILL_DATASOURCE_MESSAGE                 = 'FILLDS'
    GENERATE_TEXT_SUMMARY_MESSAGE           = 'GENTEXTSUMMARY'
    URIS_UPDATED_MESSAGE                    = 'URISUPDT'
    ASSOCIATE_EXISTING_DTREE_MESSAGE        = 'AEDTREE'
    UPDATE_DATASOURCE_FEATURES_MESSAGE      = 'DSFEATUPD'
    MONITOR_IDENTIFIED_URIS_MESSAGE         = 'MONIDU'

    # Notifications related

    FORGET_MAIL_MESSAGE                     = 'FORGETMAIL'
    NEW_USR_NOTIF_MESSAGE                   = 'NEWUSR'
    NEW_INV_MAIL_MESSAGE                    = 'NEWINV'
    USER_EVENT_MESSAGE                      = 'USEREV'
    USER_EVENT_RESPONSE_MESSAGE             = 'USEREVRESP'

    # authorization related

    RESOURCE_AUTHORIZATION_UPDATE_MESSAGE   = 'RESAUTH'
    UPDATE_QUOTES_MESSAGE                   = 'UPDQUO'

    # User management related

    DELETE_USER_MESSAGE                     = 'DELUSER'
    DELETE_AGENT_MESSAGE                    = 'DELAGENT'
    DELETE_DATASOURCE_MESSAGE               = 'DELDS'
    DELETE_DATAPOINT_MESSAGE                = 'DELDP'
    DELETE_WIDGET_MESSAGE                   = 'DELWIDGET'
    DELETE_DASHBOARD_MESSAGE                = 'DELDASHB'
    NEW_DP_WIDGET_MESSAGE                   = 'NEWDPW'
    NEW_DS_WIDGET_MESSAGE                   = 'NEWDSW'

    # websocket iface related

    SEND_SESSION_DATA_MESSAGE               = 'SSDATA'
    CLEAR_SESSION_HOOKS_MESSAGE             = 'CLSHOOKS'
    HOOK_NEW_URIS_MESSAGE                   = 'HOOKNEW'
    DATA_INTERVAL_REQUEST_MESSAGE           = 'DATINT'

class Catalog(type):
    def __init__(cls, name, bases, dct):
        if hasattr(cls, '_type_'):
            cls._catalog_[cls._type_.value]=cls
        super().__init__(name, bases, dct)

class IMCMessage(metaclass=Catalog):
    _catalog_ = {}

    def __new__(cls, *args, **kwargs):
        if cls is IMCMessage:
            raise TypeError('<IMCMessage> cannot be instantiated directly')
        return object.__new__(cls)

    @property
    def type(self):
        return self._type_

    @type.setter
    def type(self, value):
        raise TypeError('Type cannot be modified')

    @classmethod
    def load_from_serialization(cls, msg):
        if cls is IMCMessage:
            if isinstance(msg, str):
                try:
                    return cls._catalog_[msg.split('|')[0]].load_from_serialization(msg)
                except KeyError:
                    raise exceptions.BadParametersException(error=Errors.E_IIMM_IMC_UMT)
            raise exceptions.BadParametersException(error=Errors.E_IIMM_IMC_MNS)
        else:
            raise NotImplementedError

class MapVarsMessage(IMCMessage):
    _type_ = Messages.MAP_VARS_MESSAGE

    def __init__(self, did, date):
        self.did = did
        self.date = date

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IDID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IDT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did, h_date = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IHDID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IHDATE)
            did = uuid.UUID(h_did)
            date = uuid.UUID(h_date)
            return cls(did=did, date=date)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex, self._date.hex))

class MonitorVariableMessage(IMCMessage):
    _type_ = Messages.MON_VAR_MESSAGE

    def __init__(self, uid, did, date, position, length, datapointname):
        self.uid = uid
        self.did = did
        self.date = date
        self.position = position
        self.length = length
        self.datapointname = datapointname

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid=uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IUID)

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did=did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IDID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date=date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IDT)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if args.is_valid_int(position):
            self._position = position
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IPOS)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if args.is_valid_int(length):
            self._length = length
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_ILEN)

    @property
    def datapointname(self):
        return self._datapointname

    @datapointname.setter
    def datapointname(self, datapointname):
        if args.is_valid_datapointname(datapointname):
            self._datapointname = datapointname
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IDPN)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid, h_did, h_date, s_pos, s_len, datapointname = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IHUID)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IHDID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IHDATE)
            if not args.is_valid_string_int(s_pos):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_ISPOS)
            if not args.is_valid_string_int(s_len):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_ISLEN)
            uid = uuid.UUID(h_uid)
            did = uuid.UUID(h_did)
            date = uuid.UUID(h_date)
            position = int(s_pos)
            length = int(s_len)
            datapointname = datapointname
            return cls(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._uid.hex, self._did.hex, self._date.hex, str(self._position), str(self._length), self.datapointname))

class GenerateDTreeMessage(IMCMessage):
    _type_ = Messages.GDTREE_MESSAGE

    def __init__(self, did):
        self.did = did

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GDTREE_IDID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GDTREE_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GDTREE_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GDTREE_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GDTREE_IHDID)
            did = uuid.UUID(h_did)
            return cls(did=did)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex))

class FillDatapointMessage(IMCMessage):
    _type_ = Messages.FILL_DATAPOINT_MESSAGE

    def __init__(self, pid, date):
        self.pid = pid
        self.date = date

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        if args.is_valid_uuid(pid):
            self._pid = pid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IPID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IDT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_pid, h_date = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IST)
            if not args.is_valid_hex_uuid(h_pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IHPID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IHDATE)
            pid = uuid.UUID(h_pid)
            date = uuid.UUID(h_date)
            return cls(pid=pid, date=date)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._pid.hex, self._date.hex))

class FillDatasourceMessage(IMCMessage):
    _type_ = Messages.FILL_DATASOURCE_MESSAGE

    def __init__(self, did, date):
        self.did = did
        self.date = date

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IDID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IDT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did, h_date = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IHDID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IHDATE)
            did = uuid.UUID(h_did)
            date = uuid.UUID(h_date)
            return cls(did=did, date=date)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex, self._date.hex))

class NegativeVariableMessage(IMCMessage):
    _type_ = Messages.NEG_VAR_MESSAGE

    def __init__(self, pid, date, position, length):
        self.pid = pid
        self.date = date
        self.position = position
        self.length = length

    @property
    def pid(self):
        return self._pid
    
    @pid.setter
    def pid(self, pid):
        if args.is_valid_uuid(pid):
            self._pid = pid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IPID)

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IDT)

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        if args.is_valid_int(position):
            self._position = position
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IPOS)

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, length):
        if args.is_valid_int(length):
            self._length = length
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_ILEN)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_pid, h_date, s_pos, s_len = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IST)
            if not args.is_valid_hex_uuid(h_pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IHPID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IHDATE)
            if not args.is_valid_string_int(s_pos):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_ISPOS)
            if not args.is_valid_string_int(s_len):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_ISLEN)
            pid = uuid.UUID(h_pid)
            date = uuid.UUID(h_date)
            position = int(s_pos)
            length = int(s_len)
            return cls(pid=pid, date=date, position=position, length=length)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._pid.hex, self._date.hex, str(self._position), str(self._length)))

class PositiveVariableMessage(IMCMessage):
    _type_ = Messages.POS_VAR_MESSAGE

    def __init__(self, pid, date, position, length):
        self.pid = pid
        self.date = date
        self.position = position
        self.length = length

    @property
    def pid(self):
        return self._pid
    
    @pid.setter
    def pid(self, pid):
        if args.is_valid_uuid(pid):
            self._pid = pid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IPID)

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IDT)

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        if args.is_valid_int(position):
            self._position = position
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IPOS)

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, length):
        if args.is_valid_int(length):
            self._length = length
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_ILEN)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_pid, h_date, s_pos, s_len = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IST)
            if not args.is_valid_hex_uuid(h_pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IHPID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IHDATE)
            if not args.is_valid_string_int(s_pos):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_ISPOS)
            if not args.is_valid_string_int(s_len):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_ISLEN)
            pid = uuid.UUID(h_pid)
            date = uuid.UUID(h_date)
            position = int(s_pos)
            length = int(s_len)
            return cls(pid=pid, date=date, position=position, length=length)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._pid.hex, self._date.hex, str(self._position), str(self._length)))

class NewUserNotificationMessage(IMCMessage):
    _type_ = Messages.NEW_USR_NOTIF_MESSAGE

    def __init__(self, email, code):
        self.email = email
        self.code = code

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if args.is_valid_email(email):
            self._email = email
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_IEMAIL)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        if args.is_valid_code(code):
            self._code = code
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_ICODE)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, email, code = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_IST)
            email = email
            code = code
            return cls(email=email, code=code)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._email, self._code))

class UpdateQuotesMessage(IMCMessage):
    _type_ = Messages.UPDATE_QUOTES_MESSAGE

    def __init__(self, operation, params):
        self.operation = operation
        self.params = params

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation):
        if isinstance(operation, Operations):
            self._operation = operation
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IOP)

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        if not isinstance(params, dict):
            raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IPRM)
        else:
            self._params={}
            for key,value in params.items():
                if isinstance(value,list):
                    values=[]
                    for item in value:
                        values.append(uuid.UUID(item) if args.is_valid_hex_uuid(item) or args.is_valid_hex_date(item) else item)
                    self._params[key]=values
                else:
                    self._params[key]=uuid.UUID(value) if args.is_valid_hex_uuid(value) or args.is_valid_hex_date(value) else value

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, operation_name, js_params = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IST)
            try:
                params=json.loads(js_params)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IJSPRM)
            try:
                operation = getattr(Operations, operation_name)
            except (AttributeError,TypeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IOPN)
            return cls(operation=operation, params=params)

    def to_serialization(self):
        params={}
        for key,value in self._params.items():
            if isinstance(value,list):
                values=[]
                for item in value:
                    values.append(item.hex) if args.is_valid_uuid(item) or args.is_valid_date(item) else item
                params[key]=values
            else:
                params[key]=value.hex if args.is_valid_uuid(value) or args.is_valid_date(value) else value
        return '|'.join((self._type_.value, self._operation.name, json.dumps(params)))

class ResourceAuthorizationUpdateMessage(IMCMessage):
    _type_ = Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE

    def __init__(self, operation, params):
        self.operation = operation
        self.params = params

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation):
        if isinstance(operation, Operations):
            self._operation = operation
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IOP)

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        if not isinstance(params, dict):
            raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IPRM)
        else:
            self._params={}
            for key,value in params.items():
                if isinstance(value,list):
                    values=[]
                    for item in value:
                        values.append(uuid.UUID(item) if args.is_valid_hex_uuid(item) or args.is_valid_hex_date(item) else item)
                    self._params[key]=values
                else:
                    self._params[key]=uuid.UUID(value) if args.is_valid_hex_uuid(value) or args.is_valid_hex_date(value) else value

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, operation_name, js_params = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IST)
            try:
                params=json.loads(js_params)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IJSPRM)
            try:
                operation = getattr(Operations, operation_name)
            except (AttributeError,TypeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IOPN)
            return cls(operation=operation, params=params)

    def to_serialization(self):
        params={}
        for key,value in self._params.items():
            if isinstance(value,list):
                values=[]
                for item in value:
                    values.append(item.hex) if args.is_valid_uuid(item) or args.is_valid_date(item) else item
                params[key]=values
            else:
                params[key]=value.hex if args.is_valid_uuid(value) or args.is_valid_date(value) else value
        return '|'.join((self._type_.value, self._operation.name, json.dumps(params)))

class NewDPWidgetMessage(IMCMessage):
    _type_ = Messages.NEW_DP_WIDGET_MESSAGE

    def __init__(self, uid, pid):
        self.uid = uid
        self.pid = pid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid = uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IUID)

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        if args.is_valid_uuid(pid):
            self._pid = pid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IPID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid, h_pid = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IHUID)
            if not args.is_valid_hex_uuid(h_pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IHPID)
            uid = uuid.UUID(h_uid)
            pid = uuid.UUID(h_pid)
            return cls(uid=uid, pid=pid)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._uid.hex, self._pid.hex))

class NewDSWidgetMessage(IMCMessage):
    _type_ = Messages.NEW_DS_WIDGET_MESSAGE

    def __init__(self, uid, did):
        self.uid = uid
        self.did = did

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid = uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IUID)

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IDID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid, h_did = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IHUID)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IHDID)
            uid = uuid.UUID(h_uid)
            did = uuid.UUID(h_did)
            return cls(uid=uid, did=did)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._uid.hex, self._did.hex))

class DeleteUserMessage(IMCMessage):
    _type_ = Messages.DELETE_USER_MESSAGE

    def __init__(self, uid):
        self.uid = uid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid = uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELUSER_IUID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELUSER_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELUSER_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELUSER_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELUSER_IHUID)
            uid = uuid.UUID(h_uid)
            return cls(uid=uid)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._uid.hex))

class DeleteAgentMessage(IMCMessage):
    _type_ = Messages.DELETE_AGENT_MESSAGE

    def __init__(self, aid):
        self.aid = aid

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, aid):
        if args.is_valid_uuid(aid):
            self._aid = aid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELAGENT_IAID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_aid = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELAGENT_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELAGENT_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELAGENT_IST)
            if not args.is_valid_hex_uuid(h_aid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELAGENT_IHAID)
            aid = uuid.UUID(h_aid)
            return cls(aid=aid)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._aid.hex))

class DeleteDatasourceMessage(IMCMessage):
    _type_ = Messages.DELETE_DATASOURCE_MESSAGE

    def __init__(self, did):
        self.did = did

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDS_IDID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDS_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDS_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDS_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDS_IHDID)
            did = uuid.UUID(h_did)
            return cls(did=did)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex))

class DeleteDatapointMessage(IMCMessage):
    _type_ = Messages.DELETE_DATAPOINT_MESSAGE

    def __init__(self, pid):
        self.pid = pid

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        if args.is_valid_uuid(pid):
            self._pid = pid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDP_IPID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_pid = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDP_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDP_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDP_IST)
            if not args.is_valid_hex_uuid(h_pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDP_IHPID)
            pid = uuid.UUID(h_pid)
            return cls(pid=pid)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._pid.hex))

class DeleteWidgetMessage(IMCMessage):
    _type_ = Messages.DELETE_WIDGET_MESSAGE

    def __init__(self, wid):
        self.wid = wid

    @property
    def wid(self):
        return self._wid

    @wid.setter
    def wid(self, wid):
        if args.is_valid_uuid(wid):
            self._wid = wid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELWIDGET_IWID)
    
    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_wid = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELWIDGET_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELWIDGET_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELWIDGET_IST)
            if not args.is_valid_hex_uuid(h_wid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELWIDGET_IHWID)
            wid = uuid.UUID(h_wid)
            return cls(wid=wid)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._wid.hex))

class DeleteDashboardMessage(IMCMessage):
    _type_ = Messages.DELETE_DASHBOARD_MESSAGE

    def __init__(self, bid):
        self.bid = bid

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, bid):
        if args.is_valid_uuid(bid):
            self._bid = bid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDASHB_IBID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_bid = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDASHB_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDASHB_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDASHB_IST)
            if not args.is_valid_hex_uuid(h_bid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDASHB_IHBID)
            bid = uuid.UUID(h_bid)
            return cls(bid=bid)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._bid.hex))

class UserEventMessage(IMCMessage):
    _type_ = Messages.USER_EVENT_MESSAGE

    def __init__(self, uid, event_type, parameters=None):
        self.uid = uid
        self.event_type = event_type
        self.parameters = parameters

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid = uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IUID)

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        if args.is_valid_int(event_type):
            self._event_type = event_type
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IET)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        if parameters is None:
            self._parameters = {}
        elif isinstance(parameters, dict):
            self._parameters = parameters
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IPRM)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid, s_event_type, js_parameters = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IHUID)
            if not args.is_valid_string_int(s_event_type):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_ISET)
            try:
                parameters=json.loads(js_parameters)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IJSPRM)
            uid = uuid.UUID(h_uid)
            event_type = int(s_event_type)
            return cls(uid=uid, event_type=event_type, parameters=parameters)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._uid.hex, str(self._event_type), json.dumps(self._parameters)))

class UserEventResponseMessage(IMCMessage):
    _type_ = Messages.USER_EVENT_RESPONSE_MESSAGE

    def __init__(self, uid, date, parameters=None):
        self.uid = uid
        self.date = date
        self.parameters = parameters

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid = uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IUID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IDT)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        if parameters is None:
            self._parameters = {}
        elif isinstance(parameters, dict):
            self._parameters = parameters
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IPRM)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid, h_date, js_parameters = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IHUID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IHDATE)
            try:
                parameters=json.loads(js_parameters)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IJSPRM)
            uid = uuid.UUID(h_uid)
            date = uuid.UUID(h_date)
            parameters = parameters
            return cls(uid=uid, date=date, parameters=parameters)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._uid.hex, self._date.hex, json.dumps(self._parameters)))

class GenerateTextSummaryMessage(IMCMessage):
    _type_ = Messages.GENERATE_TEXT_SUMMARY_MESSAGE

    def __init__(self, did, date):
        self.did = did
        self.date = date

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IDID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IDT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did, h_date = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IHDID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IHDATE)
            did = uuid.UUID(h_did)
            date = uuid.UUID(h_date)
            return cls(did=did, date=date)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex, self._date.hex))

class NewInvitationMailMessage(IMCMessage):
    _type_ = Messages.NEW_INV_MAIL_MESSAGE

    def __init__(self, email, inv_id):
        self.email = email
        self.inv_id = inv_id

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if args.is_valid_email(email):
            self._email = email
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_IEMAIL)

    @property
    def inv_id(self):
        return self._inv_id

    @inv_id.setter
    def inv_id(self, inv_id):
        if args.is_valid_string(inv_id):
            self._inv_id = inv_id
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_IINV)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, email, inv_id = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_IST)
            return cls(email=email, inv_id=inv_id)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._email, self._inv_id))

class ForgetMailMessage(IMCMessage):
    _type_ = Messages.FORGET_MAIL_MESSAGE

    def __init__(self, email, code):
        self.email = email
        self.code = code

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if args.is_valid_email(email):
            self._email = email
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_IEMAIL)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        if args.is_valid_uuid(code):
            self._code = code
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_ICODE)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, email, h_code = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_IST)
            if not args.is_valid_hex_uuid(h_code):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_IHCODE)
            email = email
            code = uuid.UUID(h_code)
            return cls(email=email, code=code)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._email, self._code.hex))

class UrisUpdatedMessage(IMCMessage):
    _type_ = Messages.URIS_UPDATED_MESSAGE

    def __init__(self, uris, date):
        self.uris = uris
        self.date = date

    @property
    def uris(self):
        return self._uris

    @uris.setter
    def uris(self, uris):
        if (isinstance(uris, list)
            and all(isinstance(item,dict) for item in uris)
            and all('uri' in item for item in uris)
            and all('type' in item for item in uris)
            and all('id' in item for item in uris)
            and all(args.is_valid_uri(item['uri']) for item in uris)
            and all(args.is_valid_uuid(item['id']) or args.is_valid_hex_uuid(item['id']) for item in uris)):
            uri_list=[]
            for item in uris:
                uri_list.append({'uri':item['uri'],'type':item['type'],'id':item['id'] if args.is_valid_uuid(item['id']) else uuid.UUID(item['id'])})
            self._uris = uri_list
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_IURIS)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_IDT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, js_uris, h_date = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_IST)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_IHDATE)
            try:
                uris=json.loads(js_uris)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_IJSURIS)
            uris = uris
            date = uuid.UUID(h_date)
            return cls(uris=uris, date=date)

    def to_serialization(self):
        uris = [{'uri':item['uri'],'type':item['type'],'id':item['id'].hex} for item in self._uris]
        return '|'.join((self._type_.value, json.dumps(uris), self._date.hex))

class SendSessionDataMessage(IMCMessage):
    _type_ = Messages.SEND_SESSION_DATA_MESSAGE

    def __init__(self, sid, data):
        self.sid = sid
        self.data = data

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        if args.is_valid_uuid(sid):
            self._sid = sid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_ISID)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_sid, js_data = msg.split('|',2)
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_IST)
            if not args.is_valid_hex_uuid(h_sid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_IHSID)
            try:
                data=json.loads(js_data)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_IJSDATA)
            sid = uuid.UUID(h_sid)
            return cls(sid=sid, data=data)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._sid.hex, json.dumps(self._data)))

class ClearSessionHooksMessage(IMCMessage):
    _type_ = Messages.CLEAR_SESSION_HOOKS_MESSAGE

    def __init__(self, sid, ids):
        self.sid = sid
        self.ids = ids

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        if args.is_valid_uuid(sid):
            self._sid = sid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_ISID)

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        if (isinstance(ids, list)
            and all(isinstance(item,list) or isinstance(item,tuple) for item in ids)
            and all(len(item) == 2 for item in ids)
            and all(args.is_valid_uuid(item[0]) or args.is_valid_hex_uuid(item[0]) for item in ids)
            and all(isinstance(item[1],str) for item in ids)):
            id_list=[]
            for item in ids:
                id_list.append((item[0] if args.is_valid_uuid(item[0]) else uuid.UUID(item[0]),item[1]))
            self._ids = id_list
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_IIDS)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_sid, js_ids = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_IST)
            if not args.is_valid_hex_uuid(h_sid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_IHSID)
            try:
                ids=json.loads(js_ids)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_IJSIDS)
            sid = uuid.UUID(h_sid)
            ids = ids
            return cls(sid=sid, ids=ids)

    def to_serialization(self):
        ids=[(item[0].hex,item[1]) for item in self._ids]
        return '|'.join((self._type_.value, self._sid.hex, json.dumps(ids)))

class HookNewUrisMessage(IMCMessage):
    _type_ = Messages.HOOK_NEW_URIS_MESSAGE

    def __init__(self, uid, date, uris):
        self.uid = uid
        self.date = date
        self.uris = uris

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if args.is_valid_uuid(uid):
            self._uid = uid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IUID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IDT)

    @property
    def uris(self):
        return self._uris

    @uris.setter
    def uris(self, uris):
        if (isinstance(uris, list)
            and all(isinstance(item,dict) for item in uris)
            and all('uri' in item for item in uris)
            and all('type' in item for item in uris)
            and all('id' in item for item in uris)
            and all(args.is_valid_uri(item['uri']) for item in uris)
            and all(args.is_valid_uuid(item['id']) or args.is_valid_hex_uuid(item['id']) for item in uris)):
            uri_list=[]
            for item in uris:
                uri_list.append({'uri':item['uri'],'type':item['type'],'id':item['id'] if args.is_valid_uuid(item['id']) else uuid.UUID(item['id'])})
            self._uris = uri_list
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IURIS)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_uid, h_date, js_uris = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IST)
            if not args.is_valid_hex_uuid(h_uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IHUID)
            if not args.is_valid_hex_date(h_date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IHDATE)
            try:
                uris=json.loads(js_uris)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IJSURIS)
            uid = uuid.UUID(h_uid)
            date = uuid.UUID(h_date)
            return cls(uid=uid, date=date, uris=uris)

    def to_serialization(self):
        uris = [{'uri':item['uri'],'type':item['type'],'id':item['id'].hex} for item in self._uris]
        return '|'.join((self._type_.value, self._uid.hex, self._date.hex,  json.dumps(uris)))

class DataIntervalRequestMessage(IMCMessage):
    _type_ = Messages.DATA_INTERVAL_REQUEST_MESSAGE

    def __init__(self, sid, uri, ii, ie, count=None, irt=None):
        self.sid = sid
        self.uri = uri
        self.ii = ii
        self.ie = ie
        self.count = count
        self.irt = irt

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        if args.is_valid_uuid(sid):
            self._sid = sid
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_ISID)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        if (isinstance(uri,dict)
            and 'uri' in uri
            and 'type' in uri
            and 'id' in uri
            and args.is_valid_uri(uri['uri'])
            and (args.is_valid_uuid(uri['id']) or args.is_valid_hex_uuid(uri['id']))):
            self._uri={'uri':uri['uri'],'type':uri['type'],'id':uri['id'] if args.is_valid_uuid(uri['id']) else uuid.UUID(uri['id'])}
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IURI)

    @property
    def ii(self):
        return self._ii

    @ii.setter
    def ii(self, ii):
        if args.is_valid_date(ii):
            self._ii = ii
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_III)

    @property
    def ie(self):
        return self._ie

    @ie.setter
    def ie(self, ie):
        if args.is_valid_date(ie):
            self._ie = ie
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IIE)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        if count is None:
            self._count = None
        elif args.is_valid_int(count):
            self._count = count
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_ICOUNT)

    @property
    def irt(self):
        return self._irt

    @irt.setter
    def irt(self, value):
        if value is None:
            self._irt = None
        elif args.is_valid_message_sequence(value):
            self._irt = value
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IIRT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_sid, h_ii, h_ie, js_uri, js_count, js_irt = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IST)
            if not args.is_valid_hex_uuid(h_sid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IHSID)
            if not args.is_valid_hex_date(h_ii):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IHII)
            if not args.is_valid_hex_date(h_ie):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IHIE)
            try:
                uri=json.loads(js_uri)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IJSURI)
            try:
                count=json.loads(js_count)
            except (TypeError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IJSCOUNT)
            try:
                irt=TimeUUID(s=json.loads(js_irt)) if json.loads(js_irt) != None else None
            except (AttributeError, TypeError, ValueError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DIRM_IJSIRT)
            sid = uuid.UUID(h_sid)
            ii = uuid.UUID(h_ii)
            ie = uuid.UUID(h_ie)
            return cls(sid=sid, ii=ii, ie=ie, uri=uri, count=count, irt=irt)

    def to_serialization(self):
        uri = {'uri':self._uri['uri'],'type':self._uri['type'],'id':self._uri['id'].hex}
        return '|'.join((self._type_.value, self._sid.hex, self._ii.hex, self._ie.hex, json.dumps(uri),json.dumps(self._count),json.dumps(self._irt.hex if self._irt != None else None)))


class AssociateExistingDTreeMessage(IMCMessage):
    _type_ = Messages.ASSOCIATE_EXISTING_DTREE_MESSAGE

    def __init__(self, did):
        self.did = did

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_AEDTREE_IDID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_AEDTREE_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_AEDTREE_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_AEDTREE_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_AEDTREE_IHDID)
            did = uuid.UUID(h_did)
            return cls(did=did)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex))


class UpdateDatasourceFeaturesMessage(IMCMessage):
    _type_ = Messages.UPDATE_DATASOURCE_FEATURES_MESSAGE

    def __init__(self, did):
        self.did = did

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DSFEATUPD_IDID)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DSFEATUPD_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_DSFEATUPD_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DSFEATUPD_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DSFEATUPD_IHDID)
            did = uuid.UUID(h_did)
            return cls(did=did)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex))


class MonitorIdentifiedUrisMessage(IMCMessage):
    _type_ = Messages.MONITOR_IDENTIFIED_URIS_MESSAGE

    def __init__(self, did, date=None):
        self.did = did
        self.date = date

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, did):
        if args.is_valid_uuid(did):
            self._did = did
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_IDID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if date == None or args.is_valid_date(date):
            self._date = date
        else:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_IDT)

    @classmethod
    def load_from_serialization(cls, msg):
        try:
            m_type, h_did, js_date = msg.split('|')
        except ValueError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_ELFS)
        except AttributeError:
            raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_MINS)
        else:
            if not m_type == cls._type_.value:
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_IST)
            if not args.is_valid_hex_uuid(h_did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_IHDID)
            try:
                date=TimeUUID(s=json.loads(js_date)) if json.loads(js_date) != None else None
            except (AttributeError, TypeError, ValueError,json.JSONDecodeError):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONIDU_IJSDATE)
            did = uuid.UUID(h_did)
            return cls(did=did, date=date)

    def to_serialization(self):
        return '|'.join((self._type_.value, self._did.hex, json.dumps(self._date.hex if self._date != None else None)))

