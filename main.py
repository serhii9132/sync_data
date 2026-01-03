import os
import sys
import datetime
import posixpath
import subprocess
import argparse
from typing import Dict, List
from src import mnt, constants, path_util

def parse_args(list_sync_dirs: List[str]) -> Dict[str, any]:
    parser = argparse.ArgumentParser(description='Synchronization files between local storage and external HDD')
    group = parser.add_mutually_exclusive_group()

    for drive in list_sync_dirs:
        if 'vm' in drive:
            group.add_argument('-n', '--no_vm', action='store_true', help='Copies all files, ignoring directories which store images of virtual machines')

    group.add_argument('-a', '--all', action='store_true', help='Copies all files, which are located on the drive')
    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])
    else:
        return args

def get_sync_dirs(backup_profile: Dict[str, any]) -> List[str]:
    sync_dirs = []
    for drive in backup_profile['drives']:
        sync_dirs.extend(posixpath.join(drive['mnt_point'], d) for d in drive.get('sync_dirs', []))
    return sync_dirs

def get_log_paths(log_dir: str, drive_label: str) -> Dict[str, str]:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return {
        "dry_run": posixpath.join(log_dir, f"{timestamp}_{drive_label}_DRY_RUN.log"),
        "upload": posixpath.join(log_dir, f"{timestamp}_{drive_label}_UPLOAD.log"),
    }

def get_upload_preset(backup_profile: Dict[str, any]) -> Dict[str, any]:
    upload_preset = mnt.get_mnt_point_dest()

    subprocess.run(['mkdir', '-p', constants.PATH_LOG_DIR], stderr=sys.stderr, stdout=sys.stdout)
    log_paths = get_log_paths(constants.PATH_LOG_DIR, upload_preset.get('uuid'))

    upload_preset.update({
        "full_path_dest_dir": posixpath.join(upload_preset.get('mnt_point'), backup_profile.get('name_target_dir')),
        "path_log_file_dry_run_mode": log_paths['dry_run'],
        "path_log_file_upload_mode": log_paths['upload']
    })

    return upload_preset

def run_rsync(sync_dirs: List[str], dest_dir: str, log_file: str, dry_run: bool) -> subprocess.CompletedProcess:
    path_exception_file_rsync = posixpath.join(
        path_util.conv_path_win_to_unix(os.path.dirname(os.path.realpath(__file__))),
        constants.NAME_FILE_RSYNC_EXCLUSION
    )

    rsync_command = [
        "rsync", "--recursive", "--perms", "--times", "--group", "--owner", "--specials",
        "--human-readable", "--stats", "--progress", "--del", "--verbose",
        "--copy-links", "--out-format=%t %f %b",
        f"--exclude-from={path_exception_file_rsync}",
        f"--log-file={log_file}",
    ]

    if dry_run:
        rsync_command.insert(3, "--dry-run")

    rsync_command.extend(sync_dirs)
    rsync_command.append(dest_dir)
    
    return subprocess.run(rsync_command, stderr=sys.stderr, stdout=sys.stdout)

def execute_rsync_phase(preset: Dict[str, str], sync_dirs: List[str], dry_run: bool) -> None:
    log_file = preset.get('path_log_file_dry_run_mode') if dry_run else preset.get('path_log_file_upload_mode')
    process = run_rsync(sync_dirs, preset.get('full_path_dest_dir'), log_file, dry_run)

    if process.returncode != 0:
        phase = "dry-run" if dry_run else "upload"
        print(f"Error in {phase}\nCheck logs")
        sys.exit(1)

def main() -> None:
    backup_profile = mnt.update_backup_profile()
    list_sync_dirs = get_sync_dirs(backup_profile)
    cli_args = parse_args(list_sync_dirs)
    upload_preset = get_upload_preset(backup_profile)

    if 'no_vm' in cli_args:
        if cli_args['no_vm'] is True:
            list_sync_dirs = [item for item in list_sync_dirs if 'vm' not in item]

    execute_rsync_phase(upload_preset, list_sync_dirs, dry_run=True)
    execute_rsync_phase(upload_preset, list_sync_dirs, dry_run=False)

if __name__ == "__main__":
    main()
