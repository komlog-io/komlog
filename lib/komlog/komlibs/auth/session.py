'''

methods for managing web sessions

'''

from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.validation import arguments as args
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import agent as ormagent
from komlog.komimc import bus as msgbus

def get_agent_session_info(sid):
    ''' returns the agent session information '''
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_AS_GASI_ISID)
    session=cassapiagent.get_agent_session(sid=sid)
    if session is None:
        raise exceptions.SessionNotFoundException(error=Errors.E_AS_GASI_SNF)
    return session

def set_agent_session(sid, aid, uid, pv):
    ''' associate the session id to the current imc_address of the running process '''
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_AS_SAGS_ISID)
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_AS_SAGS_IAID)
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_AS_SAGS_IUID)
    if not args.is_valid_int(pv):
        raise exceptions.BadParametersException(error=Errors.E_AS_SAGS_IPV)
    if msgbus.msgbus.imc_address is None:
        raise exceptions.BadParametersException(error=Errors.E_AS_SAGS_IMCNC)
    session=ormagent.AgentSession(
        sid=sid,
        aid=aid,
        uid=uid,
        pv=pv,
        imc_address=msgbus.msgbus.imc_address,
        last_update=timeuuid.uuid1()
    )
    return cassapiagent.insert_agent_session(session)

def unset_agent_session(sid, last_update=None):
    ''' dissociates aid from sid, indicating the session is orphaned, because the session
        is not found in the module with imc_address.
        last_update indicates to delete the session if last_update field is less or equal than it.
        This is to implement lightweight transactions and try to avoid race conditions.'''
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_AS_USAGS_ISID)
    if last_update and not args.is_valid_date(last_update):
        raise exceptions.BadParametersException(error=Errors.E_AS_USAGS_ILU)
    session=ormagent.AgentSession(
        sid=sid,
        aid=None,
        uid=None,
        pv=None,
        imc_address=None,
        last_update=timeuuid.uuid1()
    )
    if last_update:
        return cassapiagent.update_agent_session_if_last_update(session,last_update)
    else:
        return cassapiagent.insert_agent_session(session)

def delete_agent_session(sid, last_update=None):
    ''' delete the session id from the current active agent sessions.
        last_update indicate to delete the session if last_update field is less or equal than.
        This is to implement lightweight transactions and try to avoid race conditions.'''
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_AS_DAGS_ISID)
    if last_update and not args.is_valid_date(last_update):
        raise exceptions.BadParametersException(error=Errors.E_AS_DAGS_ILU)
    if last_update:
        return cassapiagent.delete_agent_session_if_last_update(sid=sid, last_update=last_update)
    else:
        return cassapiagent.delete_agent_session(sid=sid)

