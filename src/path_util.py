import subprocess

def conv_path_win_to_unix(windows_path: str) -> str:
    s = subprocess.run(['cygpath', '--unix', windows_path], capture_output=True, text=True)
    return s.stdout.strip('\n')