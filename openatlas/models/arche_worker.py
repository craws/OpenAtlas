from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import g, has_request_context
from psycopg2.extensions import connection

from openatlas import app
from openatlas.database.connect import open_connection
from openatlas.models.export import arche_export

ARCHE_EXPORT_LOCK_ID = 472910384
ARCHE_STATUS_FILENAME = '.export_status.json'
ARCHE_WORKER_LOG_FILENAME = '.export_worker.log'
STARTING_GRACE_SECONDS = 30
ACTIVE_STATUSES = ('starting', 'running')


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def get_status_path() -> Path:
    return Path(app.config['ARCHE_PATH']) / ARCHE_STATUS_FILENAME


def get_worker_log_path() -> Path:
    return Path(app.config['ARCHE_PATH']) / ARCHE_WORKER_LOG_FILENAME


def cleanup_empty_worker_log() -> None:
    log_path = get_worker_log_path()
    try:
        if log_path.is_file() and log_path.stat().st_size == 0:
            log_path.unlink()
    except OSError:
        pass


def write_arche_status(data: dict[str, Any]) -> None:
    arche_dir = Path(app.config['ARCHE_PATH'])
    arche_dir.mkdir(parents=True, exist_ok=True)
    status_path = get_status_path()
    tmp_path = status_path.with_suffix('.json.tmp')
    tmp_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    os.replace(tmp_path, status_path)


def read_arche_status() -> dict[str, Any]:
    status_path = get_status_path()
    try:
        raw = status_path.read_text(encoding='utf-8')
        data = json.loads(raw)
    except (OSError, ValueError):
        return {'status': 'idle'}
    if not isinstance(data, dict):
        return {'status': 'idle'}
    return data


def check_lock_with_cursor(cur: Any) -> bool:
    cur.execute(
        'SELECT pg_try_advisory_lock(%(lock_id)s) AS acquired',
        {'lock_id': ARCHE_EXPORT_LOCK_ID})
    row = cur.fetchone()
    acquired = bool(row and row[0])
    if acquired:
        cur.execute(
            'SELECT pg_advisory_unlock(%(lock_id)s)',
            {'lock_id': ARCHE_EXPORT_LOCK_ID})
    return not acquired


def is_arche_export_locked() -> bool:
    if has_request_context() and hasattr(g, 'cursor'):
        return check_lock_with_cursor(g.cursor)
    conn = open_connection(app.config)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            return check_lock_with_cursor(cur)
    finally:
        conn.close()


def is_starting_expired(started_at: object) -> bool:
    if not isinstance(started_at, str) or not started_at:
        return True
    try:
        started_dt = datetime.fromisoformat(started_at)
    except ValueError:
        return True
    if started_dt.tzinfo is None:
        started_dt = started_dt.replace(tzinfo=timezone.utc)
    elapsed = (datetime.now(timezone.utc) - started_dt).total_seconds()
    return elapsed > STARTING_GRACE_SECONDS


def get_arche_export_status() -> dict[str, Any]:
    status = read_arche_status()
    locked = is_arche_export_locked()
    state = status.get('status', 'idle')
    if locked:
        if state != 'running':
            return {**status, 'status': 'running'}
        return status
    if state == 'running':
        updated = {
            **status,
            'status': 'failed',
            'finished_at': utc_now_iso(),
            'error': 'Export process terminated unexpectedly'}
        write_arche_status(updated)
        return updated
    if state == 'starting' and is_starting_expired(status.get('started_at')):
        updated = {
            **status,
            'status': 'failed',
            'finished_at': utc_now_iso(),
            'error': 'Export worker failed to start'}
        write_arche_status(updated)
        return updated
    return status


def get_python_executable() -> str:
    if sys.executable and Path(sys.executable).name.startswith('python'):
        return sys.executable
    prefix_bin = Path(sys.prefix) / 'bin'
    for candidate in (prefix_bin / 'python', prefix_bin / 'python3'):
        if candidate.exists():
            return str(candidate)
    return shutil.which('python3') or shutil.which('python') or 'python3'


def acquire_arche_lock() -> connection | None:
    conn = open_connection(app.config)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(
            'SELECT pg_try_advisory_lock(%(lock_id)s) AS acquired',
            {'lock_id': ARCHE_EXPORT_LOCK_ID})
        row = cur.fetchone()
        acquired = bool(row and row[0])
    if acquired:
        return conn
    conn.close()
    return None


def release_arche_lock(conn: connection) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT pg_advisory_unlock(%(lock_id)s)',
                {'lock_id': ARCHE_EXPORT_LOCK_ID})
    finally:
        conn.close()


def execute_arche_export_in_context(base_url: str | None) -> Path:
    if has_request_context():
        try:
            archive_path = arche_export()
            g.logger.log('info', 'database', 'ARCHE export')
            return archive_path
        except Exception as e:
            g.logger.log('error', 'database', 'ARCHE export failed', e)
            raise
    with app.test_request_context(
            '/export/arche/execute',
            base_url=base_url or 'http://localhost/'):
        try:
            early_response = app.preprocess_request()
            if early_response is not None:
                raise RuntimeError(
                    'Application request preprocessing aborted unexpectedly')
            archive_path = arche_export()
            g.logger.log('info', 'database', 'ARCHE export')
            return archive_path
        except Exception as e:
            if hasattr(g, 'logger'):
                g.logger.log('error', 'database', 'ARCHE export failed', e)
            raise


def run_arche_export_job(base_url: str | None = None) -> Path | None:
    lock_conn = acquire_arche_lock()
    if lock_conn is None:
        return None
    started_at = utc_now_iso()
    started_mono = time.monotonic()
    pid = os.getpid()
    write_arche_status({
        'status': 'running',
        'started_at': started_at,
        'finished_at': None,
        'duration_seconds': None,
        'filename': None,
        'error': None,
        'pid': pid})
    try:
        archive_path = execute_arche_export_in_context(base_url)
        write_arche_status({
            'status': 'done',
            'started_at': started_at,
            'finished_at': utc_now_iso(),
            'duration_seconds': round(time.monotonic() - started_mono, 1),
            'filename': archive_path.name,
            'error': None,
            'pid': pid})
        cleanup_empty_worker_log()
        return archive_path
    except Exception as e:
        write_arche_status({
            'status': 'failed',
            'started_at': started_at,
            'finished_at': utc_now_iso(),
            'duration_seconds': round(time.monotonic() - started_mono, 1),
            'filename': None,
            'error': str(e),
            'pid': pid})
        raise
    finally:
        release_arche_lock(lock_conn)


def start_arche_export_subprocess(base_url: str) -> int:
    started_at = utc_now_iso()
    write_arche_status({
        'status': 'starting',
        'started_at': started_at,
        'finished_at': None,
        'duration_seconds': None,
        'filename': None,
        'error': None,
        'pid': None})
    command = [
        get_python_executable(),
        '-m', 'flask',
        '--app', 'openatlas',
        'arche-export',
        '--base-url', base_url]
    log_path = get_worker_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with log_path.open('w', encoding='utf-8') as err_log:
            proc = subprocess.Popen(
                command,
                cwd=str(Path(app.root_path).parent),
                env=os.environ.copy(),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=err_log,
                start_new_session=True,
                close_fds=True)
    except OSError as e:
        write_arche_status({
            'status': 'failed',
            'started_at': started_at,
            'finished_at': utc_now_iso(),
            'duration_seconds': None,
            'filename': None,
            'error': str(e),
            'pid': None})
        raise
    return proc.pid


def main() -> None:
    parser = argparse.ArgumentParser(description='Run ARCHE export job')
    parser.add_argument('--base-url', default='http://localhost/')
    args = parser.parse_args()
    result = run_arche_export_job(base_url=args.base_url)
    if result is None:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
