import json
from collections.abc import Iterator
from pathlib import Path

from rdflib import Graph

from openatlas.api.api_v1.context.lod_context import get_lod_context
from openatlas.api.api_v1.formatters.export_util import (
    iter_entity_batches, write_stream_to_file)
from openatlas.api.api_v1.formatters.lod_formatter import format_lod_entities


def stream_lod_nt(
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 2000) -> Iterator[str]:
    ctx = get_lod_context()['@context']
    for entities in iter_entity_batches(
            class_name=class_name,
            limit=limit,
            batch_size=batch_size):
        lod_data = format_lod_entities(entities)
        graph_data = {
            '@context': ctx,
            '@graph': lod_data['orderedItems']}
        rdf_g = Graph()
        rdf_g.parse(data=json.dumps(graph_data), format='json-ld')
        yield rdf_g.serialize(format='nt')


def export_lod_dump_to_file(
        output_path: Path | str,
        *,
        class_name: str | None = None,
        limit: int | None = None,
        batch_size: int = 2000,
        compress: bool = True) -> Path:
    return write_stream_to_file(
        output_path,
        stream_lod_nt(
            class_name=class_name,
            limit=limit,
            batch_size=batch_size),
        compress=compress)
