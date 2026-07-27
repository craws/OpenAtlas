import json
import pathlib
from typing import Any

from flask import Response, jsonify
from flask_restful import marshal

from openatlas import app
from openatlas.api.formats.xml import subunit_xml
from openatlas.api.resources.templates import subunit_template


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
    """Build a reverse lookup ``{full IRI: short LOUD term}`` from the
    bundled JSON-LD ``@context``.

    The LOUD ``@context`` (``openatlas/api/linked-art.json``) maps short
    Linked Art / CIDOC terms (e.g. ``identified_by``) to their full IRI
    definitions (e.g. ``crm:P1_is_identified_by``). When emitting JSON-LD
    we already use the short terms directly, but elsewhere — most
    notably in the CIDOC/CRM relation lookup that powers the API's
    "human readable property name" output — we have the *full* property
    URI in hand and need to recover the matching short term. This
    function produces exactly that inverse mapping.

    Structure of the context that we walk:

    - Top-level entries can be either a plain string alias or a dict
      with at least an ``@id`` (the full IRI). Only dict entries carry
      an IRI we can invert, so strings are skipped.
    - Some entries declare a nested ``@context`` (JSON-LD scoped
      contexts, used by Linked Art to redefine terms inside specific
      types, e.g. ``Production`` redefining ``carried_out_by``). We
      recurse one level into those so the nested terms also become
      resolvable; deeper nesting is not used in our context file today.

    Returns
    -------
    dict[str, str]
        Mapping ``full IRI -> short LOUD/CIDOC term``. Built fresh on
        every call (cheap: one small JSON file, a few dozen keys); use
        :func:`get_loud_context` if you need the raw context instead.
    """
    context = get_loud_context().get('@context', {})
    inverted: dict[str, str] = {}
    for term, definition in context.items():
        if not isinstance(definition, dict):
            continue  # plain string aliases carry no @id to invert
        inverted[definition['@id']] = term
        # Recurse one level into scoped @context blocks (e.g. Production
        # redefining carried_out_by). Deeper nesting is not used today.
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
