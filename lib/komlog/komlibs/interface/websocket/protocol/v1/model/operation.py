
from komlog.komlibs.auth.model.operations import Operations as AuthOperations
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Operations


OPAUTHS={
    Operations.NEW_DATASOURCE:AuthOperations.NEW_DATASOURCE,
    Operations.NEW_USER_DATAPOINT:AuthOperations.NEW_USER_DATAPOINT,
    Operations.DATASOURCE_DATA_STORED:AuthOperations.DATASOURCE_DATA_STORED,
    Operations.DATAPOINT_DATA_STORED:AuthOperations.DATAPOINT_DATA_STORED,
}

class WSIFaceOperation:
    def __new__(cls, *args, **kwargs):
        if cls is WSIFaceOperation:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_IC)
        return super(WSIFaceOperation, cls).__new__(cls)

    def __init__(self, oid):
        self._oid = None
        self.oid = oid

    @property
    def oid(self):
        return self._oid

    @oid.setter
    def oid(self, value):
        if self._oid:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_OIDAI)
        if value in Operations:
            self._oid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_IOID)

    @property
    def auth_operation(self):
        return OPAUTHS[self.oid] if self.oid in OPAUTHS else None

class NewDatasourceOperation(WSIFaceOperation):
    def __init__(self, uid, aid, did):
        self._uid = None
        self._aid = None
        self._did = None
        self.uid = uid
        self.aid = aid
        self.did = did
        super().__init__(oid=Operations.NEW_DATASOURCE)

    @property
    def params(self):
        return {
            'uid':self._uid,
            'aid':self._aid,
            'did':self._did
        }

    @params.setter
    def params(self, value):
        raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_PMNA)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if args.is_valid_uuid(value):
            self._uid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_NDSO_IUT)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, value):
        if args.is_valid_uuid(value):
            self._aid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_NDSO_IAT)

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, value):
        if args.is_valid_uuid(value):
            self._did = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_NDSO_IDT)

class NewUserDatapointOperation(WSIFaceOperation):
    def __init__(self, uid, aid, pid):
        self._uid = None
        self._aid = None
        self._pid = None
        self.uid = uid
        self.aid = aid
        self.pid = pid
        super().__init__(oid=Operations.NEW_USER_DATAPOINT)

    @property
    def params(self):
        return {
            'uid':self._uid,
            'aid':self._aid,
            'pid':self._pid
        }

    @params.setter
    def params(self, value):
        raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_PMNA)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if args.is_valid_uuid(value):
            self._uid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_NUDPO_IUT)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, value):
        if args.is_valid_uuid(value):
            self._aid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_NUDPO_IAT)

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        if args.is_valid_uuid(value):
            self._pid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_NUDPO_IPT)

class DatasourceDataStoredOperation(WSIFaceOperation):
    def __init__(self, uid, did, date):
        self._uid = None
        self._did = None
        self._date = None
        self.uid = uid
        self.did = did
        self.date = date
        super().__init__(oid=Operations.DATASOURCE_DATA_STORED)

    @property
    def params(self):
        return {
            'uid':self._uid,
            'did':self._did,
            'date':self._date,
        }

    @params.setter
    def params(self, value):
        raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_PMNA)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if args.is_valid_uuid(value):
            self._uid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_DSDSTO_IUID)

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, value):
        if args.is_valid_uuid(value):
            self._did = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_DSDSTO_IDID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if args.is_valid_date(value):
            self._date = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_DSDSTO_IDATE)

class DatapointDataStoredOperation(WSIFaceOperation):
    def __init__(self, uid, pid, date):
        self._uid = None
        self._pid = None
        self._date = None
        self.uid = uid
        self.pid = pid
        self.date = date
        super().__init__(oid=Operations.DATAPOINT_DATA_STORED)

    @property
    def params(self):
        return {
            'uid':self._uid,
            'pid':self._pid,
            'date':self._date,
        }

    @params.setter
    def params(self, value):
        raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_WSIO_PMNA)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if args.is_valid_uuid(value):
            self._uid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_DPDSTO_IUID)

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        if args.is_valid_uuid(value):
            self._pid = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_DPDSTO_IPID)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if args.is_valid_date(value):
            self._date = value
        else:
            raise exceptions.OperationValidationException(error=Errors.E_IWSPV1MO_DPDSTO_IDATE)

