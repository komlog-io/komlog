MESSAGE_MODULES = ['validation','storing','textmining','gestconsole','rescontrol','events']

import sys
from komfig import logger

message_funcs={}

def process_message(message):
    try:
        return message_funcs[message.type](message=message)
    except KeyError:
        logger.logger.debug('Loading message processing function: '+message.type)
        for module in MESSAGE_MODULES:
            try:
                message_funcs[message.type]=getattr(sys.modules['komlibs.interface.imc.api.'+module],'process_message_'+message.type)
                return message_funcs[message.type](message=message)
            except KeyError as e:
                logger.logger.debug('Loading module to obtain function: '+str(e))
                __import__('komlibs.interface.imc.api.'+module)
                try:
                    message_funcs[message.type]=getattr(sys.modules['komlibs.interface.imc.api.'+module],'process_message_'+message.type)
                    return message_funcs[message.type](message=message)
                except AttributeError as e:
                    logger.logger.debug('Error getting function from loaded module '+module+': '+str(e))
            except AttributeError as e:
                logger.logger.debug('Error getting function from module '+module+': '+str(e))
        return None

