#coding:utf-8
###############################################################################
# Rescontrol Module
#
# This module implement Resource and authorization related control messages
#
#
# author: jcazor
# date: 30/09/2013
###############################################################################

from komapp import modules


class Rescontrol(modules.Module):
    def __init__(self, instance_number):
        super(Rescontrol,self).__init__(name=self.__class__.__name__, instance_number=instance_number, needs_db=True, needs_msgbus=True)

