import json
from pathlib import Path
import shutil
import subprocess
from typing import Optional


def get_kobo_mountpoint(label: str='KOBOeReader') -> Optional[Path]:
    has_lsblk = shutil.which('lsblk')
    find_mount_cmd = None
    if has_lsblk:  # on Linux
        find_mount_cmd = 'lsblk -f --json'
        xxx = subprocess.check_output(find_mount_cmd.split(' ')).decode('utf8')
        jj = json.loads(xxx)
        devices = [d for d in jj['blockdevices'] if d.get('label', None) == label]
        kobos = []
        for d in devices:
            # older lsblk outputs single mountpoint..
            mp = d.get('mountpoint')
            if mp is not None:
                kobos.append(mp)
            mps = d.get('mountpoints')
            if mps is not None:
                kobos.extend(mps)
    else:
        find_mount_cmd = 'df -H'
        output = subprocess.check_output(find_mount_cmd.split(' ')).decode('utf8')
        output_parts = [o.split() for o in output.split('\n')]
        kobos = [o[-1] for o in output_parts if f'/Volumes/{label}' in o]

    if len(kobos) > 1:
        raise RuntimeError(f'Multiple Kobo devices detected: {kobos}')
    elif len(kobos) == 0:
        raise RuntimeError(f"Could not find Kobo device in with command '{find_mount_cmd}'")
    else:
        [kobo] = kobos
        return Path(kobo)
