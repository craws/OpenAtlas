import gzip
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from flask import g
from rdflib import Dataset

from openatlas.api.api_v1.formatters.la_formatter import (
    LA_CONTEXT, format_la_entities)
from openatlas.models.entity import Entity


def stream_la_dump(
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 1000,
        output_format: str = 'jsonl') -> Iterator[str]:
    last_id = 0
    exported = 0

    while True:
        cur_limit = batch_size
        if limit is not None:
            if exported >= limit:
                break
            cur_limit = min(batch_size, limit - exported)

        where_clause = 'WHERE id > %(last_id)s'
        params: dict[str, Any] = {'last_id': last_id, 'limit': cur_limit}
        if class_name and class_name.lower() != 'all':
            where_clause += ' AND openatlas_class_name = %(class)s'
            params['class'] = class_name.lower()

        g.cursor.execute(
            f'SELECT id FROM model.entity {where_clause} ORDER BY id '
            f'LIMIT %(limit)s;',
            params)
        rows = g.cursor.fetchall()
        if not rows:
            break

        ids = [r[0] for r in rows]
        last_id = ids[-1]

        entities = Entity.get_by_ids(ids, types=True, aliases=True)
        if not entities:
            break

        la_data = format_la_entities(entities)
        items = la_data['orderedItems']

        if output_format == 'nt':
            graph = Dataset()
            graph.parse(data=json.dumps(la_data), format='json-ld')
            nt = graph.serialize(format='nt')
            exported += len(entities)
            yield nt
        else:
            lines = [
                json.dumps({'@context': LA_CONTEXT, **item})
                for item in items]
            chunk = '\n'.join(lines) + '\n'
            exported += len(entities)
            yield chunk


def export_la_dump_to_file(
        output_path: Path | str,
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 1000,
        output_format: str = 'jsonl',
        compress: bool = True) -> Path:
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if compress:
        if not str(target_path).endswith('.gz'):
            target_path = target_path.with_name(f'{target_path.name}.gz')
        with gzip.open(target_path, 'wt', encoding='utf-8') as f:
            for chunk in stream_la_dump(
                    class_name=class_name,
                    limit=limit,
                    batch_size=batch_size,
                    output_format=output_format):
                f.write(chunk)
    else:
        with open(target_path, 'w', encoding='utf-8') as f:
            for chunk in stream_la_dump(
                    class_name=class_name,
                    limit=limit,
                    batch_size=batch_size,
                    output_format=output_format):
                f.write(chunk)

    return target_path
