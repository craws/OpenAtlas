import gzip
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Final

from flask import g

from openatlas import app
from openatlas.api.api_v1.error_handlers import abort_too_many_requests
from openatlas.api.api_v1.models.util import OpenAtlasClassEnum
from openatlas.api.api_v1.util.files import has_file_access
from openatlas.models.entity import Entity

MAX_CONCURRENT_DUMPS: Final[int] = 2
_DUMP_SEMAPHORE = threading.BoundedSemaphore(MAX_CONCURRENT_DUMPS)
PUBLIC_EXPORT_CLASSES: Final[list[str]] = [
    c.value for c in OpenAtlasClassEnum]


def _fetch_batch_ids(
        last_id: int,
        batch_limit: int,
        class_name: str | None) -> list[int]:
    if class_name and class_name.lower() != 'all':
        g.cursor.execute(
            """
            SELECT id FROM model.entity
            WHERE id > %(last_id)s AND openatlas_class_name = %(class)s
            ORDER BY id LIMIT %(limit)s;
            """,
            {
                'last_id': last_id,
                'class': class_name.lower(),
                'limit': batch_limit})
    else:
        g.cursor.execute(
            """
            SELECT id FROM model.entity
            WHERE id > %(last_id)s
                AND openatlas_class_name = ANY(%(classes)s)
            ORDER BY id LIMIT %(limit)s;
            """,
            {
                'last_id': last_id,
                'classes': PUBLIC_EXPORT_CLASSES,
                'limit': batch_limit})
    return [row[0] for row in g.cursor.fetchall()]


def iter_entity_batches(
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 1000) -> Iterator[list[Entity]]:
    last_id = 0
    exported = 0

    while True:
        if limit is not None and exported >= limit:
            break
        ids = _fetch_batch_ids(last_id, batch_size, class_name)
        if not ids:
            break

        last_id = ids[-1]
        entities = [
            e for e in Entity.get_by_ids(ids, types=True, aliases=True)
            if e.class_.name != 'file' or has_file_access(e)]
        if not entities:
            continue
        if limit is not None:
            entities = entities[:limit - exported]
        exported += len(entities)
        yield entities


def guard_dump_stream(stream: Iterator[str]) -> Iterator[str]:
    if not _DUMP_SEMAPHORE.acquire(blocking=False):
        abort_too_many_requests()

    def _guarded() -> Iterator[str]:
        try:
            yield from stream
        except Exception:
            app.logger.exception('Error while streaming API dump')
            raise
        finally:
            _DUMP_SEMAPHORE.release()

    return _guarded()


def write_stream_to_file(
        output_path: Path | str,
        chunks: Iterator[str],
        *,
        compress: bool = True) -> Path:
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if compress:
        if not str(target_path).endswith('.gz'):
            target_path = target_path.with_name(f'{target_path.name}.gz')
        with gzip.open(target_path, 'wt', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(chunk)
    else:
        with open(target_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(chunk)

    return target_path
