import os
from typing import Dict

def load_backup_profile() -> Dict[str, any]:
    """
    Loads the backup profile from environment variables.

    Searches for necessary environment variables to define the target directory 
    and the list of source drives/directories for synchronization. 
    The environment variable names for source drives/directories must 
    follow the format: UUID_VOL_SRC_DRIVE_N and LIST_DIRS_SRC_DRIVE_N.

    Environment Variables:
    - NAME_TARGET_DIR: The name of the target directory for the backup.
    - UUID_VOL_SRC_DRIVE_N: The UUID of the source volume (drive) N.
    - LIST_DIRS_SRC_DRIVE_N: A comma-separated list of directories to synchronize 
      on source volume N.

    :raises ValueError: If NAME_TARGET_DIR is not set, or if LIST_DIRS_SRC_DRIVE_N 
                        is missing for a configured drive UUID, or if no backup 
                        drives are configured.
    :returns: A Dictionary (Dict) containing the backup profile:
              - 'name_target_dir' (str): The name of the target directory.
              - 'drives' (list): A list of dictionaries, each describing a 
                source drive:
                - 'uuid' (str): The UUID of the source volume.
                - 'sync_dirs' (list[str]): The list of directories to synchronize.
                
    ### Expected Output
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
    """ 
    name_target_dir = os.getenv('NAME_TARGET_DIR')
    if not name_target_dir:
        raise ValueError("NAME_TARGET_DIR is required in .env")
    
    drives = []
    i = 1
    
    while True:
        uuid = os.getenv(f'UUID_VOL_SRC_DRIVE_{i}')
        dirs_str = os.getenv(f'LIST_DIRS_SRC_DRIVE_{i}')
        
        if not uuid:
            break
            
        if not dirs_str:
            raise ValueError(f"LIST_DIRS_SRC_DRIVE_{i} is required for UUID {uuid}")
        
        drives.append({
            'uuid': uuid.strip(),
            'sync_dirs': [d.strip() for d in dirs_str.split(',') if d.strip()]
        })
        i += 1
    
    if not drives:
        raise ValueError("No backup drives configured")
    
    return {
        'name_target_dir': name_target_dir,
        'drives': drives
    }