import json
from typing import Any, Iterable, Union

from rdflib import Graph


def rdf_output(
        data: Union[list[dict[str, Any]], dict[str, Any]],
        parser: dict[str, Any]) \
        -> Union[str, bytes, bytearray, Iterable[str], Iterable[bytes], None]:
    graph = Graph().parse(data=json.dumps(data), format='json-ld')
    return graph.serialize(format=parser['format'], encoding='utf-8')
