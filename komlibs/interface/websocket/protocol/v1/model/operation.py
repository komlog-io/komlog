
from komlibs.auth import operations as authoperations
from komlibs.general.validation import arguments as args
from komlibs.interface.websocket.protocol.v1 import errors, exceptions
from komlibs.interface.websocket.protocol.v1.model import types


OPAUTHS={
    types.OPERATION_NEW_DATASOURCE:authoperations.NEW_DATASOURCE,
}

class WSIFaceOperation:
    def __new__(cls, *args, **kwargs):
        if cls is WSIFaceOperation:
            raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_WSIO_IC)
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
            raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_WSIO_OIDAI)
        if args.is_valid_int(value):
            self._oid = value
        else:
            raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_WSIO_IOID)

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
        super(NewDatasourceOperation, self).__init__(oid=types.OPERATION_NEW_DATASOURCE)

    @property
    def params(self):
        return {
            'uid':self._uid,
            'aid':self._aid,
            'did':self._did
        }

    @params.setter
    def params(self, value):
        raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_WSIO_PMNA)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if args.is_valid_uuid(value):
            self._uid = value
        else:
            raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_NDSO_IUT)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, value):
        if args.is_valid_uuid(value):
            self._aid = value
        else:
            raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_NDSO_IAT)

    @property
    def did(self):
        return self._did

    @did.setter
    def did(self, value):
        if args.is_valid_uuid(value):
            self._did = value
        else:
            raise exceptions.OperationValidationException(error=errors.E_IWSPV1MO_NDSO_IDT)

