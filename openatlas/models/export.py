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
        app.config['EXPORT_DIR'] / 'sql' \
        / f'{current_date_for_filename()}_dump{postfix}.sql'
    if os.name == 'posix':
        command = \
            "pg_dump " \
            f"-h {app.config['DATABASE_HOST']} " \
            f"-d {app.config['DATABASE_NAME']} " \
            f"-U {app.config['DATABASE_USER']} " \
            f"-p {app.config['DATABASE_PORT']} " \
            f"-f {file}"
        try:
            subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                env={'PGPASSWORD': app.config['DATABASE_PASS']}).wait()
            with open(os.devnull, 'w') as null:
                subprocess.Popen(
                    ['7z', 'a', f'{file}.7z', file],
                    stdout=null).wait()
            file.unlink()
        except Exception:  # pragma: no cover
            return False
    else:  # pragma: no cover
        os.popen(
            f'"{shutil.which("pg_dump")}" '
            '-h 127.0.0.1 '
            f'-d {app.config["DATABASE_NAME"]} '
            f'-U {app.config["DATABASE_USER"]} '
            f'-p {app.config["DATABASE_PORT"]} '
            f'> {file}')
    return True
