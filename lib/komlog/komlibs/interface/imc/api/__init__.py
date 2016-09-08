MESSAGE_MODULES = ['textmining','gestconsole','rescontrol','events','lambdas']

import sys
from komlog.komfig import logging

message_funcs={}

def process_message(message):
    try:
        return message_funcs[message._type_.value](message=message)
    except KeyError:
        logging.logger.debug('Loading message processing function: '+message._type_.value)
        for module in MESSAGE_MODULES:
            try:
                message_funcs[message._type_.value]=getattr(sys.modules['komlog.komlibs.interface.imc.api.'+module],'process_message_'+message._type_.value)
                return message_funcs[message._type_.value](message=message)
            except KeyError as e:
                logging.logger.debug('Loading module to obtain function: '+str(e))
                __import__('komlog.komlibs.interface.imc.api.'+module)
                try:
                    message_funcs[message._type_.value]=getattr(sys.modules['komlog.komlibs.interface.imc.api.'+module],'process_message_'+message._type_.value)
                    return message_funcs[message._type_.value](message=message)
                except AttributeError as e:
                    logging.logger.debug('Error getting function from loaded module '+module+': '+str(e))
            except AttributeError as e:
                logging.logger.debug('Error getting function from module '+module+': '+str(e))
        return None

