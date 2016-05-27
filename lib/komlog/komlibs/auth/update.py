from komlog.komfig import logging
from komlog.komlibs.auth.model import relations
from komlog.komlibs.auth.quotes import update as quoup
from komlog.komlibs.auth.quotes import compare as quocmp
from komlog.komlibs.auth.quotes import deny as quodeny
from komlog.komlibs.auth.resources import update as resup


def update_quotes(operation, params):
    quotes=relations.operation_quotes[operation]
    num_updates=len(quotes)
    num_success=0
    for quo in quotes:
        qvalue=quoup.quote_funcs[quo](params=params)
        if qvalue is not None:
            should_block=quocmp.quote_funcs[quo](params=params)
            if should_block is not None:
                deny=True if should_block else False
                if quodeny.quote_funcs[quo](params=params,deny=deny):
                    num_success+=1
            else:
                logging.logger.error('quote compare returned None. quote: '+quo.name)
        else:
            logging.logger.error('quote update returned None. quote: '+quo.name)
    return True if num_success==num_updates else False

def update_resources(operation, params):
    update_funcs=resup.get_update_funcs(operation=operation)
    if update_funcs==[]:
        return True
    num_updates=len(update_funcs)
    num_success=0
    for update_func in update_funcs:
        result=update_func(params=params)
        if result:
            ''' auth updated successfully'''
            num_success+=1
        else:
            logging.logger.error('Error updating authorization: '+update_func+' '+str(params))
    if num_success==num_updates:
        return True
    else:
        return False

