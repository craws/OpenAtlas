import json
from collections.abc import Iterator
from pathlib import Path

from flask import g
from rdflib import Dataset

from openatlas.api.api_v1.context.lod_context import get_linked_art_context
from openatlas.api.api_v1.formatters.export_util import (
    iter_entity_batches, write_stream_to_file)
from openatlas.api.api_v1.formatters.la_formatter import (
    LA_CONTEXT, format_la_entities)


def _clear_batch_caches() -> None:
    if hasattr(g, 'api_file_paths'):
        g.api_file_paths.clear()
    if hasattr(g, 'api_rights_holders'):
        g.api_rights_holders.clear()


def stream_la_dump(
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 1000,
        output_format: str = 'jsonl') -> Iterator[str]:
    la_ctx = get_linked_art_context() if output_format == 'nt' else None
    for entities in iter_entity_batches(
            class_name=class_name,
            limit=limit,
            batch_size=batch_size):
        la_data = format_la_entities(entities)
        _clear_batch_caches()

        if output_format == 'nt':
            graph_data = {
                '@context': la_ctx,
                '@graph': la_data['orderedItems']}
            graph = Dataset()
            graph.parse(data=json.dumps(graph_data), format='json-ld')
            yield graph.serialize(format='nt')
        else:
            lines = [
                json.dumps({'@context': LA_CONTEXT, **item})
                for item in la_data['orderedItems']]
            yield '\n'.join(lines) + '\n'


def export_la_dump_to_file(
        output_path: Path | str,
        *,
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 1000,
        output_format: str = 'jsonl',
        compress: bool = True) -> Path:
    return write_stream_to_file(
        output_path,
        stream_la_dump(
            class_name=class_name,
            limit=limit,
            batch_size=batch_size,
            output_format=output_format),
        compress=compress)
