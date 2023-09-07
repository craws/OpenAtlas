import json
import os
from typing import Any, Union

from rdflib import Graph

from openatlas import app


def rdf_output(
        data: Union[list[dict[str, Any]], dict[str, Any]],
        parser: dict[str, Any]) -> Any:  # pragma: nocover
    os.environ['http_proxy'] = app.config['API_PROXY']
    os.environ['https_proxy'] = app.config['API_PROXY']
    graph = Graph().parse(data=json.dumps(data), format='json-ld')
    return graph.serialize(format=parser['format'], encoding='utf-8')
