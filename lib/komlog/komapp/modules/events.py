from komlog.komapp.modules import modules


class Events(modules.Module):
    def __init__(self, instance):
        super().__init__(
            name=self.__class__.__name__,
            instance=instance,
            needs_db=True,
            needs_msgbus=True,
            tasks=[self._messages_listener]
        )

def get_module(instance):
    mod = Events(instance=instance)
    return mod

