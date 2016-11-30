
class Catalog(type):
    def __init__(cls, name, bases, dct):
        if hasattr(cls, '_action_') and hasattr(cls, '_version_'):
            try:
                cls._catalog_[cls._version_][cls._action_.value]=cls
            except KeyError:
                cls._catalog_[cls._version_]={}
                cls._catalog_[cls._version_][cls._action_.value]=cls
        super().__init__(name, bases, dct)

class MessagesCatalog(metaclass=Catalog):
    _catalog_ = {}

    def __new__(cls, *args, **kwargs):
        if cls is MessagesCatalog:
            raise TypeError('<MessagesCatalog> cannot be instantiated directly')
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
    def catalog(cls):
        return cls._catalog_

    @classmethod
    def get_message(cls, version, action, **kwargs):
        if cls is MessagesCatalog:
            try:
                return cls._catalog_[version][action.value](**kwargs)
            except KeyError:
                pass
        return None

import komlog.komlibs.interface.websocket.protocol.v1.model.message
