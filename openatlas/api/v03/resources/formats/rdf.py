import json
from typing import Any, Dict, Iterable, List, Union

from rdflib import Graph


def rdf_output(
        data: Union[List[Dict[str, Any]], Dict[str, Any]],
        parser: Dict[str, Any]) \
        -> Union[str, bytes, bytearray, Iterable[str], Iterable[bytes], None]:
    graph = Graph().parse(data=json.dumps(data), format='json-ld')
    return graph.serialize(format=parser['format'], encoding='utf-8')
