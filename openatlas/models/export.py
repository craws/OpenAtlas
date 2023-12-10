import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from openatlas import app


def current_date_for_filename() -> str:
    today = datetime.today()
    return \
        f'{today.year}-{today.month:02}-{today.day:02}_' \
        f'{today.hour:02}{today.minute:02}'


def sql_export(format_: str, postfix: Optional[str] = '') -> bool:
    file = app.config['EXPORT_PATH'] \
           / f'{current_date_for_filename()}_export{postfix}.{format_}'
    command: Any = [
        "pg_dump" if os.name == 'posix'
        else Path(str(shutil.which("pg_dump.exe")))]
    if format_ == 'dump':
        command.append('-Fc')
    command.extend([
        '-h', app.config['DATABASE_HOST'],
        '-d', app.config['DATABASE_NAME'],
        '-U', app.config['DATABASE_USER'],
        '-p', str(app.config['DATABASE_PORT']),
        '-f', file])
    try:
        root = os.environ['SYSTEMROOT'] if 'SYSTEMROOT' in os.environ else ''
        subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            env={
                'PGPASSWORD': app.config['DATABASE_PASS'],
                'SYSTEMROOT': root}).wait()
        with open(os.devnull, 'w', encoding='utf8') as null:
            subprocess.Popen(
                ['7z', 'a', f'{file}.7z', file],
                stdout=null).wait()
        file.unlink()
    except Exception:  # pragma: no cover
        return False

    return True
