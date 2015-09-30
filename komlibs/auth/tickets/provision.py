'''

this file implements method for creating and provisioning tickets

'''

import uuid
from komcass.api import ticket as ticketapi
from komcass.api import snapshot as snapshotapi
from komcass.model.orm import ticket as ormticket
from komcass.model.orm import snapshot as ormsnapshot
from komlibs.auth import exceptions, errors
from komlibs.auth.tickets.types import permission, share
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komfig import logger

def new_snapshot_ticket(uid, nid, expires=False, share_type=None):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_ATP_NST_IUID)
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_ATP_NST_INID)
    if expires and not args.is_valid_date(expires):
        raise exceptions.BadParametersException(error=errors.E_ATP_NST_IEXP)
    if share_type and (not args.is_valid_int(share_type) or not share_type in share.NEW_SNAPSHOT_OPTIONS_AVAILABLE_TO_USER):
        raise exceptions.BadParametersException(error=errors.E_ATP_NST_ISHT)
    snapshot=snapshotapi.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.TicketCreationException(error=errors.E_ATP_NST_SNF)
    tid=uuid.uuid4()
    date=timeuuid.uuid1()
    resources=set()
    permissions=dict()
    expires=expires if expires else timeuuid.HIGHEST_TIME_UUID
    share_type=share_type if share_type else share.NEW_SNAPSHOT_DEFAULT_SHARE_TYPE
    resources.add(nid)
    permissions[nid]=permission.NEW_SNAPSHOT_TICKET_NID_PERMISSIONS[share_type]
    if isinstance(snapshot, ormsnapshot.SnapshotDs):
        resources.add(snapshot.did)
        permissions[snapshot.did]=permission.NEW_SNAPSHOT_TICKET_DID_PERMISSIONS[share_type]
    elif isinstance(snapshot, ormsnapshot.SnapshotDp):
        resources.add(snapshot.pid)
        permissions[snapshot.pid]=permission.NEW_SNAPSHOT_TICKET_PID_PERMISSIONS[share_type]
    elif isinstance(snapshot, ormsnapshot.SnapshotMultidp) \
      or isinstance(snapshot, ormsnapshot.SnapshotHistogram) \
      or isinstance(snapshot, ormsnapshot.SnapshotLinegraph) \
      or isinstance(snapshot, ormsnapshot.SnapshotTable):
        for pid in snapshot.datapoints:
            resources.add(pid)
            permissions[pid]=permission.NEW_SNAPSHOT_TICKET_PID_PERMISSIONS[share_type]
    else:
        raise exceptions.TicketCreationException(error=errors.E_ATP_NST_USTF)
    allowed_uids=set()
    allowed_cids=set()
    for user_id in snapshot.shared_with_uids:
        allowed_uids.add(user_id)
    for circle_id in snapshot.shared_with_cids:
        allowed_cids.add(circle_id)
    interval_init=snapshot.interval_init
    interval_end=snapshot.interval_end
    ticket=ormticket.Ticket(tid=tid, date=date, uid=uid, expires=expires, allowed_uids=allowed_uids, allowed_cids=allowed_cids, resources=resources, permissions=permissions, interval_init=interval_init, interval_end=interval_end)
    if ticketapi.insert_ticket(ticket=ticket):
        return {'tid':tid}
    else:
        raise exceptions.TicketCreationException(error=errors.E_ATP_NST_EIDB)

