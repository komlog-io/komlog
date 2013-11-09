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

import sections, options
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komimc import codes as msgcodes
from komlibs.quotes import update,compare

UPDATEFUNCS={}
COMPAREFUNCS={}

class Rescontrol(modules.Module):
    def __init__(self, config, instance_number):
        super(Rescontrol,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.RESCONTROL,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.RESCONTROL,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.RESCONTROL,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['broker'] = self.config.safe_get(sections.RESCONTROL, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Rescontrol module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cass_cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Rescontrol module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype = message.type
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                messages.process_msg_result(msgresult,self.message_bus,self.logger)
            except AttributeError:
                self.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                self.logger.exception('Exception processing message: '+str(e))

    def process_msg_UPDQUO(self, message):
        msgresult=messages.MessageResult(message)
        quotes_to_update=list(message.operation.get_quotes_to_update())
        opparams=message.operation.get_params()
        for quote in quotes_to_update:
            self.logger.debug('Inicio de proceso de quota: '+quote)
            try:
                qvalue=UPDATEFUNCS[quote](cf=self.cass_cf,params=opparams)
            except KeyError:
                try:
                    UPDATEFUNCS[quote]=getattr(update,'update_'+quote)
                    COMPAREFUNCS[quote]=getattr(compare,'compare_'+quote)
                    quotes_to_update.append(quote)
                except Exception as e:
                    self.logger.exception('Exception getting quote funcions: '+quote+' '+str(e))
                    msgresult.retcode=msgcodes.ERROR
            except Exception as e:
                self.logger.exception('Exception in quote update function: '+quote+' '+str(e))
                msgresult.retcode=msgcodes.ERROR
            else:
                if qvalue is not None:
                    ''' quote updated successfully, the return value is the quota value updated'''
                    ''' now determine if quota is aproaching limits '''
                    try:
                        should_block=COMPAREFUNCS[quote](cf=self.cass_cf,params=opparams)
                        if should_block:
                            '''aqui creo un mensaje UPDATEQUOAUTH que se enviara al modulo para que revise el acceso 
                            al interfaz relacionado con la cuota '''
                        msgresult.retcode=msgcodes.SUCCESS
                    except Exception as e:
                        self.logger.exception('Exception in quote compare function: '+quote+' '+str(e))
                        msgresult.retcode=msgcodes.ERROR
                else:
                    self.logger.error('Error updating quote: '+quote)
                    msgresult.retcode=msgcodes.ERROR
        return msgresult


