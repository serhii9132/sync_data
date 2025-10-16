### Usage
1.Create a .env file in the root of the project with the following content:
```
#### UUIDs of external drives
UUID_VOL_EXT_DRIVE_1=AAAAACC1
UUID_VOL_EXT_DRIVE_2=AAAAACC2
UUID_VOL_EXT_DRIVE_3=AAAAACC3

NAME_TARGET_DIR=target_dir

#### UUIDs and the list of synchronized folders from the source disks
UUID_VOL_SRC_DRIVE_1=AAAAACC4
LIST_DIRS_SRC_DRIVE_1=dir1,dir2,dir3

UUID_VOL_SRC_DRIVE_2=AAAAACC5
LIST_DIRS_SRC_DRIVE_2=dir1,dir2,dir3
```

2. Run python main.py (-a | -n). Use the -h option to view more detailed information about the launch parameters.

### Python dependencies:
- WMI
- python-dotenv