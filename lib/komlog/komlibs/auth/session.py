'''

methods for managing web sessions

'''

from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import agent as ormagent
from komlog.komimc import bus as msgbus


def set_agent_session(sid, aid, uid):
    ''' associate the session id to the current imc_address of the running process '''
    if msgbus.msgbus.imc_address is None:
        return False
    session=ormagent.AgentSession(
        sid=sid,
        aid=aid,
        uid=uid,
        imc_address=msgbus.msgbus.imc_address,
        generated=timeuuid.uuid1()
    )
    return cassapiagent.insert_agent_session(session)

def unset_agent_session(sid):
    ''' delete the session id from the current active agent sessions '''
    return cassapiagent.delete_agent_session(sid=sid)

