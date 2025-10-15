import sys
import wmi
from typing import Dict
from . import constants, path_util

def get_mnt_point(uuid: str) -> str | None:
    try:
        c = wmi.WMI()

        for drive in c.Win32_LogicalDisk():
            if drive.VolumeSerialNumber and drive.VolumeSerialNumber == uuid:
                return path_util.conv_path_win_to_unix(drive.DeviceID)
            
        return None
    except Exception as e:
        sys.exit(f'An error occurred: {e}')

def update_backup_profile() -> Dict[str, any]:
    backup_profile = constants.BACKUP_PROFILE
    mnt_point = ''
    curr_uuid = ''

    for drive in backup_profile.get('drives'):
        curr_uuid = drive.get('uuid')
        mnt_point = get_mnt_point(curr_uuid)

        if mnt_point is not None:
            drive['mnt_point'] = mnt_point
        else:
            sys.exit(f'The source disk with UUID {curr_uuid} was not found or is not mounted')

    return backup_profile

def get_mnt_point_dest() -> Dict[str, str]:
    list_uuids = [
        constants.UUID_VOL_EXT_DRIVE_1,
        constants.UUID_VOL_EXT_DRIVE_2,
        constants.UUID_VOL_EXT_DRIVE_3
    ]

    mnt = {}

    for uuid in list_uuids:
        mnt = get_mnt_point(uuid)
        if mnt is not None:
            return {
                'uuid' : uuid,
                'mnt_point': mnt
            }

    sys.exit("UUID not found in connected drives.")