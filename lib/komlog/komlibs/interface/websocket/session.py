'''

this file implements methods for managing agent sessions
from the websocket interface

'''

import time
import traceback
from komlog.komfig import logging
from komlog.komlibs.auth import session
from komlog.komlibs.auth.passport import AgentPassport
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors as errorsv1

agent_callback={}

def set_session(passport, callback):
    try:
        if isinstance(passport, AgentPassport) and session.set_agent_session(sid=passport.sid, aid=passport.aid, uid=passport.uid, pv=passport.pv):
            agent_callback[passport.sid]=callback
            return True
        return False
    except Exception as e:
        t=time.time()
        ex_info=traceback.format_exc().splitlines()
        for line in ex_info:
            logging.logger.error(line)
        error=getattr(e,'error',errorsv1.UNKNOWN)
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.session.set_session',error.name,str(t),str(t))))
        return False

def unset_session(passport):
    try:
        if isinstance(passport, AgentPassport) and session.unset_agent_session(passport.sid):
            agent_callback.pop(passport.sid,None)
            return True
        return False
    except Exception as e:
        t=time.time()
        ex_info=traceback.format_exc().splitlines()
        for line in ex_info:
            logging.logger.error(line)
        error=getattr(e,'error',errorsv1.UNKNOWN)
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.session.unset_session',error.name,str(t),str(t))))
        return False

