import os
import posixpath
from dotenv import load_dotenv
from . import path_util, load_profile

load_dotenv()

NAME_FILE_RSYNC_EXCLUSION = 'exclude.txt'

PATH_LOG_DIR = posixpath.join(path_util.conv_path_win_to_unix(os.environ["HOME"]), 'logs', 'sync-data')

UUID_VOL_EXT_DRIVE_1=os.getenv('UUID_VOL_EXT_DRIVE_1')

UUID_VOL_EXT_DRIVE_2=os.getenv('UUID_VOL_EXT_DRIVE_2')

UUID_VOL_EXT_DRIVE_3=os.getenv('UUID_VOL_EXT_DRIVE_3')

BACKUP_PROFILE = load_profile.load_backup_profile()