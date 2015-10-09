'''

This files defines the posible permissions applied to resources when creating tickets
Permissions depend on how the object was created by the user (the share type used)


'''

from komlibs.auth.tickets.types import share
from komlibs.auth import permissions

NEW_SNAPSHOT_TICKET_DID_PERMISSIONS={
    share.NEW_SNAPSHOT_SHARE_READ_ONLY:permissions.CAN_READ_DATA,
    share.NEW_SNAPSHOT_SHARE_READ_AND_SHARE:permissions.CAN_READ_DATA,
}

NEW_SNAPSHOT_TICKET_PID_PERMISSIONS={
    share.NEW_SNAPSHOT_SHARE_READ_ONLY:permissions.CAN_READ_DATA,
    share.NEW_SNAPSHOT_SHARE_READ_AND_SHARE:permissions.CAN_READ_DATA,
}

NEW_SNAPSHOT_TICKET_NID_PERMISSIONS={
    share.NEW_SNAPSHOT_SHARE_READ_ONLY:permissions.CAN_READ_CONFIG,
    share.NEW_SNAPSHOT_SHARE_READ_AND_SHARE:permissions.CAN_READ_CONFIG|permissions.CAN_SNAPSHOT,
}

