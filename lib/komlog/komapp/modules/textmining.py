from komlog.komapp.modules import modules


class Textmining(modules.Module):
    def __init__(self, instance):
        super().__init__(
            name=self.__class__.__name__,
            instance=instance,
            needs_db=True,
            needs_msgbus=True,
            needs_mailer=False,
            tasks=[self._messages_listener]
        )

def get_module(instance):
    mod = Textmining(instance=instance)
    return mod

