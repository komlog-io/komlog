#coding:utf-8
'''

Resource Control message definitions

'''

from komfig import logger
from komlibs.auth.quotes import update as quoup
from komlibs.auth.quotes import compare as quocmp
from komlibs.auth.quotes import deny as quodeny
from komlibs.auth.resources import update as resup
from komimc import messages
from komimc import codes as msgcodes

quote_update_funcs={}
quote_compare_funcs={}
quote_deny_funcs={}
resource_update_funcs={}

def process_message_UPDQUO(message):
    msgresult=messages.MessageResult(message)
    quotes_to_update=list(message.operation.get_quotes_to_update())
    opparams=message.operation.get_params()
    for quote in quotes_to_update:
        logger.logger.debug('Inicio de proceso de quota: '+quote)
        try:
            qvalue=quote_update_funcs[quote](params=opparams)
        except KeyError:
            try:
                quote_update_funcs[quote]=getattr(quoup,'update_'+quote)
                quote_compare_funcs[quote]=getattr(quocmp,'compare_'+quote)
                quote_deny_funcs[quote]=getattr(quodeny,'deny_'+quote)
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
                    should_block=quote_compare_funcs[quote](params=opparams)
                    deny=True if should_block else False
                    if quote_deny_funcs[quote](params=opparams,deny=deny):
                        msgresult.retcode=msgcodes.SUCCESS
                except Exception as e:
                    logger.logger.exception('Exception evaluating quote denial: '+quote+' '+str(e))
                    msgresult.retcode=msgcodes.ERROR
            else:
                logger.logger.error('Error updating quote: '+quote)
                msgresult.retcode=msgcodes.ERROR
    return msgresult

def process_message_RESAUTH(message):
    msgresult=messages.MessageResult(message)
    auths_to_update=list(message.operation.get_auths_to_update())
    opparams=message.operation.get_params()
    for auth in auths_to_update:
        logger.logger.debug('Resource authorization update begins: '+auth)
        try:
            avalue=resource_update_funcs[auth](params=opparams)
        except KeyError:
            try:
                resource_update_funcs[auth]=getattr(resup,'update_'+auth)
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


