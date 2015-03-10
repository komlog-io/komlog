from komfig import logger
from komlibs.auth.quotes import update as quoup
from komlibs.auth.quotes import compare as quocmp
from komlibs.auth.quotes import deny as quodeny
from komlibs.auth.resources import update as resup
from komlibs.auth.shared import update as sharedup

quote_update_funcs={}
quote_compare_funcs={}
quote_deny_funcs={}
resource_update_funcs={}
shared_update_funcs={}

def update_quotes(operation, params):
    update_funcs=quoup.get_update_funcs(operation=operation)
    if update_funcs==[]:
        return True
    num_updates=len(update_funcs)
    num_success=0
    for update_func in update_funcs:
        qvalue=None
        try:
            qvalue=quote_update_funcs[update_func](params=params)
        except KeyError:
            try:
                quote_update_funcs[update_func]=getattr(quoup,update_func)
                quote_compare_funcs[update_func]=getattr(quocmp,update_func)
                quote_deny_funcs[update_func]=getattr(quodeny,update_func)
                qvalue=quote_update_funcs[update_func](params=params)
            except Exception as e:
                logger.logger.exception('Exception getting quote funcions: '+update_func+' '+str(e))
        except Exception as e:
            logger.logger.exception('Exception in quote update function: '+update_func+' '+str(e))
        if qvalue is not None:
            ''' quote updated successfully, the return value is the quota value updated'''
            ''' now determine if quota is aproaching limits and should block interface'''
            try:
                should_block=quote_compare_funcs[update_func](params=params)
                deny=True if should_block else False
                if quote_deny_funcs[update_func](params=params,deny=deny):
                    num_success+=1
            except Exception as e:
                logger.logger.exception('Exception evaluating quote denial: '+update_func+' '+str(e))
        else:
            logger.logger.error('Error updating quote: '+update_func)
    if num_success==num_updates:
        return True
    else:
        return False

def update_resources(operation, params):
    update_funcs=resup.get_update_funcs(operation=operation)
    if update_funcs==[]:
        return True
    num_updates=len(update_funcs)
    num_success=0
    for update_func in update_funcs:
        avalue=False
        try:
            avalue=resource_update_funcs[update_func](params=params)
        except KeyError:
            try:
                resource_update_funcs[update_func]=getattr(resup,update_func)
                avalue=resource_update_funcs[update_func](params=params)
            except Exception as e:
                logger.logger.exception('Exception getting authorization functions: '+update_func+' '+str(e))
        except Exception as e:
            logger.logger.exception('Exception in authorization update function: '+update_func+' '+str(e))
        if avalue:
            ''' auth updated successfully'''
            num_success+=1
        else:
            logger.logger.error('Error updating authorization: '+update_func+' '+str(params))
    if num_success==num_updates:
        return True
    else:
        return False

def update_shared(operation, params):
    update_funcs=sharedup.get_update_funcs(operation=operation)
    if update_funcs==[]:
        return True
    num_updates=len(update_funcs)
    num_success=0
    for update_func in update_funcs:
        avalue=False
        try:
            avalue=shared_update_funcs[update_func](params=params)
        except KeyError:
            try:
                shared_update_funcs[update_func]=getattr(sharedup,update_func)
                avalue=shared_update_funcs[update_func](params=params)
            except Exception as e:
                logger.logger.exception('Exception getting authorization functions: '+update_func+' '+str(e))
        except Exception as e:
            logger.logger.exception('Exception in authorization update function: '+update_func+' '+str(e))
        if avalue:
            ''' auth updated successfully'''
            num_success+=1
        else:
            logger.logger.error('Error updating authorization: '+update_func+' '+str(params))
    if num_success==num_updates:
        return True
    else:
        return False

