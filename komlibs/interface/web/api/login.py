#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

from komfig import logger
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def login_request(username, password, agentid, signature):
    if args.is_valid_username(username) and args.is_valid_password(password):
        if agentid and (not args.is_valid_hex_uuid(agentid) or not args.is_valid_pubkey(signature)):
            logger.logger.debug('Not valid agentid or signature')
            logger.logger.debug(str(agentid))
            logger.logger.debug(str(signature))
            raise exceptions.BadParametersException()
        else:
            logger.logger.debug('authenthicating User...')
            if not userapi.auth_user(username=username, password=password):
                logger.logger.debug('User authenthication error')
                return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED)
            if agentid:
                logger.logger.debug('authenthicating agent...')
                if not agentapi.auth_agent(agentid=agentid, signature=signature):
                    logger.logger.debug('agent authenthication error')
                    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED)
            logger.logger.debug('Authentication successfull')
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

