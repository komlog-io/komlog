from komfig import logger
from komlibs.auth.quotes import update as quoup
from komlibs.auth.quotes import compare as quocmp
from komlibs.auth.quotes import deny as quodeny
from komlibs.auth.resources import update as resup

quote_update_funcs={}
quote_compare_funcs={}
quote_deny_funcs={}
resource_update_funcs={}

def update_quote(quote, params):
    try:
        qvalue=quote_update_funcs[quote](params=params)
    except KeyError:
        try:
            quote_update_funcs[quote]=getattr(quoup,'update_'+quote)
            quote_compare_funcs[quote]=getattr(quocmp,'compare_'+quote)
            quote_deny_funcs[quote]=getattr(quodeny,'deny_'+quote)
            return update_quote(quote, params)
        except Exception as e:
            logger.logger.exception('Exception getting quote funcions: '+quote+' '+str(e))
            return False
    except Exception as e:
        logger.logger.exception('Exception in quote update function: '+quote+' '+str(e))
        return False
    else:
        if qvalue is not None:
            ''' quote updated successfully, the return value is the quota value updated'''
            ''' now determine if quota is aproaching limits and should block interface'''
            try:
                should_block=quote_compare_funcs[quote](params=params)
                deny=True if should_block else False
                if quote_deny_funcs[quote](params=params,deny=deny):
                    return True
            except Exception as e:
                logger.logger.exception('Exception evaluating quote denial: '+quote+' '+str(e))
                return False
        else:
            logger.logger.error('Error updating quote: '+quote)
            return False

def update_resource_auth(auth, params):
    try:
        avalue=resource_update_funcs[auth](params=params)
    except KeyError:
        try:
            resource_update_funcs[auth]=getattr(resup,'update_'+auth)
            return update_resource_auth(auth, params)
        except Exception as e:
            logger.logger.exception('Exception getting authorization functions: '+auth+' '+str(e))
            return False
    except Exception as e:
        logger.logger.exception('Exception in authorization update function: '+auth+' '+str(e))
        return False
    else:
        if avalue:
            ''' auth updated successfully'''
            return True
        else:
            logger.logger.error('Error updating authorization: '+auth+' '+str(params))
            return False


