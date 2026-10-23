import json
import pathlib
from typing import Any

from flask import Response, jsonify
from flask_restful import marshal

from openatlas import app
from openatlas.api.api_v04.formats.xml import subunit_xml
from openatlas.api.api_v04.resources.templates import subunit_template


def resolve_subunits(
        subunit: list[dict[str, Any]],
        parser: dict[str, Any],
        name: str) -> Response | dict[str, Any] | tuple[Any, int]:
    out = {'collection' if parser['format'] == 'xml' else name: subunit}
    if parser['count']:
        return jsonify(len(out[name]))
    if parser['format'] == 'xml':
        if parser['download']:
            return Response(
                subunit_xml(out),
                mimetype='application/xml',
                headers={
                    'Content-Disposition': f'attachment;filename={name}.xml'})
        return Response(
            subunit_xml(out),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['download']:
        download(out, subunit_template(name))
    return marshal(out, subunit_template(name)), 200


def parse_loud_context() -> dict[str, str]:
    context = get_loud_context().get('@context', {})
    inverted: dict[str, str] = {}
    for term, definition in context.items():
        if not isinstance(definition, dict):
            continue
        inverted[definition['@id']] = term
        for nested_term, nested_def in definition.get('@context', {}).items():
            if isinstance(nested_def, dict):
                inverted[nested_def['@id']] = nested_term
    return inverted


def get_loud_context() -> dict[str, Any]:
    file_path = pathlib.Path(app.root_path) / 'api' / 'linked-art.json'

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def download(
        data: list[Any] | dict[Any, Any],
        template: dict[str, Any]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=result.json'})
