import gzip
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from flask import g
from rdflib import Graph

from openatlas.api.api_v1.context.lod_context import get_lod_context
from openatlas.api.api_v1.formatters.lod_formatter import format_lod_entities
from openatlas.models.entity import Entity


def stream_lod_nt(
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 2000) -> Iterator[str]:
    ctx = get_lod_context()['@context']
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
        if not (rows := g.cursor.fetchall()):
            break

        ids = [r[0] for r in rows]
        last_id = ids[-1]
        entities = Entity.get_by_ids(ids, types=True, aliases=True)
        lod_data = format_lod_entities(entities)
        lod_data['@context'] = ctx

        rdf_g = Graph()
        rdf_g.parse(data=json.dumps(lod_data), format='json-ld')
        exported += len(entities)
        yield rdf_g.serialize(format='nt')


def export_lod_dump_to_file(
        output_path: Path | str,
        *,
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 2000,
        compress: bool = True) -> Path:
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if compress:
        if not str(target_path).endswith('.gz'):
            target_path = target_path.with_name(f'{target_path.name}.gz')
        with gzip.open(target_path, 'wt', encoding='utf-8') as f:
            for chunk in stream_lod_nt(
                    class_name=class_name,
                    limit=limit,
                    batch_size=batch_size):
                f.write(chunk)
    else:
        with open(target_path, 'w', encoding='utf-8') as f:
            for chunk in stream_lod_nt(
                    class_name=class_name,
                    limit=limit,
                    batch_size=batch_size):
                f.write(chunk)

    return target_path
