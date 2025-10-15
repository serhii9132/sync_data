import os
from typing import Dict

def load_backup_profile() -> Dict[str, any]:    
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