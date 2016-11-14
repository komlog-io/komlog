from komlog.komapp.modules import modules


class Gestconsole(modules.Module):
    def __init__(self, instance):
        super().__init__(
            name=self.__class__.__name__,
            instance=instance,
            needs_db=True,
            needs_msgbus=True,
            needs_mailer=True,
            tasks=[self._messages_listener]
        )

def get_module(instance):
    mod = Gestconsole(instance=instance)
    return mod

