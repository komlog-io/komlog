from komlog.komapp.modules import modules

class Storing(modules.Module):
    def __init__(self, instance_number):
        super(Storing,self).__init__(name=self.__class__.__name__, instance_number=instance_number, needs_db=True, needs_msgbus=True)

