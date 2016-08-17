import time
from komlog.komfig import logging
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.model import relations
from komlog.komlibs.auth.quotes import update as quoup
from komlog.komlibs.auth.quotes import compare as quocmp
from komlog.komlibs.auth.resources import update as resup


def update_quotes(operation, params):
    quotes=relations.operation_quotes[operation]
    num_updates=len(quotes)
    failures=False
    for quo in quotes:
        try:
            now=time.time()
            f=quoup.quote_funcs[quo]
            result=f(params=params)
            if result is not None:
                f=quocmp.quote_funcs[quo]
                f(params=params)
        except exceptions.AuthException as e:
            end=time.time()
            failures=True
            fn=f.__module__+'.'+f.__qualname__
            logging.c_logger.info(','.join((fn,e.error.name,str(now),str(end))))
    return False if failures else True

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

