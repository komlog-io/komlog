from komapp.modules import modules

class Events(modules.Module):
    def __init__(self, instance_number):
        super(Events,self).__init__(name=self.__class__.__name__, instance_number=instance_number, needs_db=True, needs_msgbus=True)
