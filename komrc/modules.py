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
from komfig import config,logger
from komimc import bus as msgbus
from komimc import api as msgapi
from komimc import messages
from komimc import codes as msgcodes
from komlibs.auth.quotes import update as quoup
from komlibs.auth.quotes import compare as quocmp
from komlibs.auth.quotes import deny as quodeny
from komlibs.auth.resources import update as resup


class Rescontrol(modules.Module):
    def __init__(self, instance_number):
        super(Rescontrol,self).__init__(self.__class__.__name__, instance_number)
        self.params={}
        self.params['cassandra_keyspace'] = config.config.safe_get(sections.RESCONTROL,options.CASSANDRA_KEYSPACE)
        self.params['cassandra_cluster'] = config.config.safe_get(sections.RESCONTROL,options.CASSANDRA_CLUSTER).split(',')
        self.params['broker'] = config.config.safe_get(sections.RESCONTROL, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = config.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        if logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            logger.logger.info('Rescontrol module started')
        if not self.params['cassandra_keyspace'] or not self.params['cassandra_cluster']:
            logger.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            logger.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            casscon.initialize_session(self.params['cassandra_cluster'],self.params['cassandra_keyspace'])
            msgbus.initialize_msgbus(self.params['broker'], self.name, self.instance_number, self.hostname)
            self.__loop()
        logger.logger.info('Rescontrol module exiting')
    
    def __loop(self):
        self.quote_update_funcs={}
        self.quote_compare_funcs={}
        self.quote_deny_funcs={}
        self.resource_update_funcs={}
        while True:
            message = msgapi.retrieve_message()
            mtype = message.type
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                msgapi.process_msg_result(msgresult)
            except AttributeError:
                logger.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                logger.logger.exception('Exception processing message: '+str(e))

    def process_msg_UPDQUO(self, message):
        msgresult=messages.MessageResult(message)
        quotes_to_update=list(message.operation.get_quotes_to_update())
        opparams=message.operation.get_params()
        for quote in quotes_to_update:
            logger.logger.debug('Inicio de proceso de quota: '+quote)
            try:
                qvalue=self.quote_update_funcs[quote](params=opparams)
            except KeyError:
                try:
                    self.quote_update_funcs[quote]=getattr(quoup,'update_'+quote)
                    self.quote_compare_funcs[quote]=getattr(quocmp,'compare_'+quote)
                    self.quote_deny_funcs[quote]=getattr(quodeny,'deny_'+quote)
                    quotes_to_update.append(quote)
                except Exception as e:
                    logger.logger.exception('Exception getting quote funcions: '+quote+' '+str(e))
                    msgresult.retcode=msgcodes.ERROR
            except Exception as e:
                logger.logger.exception('Exception in quote update function: '+quote+' '+str(e))
                msgresult.retcode=msgcodes.ERROR
            else:
                if qvalue is not None:
                    ''' quote updated successfully, the return value is the quota value updated'''
                    ''' now determine if quota is aproaching limits and should block interface'''
                    try:
                        should_block=self.quote_compare_funcs[quote](params=opparams)
                        deny=True if should_block else False
                        if self.quote_deny_funcs[quote](params=opparams,deny=deny):
                            msgresult.retcode=msgcodes.SUCCESS
                    except Exception as e:
                        logger.logger.exception('Exception evaluating quote denial: '+quote+' '+str(e))
                        msgresult.retcode=msgcodes.ERROR
                else:
                    logger.logger.error('Error updating quote: '+quote)
                    msgresult.retcode=msgcodes.ERROR
        return msgresult

    def process_msg_RESAUTH(self, message):
        msgresult=messages.MessageResult(message)
        auths_to_update=list(message.operation.get_auths_to_update())
        opparams=message.operation.get_params()
        for auth in auths_to_update:
            logger.logger.debug('Resource authorization update begins: '+auth)
            try:
                avalue=self.resource_update_funcs[auth](params=opparams)
            except KeyError:
                try:
                    self.resource_update_funcs[auth]=getattr(resup,'update_'+auth)
                    auths_to_update.append(auth)
                except Exception as e:
                    logger.logger.exception('Exception getting authorization functions: '+auth+' '+str(e))
                    msgresult.retcode=msgcodes.ERROR
            except Exception as e:
                logger.logger.exception('Exception in authorization update function: '+auth+' '+str(e))
                msgresult.retcode=msgcodes.ERROR
            else:
                if avalue:
                    ''' auth updated successfully'''
                    msgresult.retcode=msgcodes.SUCCESS
                else:
                    logger.logger.error('Error updating authorization: '+auth)
                    msgresult.retcode=msgcodes.ERROR
        return msgresult


