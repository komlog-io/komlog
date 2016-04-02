#coding:utf-8
from komlog.komapp.modules import modules


class Rescontrol(modules.Module):
    def __init__(self, instance_number):
        super(Rescontrol,self).__init__(name=self.__class__.__name__, instance_number=instance_number, needs_db=True, needs_msgbus=True)

