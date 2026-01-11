import subprocess
import posixpath
import datetime
import sys
from typing import Dict, List
from src import constants

def conv_path_win_to_unix(windows_path: str) -> str:
    s = subprocess.run(['cygpath', '--unix', windows_path], capture_output=True, text=True)
    return s.stdout.strip('\n')

def get_sync_dirs(backup_profile: Dict[str, any]) -> List[str]:
    """
    Constructs the complete list of source directories for synchronization 
    by combining the mount point (mnt_point) of each drive with its 
    relative synchronization directories (sync_dirs).

    It uses posixpath.join to create paths in a Unix/POSIX-compatible format 
    (even if operating on Windows), ensuring the correct joining of the mount 
    point (e.g., /f) and the relative directory (e.g., test1).

    :param backup_profile: The Dictionary (Dict) of the backup profile, 
                           which must contain the 'drives' key. 
                           Each element in 'drives' must contain 'mnt_point' 
                           and 'sync_dirs' keys.
    :type backup_profile: Dict[str, Any]
    :returns: A List of the full paths to the directories that need 
              to be synchronized.
    :rtype: List[str]

    ## Example

    ### Input Data (backup_profile)
    ```python
    {
        'name_target_dir': 'test_target_dir', 
        'drives': [
            {
                'uuid': '9CD33173', 
                'sync_dirs': ['test1', 'test2', 'test3', 'vm'], 
                'mnt_point': '/f'
            }, 
            {
                'uuid': '0AE6398F', 
                'sync_dirs': ['test4', 'test5', 'test6'], 
                'mnt_point': '/g'
            }
        ]
    }
    ```

    ### Expected Output
    ```python
    ['/f/test1', '/f/test2', '/f/test3', '/f/vm', '/g/test4', '/g/test5', '/g/test6']
    ```
    """
    sync_dirs = []
    for drive in backup_profile['drives']:
        mnt_point = drive['mnt_point']
        rel_path_dirs = drive.get('sync_dirs')

        for item in rel_path_dirs:
            sync_dirs.append(posixpath.join(mnt_point, item))

    return sync_dirs

def get_log_paths(log_dir: str, uuid_vol: str) -> Dict[str, str]:
    """
    Creates the necessary log directories and generates the full paths 
    to the "dry-run" and "upload" log files based on the current timestamp 
    and a drive label.

    First, it creates the log directory using 'mkdir -p' (if it doesn't already exist), 
    then generates a timestamp and returns a dictionary with the full log file paths.

    :param log_dir: The base directory where log files will be stored.
    :type log_dir: str
    :param drive_label: A unique label (e.g., UUID or drive letter) 
                        that will be included in the log file name to identify 
                        the associated source drive.
    :type drive_label: str
    :returns: A Dictionary (Dict) containing the full POSIX paths to the two log files.
              - "dry_run" (str): The path to the dry-run log file.
              - "upload" (str): The path to the actual synchronization log file.
    :rtype: Dict[str, str]

    ## Example

    ### Assumed Input
    - log_dir = '/c/app_data/log/backup/'
    - drive_label = 'DCF97D17' (UUID)

    ### Expected Output
    ```python
    {
        'path_log_file_dry_run_mode': '/c/app_data/log/backup/1970-01-01_10-00-00_DCF97D17_DRY_RUN.log',
        'path_log_file_upload_mode': '/c/app_data/log/backup/1970-01-01_10-00-00_DCF97D17_UPLOAD.log'
    }
    ```
    """
    # Creating a subdirectory hierarchy in UNIX style
    subprocess.run(['mkdir', '-p', constants.PATH_LOG_DIR], stderr=sys.stderr, stdout=sys.stdout)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return {
        "dry_run": posixpath.join(log_dir, f"{timestamp}_{uuid_vol}_DRY_RUN.log"),
        "upload": posixpath.join(log_dir, f"{timestamp}_{uuid_vol}_UPLOAD.log"),
    }