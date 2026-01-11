import sys
import wmi
from typing import Dict
from . import constants, path_util

def get_mnt_point(uuid: str) -> str | None:
    """
    Retrieves the mount point (drive letter) for a volume with the specified UUID 
    (Volume Serial Number) in a Windows system.

    :returns: The mount point in Unix format (after conversion) 
              (e.g., '/mnt/c') as a string, if the drive is found. 
              Returns None if the drive is not found.
    """
    try:
        c = wmi.WMI()

        for drive in c.Win32_LogicalDisk():
            if drive.VolumeSerialNumber and drive.VolumeSerialNumber == uuid:
                return path_util.conv_path_win_to_unix(drive.DeviceID)
            
        return None
    except Exception as e:
        sys.exit(f'An error occurred: {e}')

def update_backup_profile() -> Dict[str, any]:
    """
    Updates the backup profile by adding mount points (mnt_point) for each 
    source drive (UUID) specified in the profile.

    The function iterates through the list of source drives defined in 
    constants.BACKUP_PROFILE. For each drive, get_mnt_point() is called 
    to determine its current mount point in the system. If the drive is found, 
    the mount point is added to its dictionary entry.

    :returns: The updated Dictionary (Dict) of the backup profile. 
              Each item in the 'drives' list will be supplemented with the 'mnt_point' key.
    :rtype: Dict[str, Any]
    :raises SystemExit: If any of the source drives (UUIDs) from the profile 
                        is not found among the connected volumes.
                        
    ## Example

    ### Assumed Input (constants.BACKUP_PROFILE before update)
    Assume the system finds:
    - Drive UUID '9CD33173' is mounted at 'F:' (converted to '/f')
    - Drive UUID '0AE6398F' is mounted at 'G:' (converted to '/g')

    ```python
    {
        'name_target_dir': 'test_target_dir', 
        'drives': [
            {
                'uuid': '9CD33173', 
                'sync_dirs': ['test1', 'test2', 'vm'] 
            }, 
            {
                'uuid': '0AE6398F', 
                'sync_dirs': ['test4', 'test5']
            }
        ]
    }
    ```

    ### Expected Output (The returned updated backup_profile)
    ```python
    {
        'name_target_dir': 'test_target_dir', 
        'drives': [
            {
                'uuid': '9CD33173', 
                'sync_dirs': ['test1', 'test2', 'vm'],
                'mnt_point': '/f' 
            }, 
            {
                'uuid': '0AE6398F', 
                'sync_dirs': ['test4', 'test5'],
                'mnt_point': '/g' 
            }
        ]
    }
    ```
    """
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
    """
    The function iterates through a list of predefined UUIDs for external drives 
    (stored in constants UUID_VOL_EXT_DRIVE_1, 2, 3) and calls 
    get_mnt_point() to find the mount point. It returns the first UUID found 
    along with its corresponding mount point.

    :returns: A Dictionary (Dict) with information about the found drive:
              - 'uuid' (str): The actual UUID of the connected target drive.
              - 'mnt_point' (str): The mount point of this drive, 
                converted to Unix format (e.g., '/mnt/c').
    :rtype: Dict[str, str]
    :raises SystemExit: If none of the UUIDs specified in the constants 
                        are found among the connected drives.

    ## Example

    ### Assumed Setup
    If the function is configured to look for UUIDs: ['A1B2C3D4', 'E5F6G7H8', 'I9J0K1L2']
    And the drive with UUID 'E5F6G7H8' is currently mounted at Windows drive letter 'H:'.

    ### Expected Output
    ```python
    {
        'uuid': 'E5F6G7H8',
        'mnt_point': '/h'
    }
    ```
    """
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