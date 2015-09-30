'''

this file implements method for ticket authorization

'''

import uuid
from komcass.api import ticket as ticketapi
from komcass.api import circle as circleapi
from komcass.model.orm import ticket as ormticket
from komlibs.auth import exceptions, errors, permissions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komfig import logger

def authorize_get_datasource_data(uid, tid, did, ii, ie):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDSD_IUID)
    if not args.is_valid_uuid(tid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDSD_ITID)
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDSD_IDID)
    if not args.is_valid_date(ii):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDSD_III)
    if not args.is_valid_date(ie):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDSD_IIE)
    now=timeuuid.uuid1()
    ticket=ticketapi.get_ticket(tid=tid)
    if not ticket:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDSD_TNF)
    if timeuuid.get_unix_timestamp(ticket.expires)<timeuuid.get_unix_timestamp(now):
        ticketapi.insert_expired_ticket(ticket=ticket)
        ticketapi.delete_ticket(tid=ticket.tid)
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDSD_EXPT)
    if not uid in ticket.allowed_uids:
        uid_in_circles=False
        sharing_user_circles=circleapi.get_circles(uid=ticket.uid)
        for circle in sharing_user_circles:
            if uid in circle.members:
                uid_in_circles=True
                break;
        if not uid_in_circles:
            raise exceptions.AuthorizationException(error=errors.E_ATA_AGDSD_UNA)
    if not did in ticket.resources:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDSD_DNA)
    permissions_needed=permissions.CAN_READ_DATA
    if did in ticket.permissions and permissions_needed & ticket.permissions[did]:
        if ii>=ticket.interval_init and ii<=ticket.interval_end and ie>= ticket.interval_init and ie<=ticket.interval_end:
            return True
        else:
            raise exceptions.AuthorizationException(error=errors.E_ATA_AGDSD_IINT)
    else:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDSD_INSP)

def authorize_get_datapoint_data(uid, tid, pid, ii, ie):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDPD_IUID)
    if not args.is_valid_uuid(tid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDPD_ITID)
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDPD_IPID)
    if not args.is_valid_date(ii):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDPD_III)
    if not args.is_valid_date(ie):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGDPD_IIE)
    now=timeuuid.uuid1()
    ticket=ticketapi.get_ticket(tid=tid)
    if not ticket:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDPD_TNF)
    if timeuuid.get_unix_timestamp(ticket.expires)<timeuuid.get_unix_timestamp(now):
        ticketapi.insert_expired_ticket(ticket=ticket)
        ticketapi.delete_ticket(tid=ticket.tid)
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDPD_EXPT)
    if not uid in ticket.allowed_uids:
        uid_in_circles=False
        sharing_user_circles=circleapi.get_circles(uid=ticket.uid)
        for circle in sharing_user_circles:
            if uid in circle.members:
                uid_in_circles=True
                break;
        if not uid_in_circles:
            raise exceptions.AuthorizationException(error=errors.E_ATA_AGDPD_UNA)
    if not pid in ticket.resources:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDPD_DNA)
    permissions_needed=permissions.CAN_READ_DATA
    if pid in ticket.permissions and permissions_needed & ticket.permissions[pid]:
        if ii>=ticket.interval_init and ii<=ticket.interval_end and ie>=ticket.interval_init and ie<=ticket.interval_end:
            return True
        else:
            raise exceptions.AuthorizationException(error=errors.E_ATA_AGDPD_IINT)
    else:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGDPD_INSP)

def authorize_get_snapshot_config(uid, tid, nid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGSNC_IUID)
    if not args.is_valid_uuid(tid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGSNC_ITID)
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_ATA_AGSNC_INID)
    now=timeuuid.uuid1()
    ticket=ticketapi.get_ticket(tid=tid)
    if not ticket:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGSNC_TNF)
    if timeuuid.get_unix_timestamp(ticket.expires)<timeuuid.get_unix_timestamp(now):
        ticketapi.insert_expired_ticket(ticket=ticket)
        ticketapi.delete_ticket(tid=ticket.tid)
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGSNC_EXPT)
    if not uid in ticket.allowed_uids:
        uid_in_circles=False
        sharing_user_circles=circleapi.get_circles(uid=ticket.uid)
        for circle in sharing_user_circles:
            if uid in circle.members:
                uid_in_circles=True
                break;
        if not uid_in_circles:
            raise exceptions.AuthorizationException(error=errors.E_ATA_AGSNC_UNA)
    if not nid in ticket.resources:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGSNC_DNA)
    permissions_needed=permissions.CAN_READ_CONFIG
    if nid in ticket.permissions and permissions_needed & ticket.permissions[nid]:
        return True
    else:
        raise exceptions.AuthorizationException(error=errors.E_ATA_AGSNC_INSP)

