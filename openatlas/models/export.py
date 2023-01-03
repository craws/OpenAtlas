import os
import shutil
import subprocess
from datetime import datetime
from typing import Optional

from openatlas import app


def current_date_for_filename() -> str:
    today = datetime.today()
    return \
        f'{today.year}-{today.month:02}-{today.day:02}_' \
        f'{today.hour:02}{today.minute:02}'


def sql_export(postfix: Optional[str] = '') -> bool:
    file = \
        app.config['EXPORT_DIR'] \
        / f'{current_date_for_filename()}_dump{postfix}.sql'
    pg_dump = "pg_dump" if os.name == 'posix' \
        else f'"{shutil.which("pg_dump.exe")}"'
    command = \
        f"{pg_dump} " \
        f"-h {app.config['DATABASE_HOST']} " \
        f"-d {app.config['DATABASE_NAME']} " \
        f"-U {app.config['DATABASE_USER']} " \
        f"-p {app.config['DATABASE_PORT']} " \
        f"-f {file}"
    try:
        root = os.environ['SYSTEMROOT'] if 'SYSTEMROOT' in os.environ else ''
        subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            env={
                'PGPASSWORD': app.config['DATABASE_PASS'],
                'SYSTEMROOT': root}).wait()
        with open(os.devnull, 'w') as null:
            subprocess.Popen(
                ['7z', 'a', f'{file}.7z', file],
                stdout=null).wait()
        file.unlink()
    except Exception:
        return False

    return True
