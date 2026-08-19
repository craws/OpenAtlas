from typing import Any

from flask import Response, request
from flask_openapi3 import APIBlueprint
from rdflib import Graph

from openatlas import app
from openatlas.api.api_v04.formats.loud import get_loud_entities
from openatlas.api.api_v04.resources.resolve_endpoints import \
    parse_loud_context
from openatlas.api.api_v04.resources.util import get_type_references
from openatlas.api.api_v1.error_handlers import abort_not_found, \
    register_error_handlers
from openatlas.api.api_v1.loud_util import get_links_for_entities
from openatlas.api.api_v1.models import EntityPath
from openatlas.api.api_v1.openapi_responses import lod_responses
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.models.entity import Entity

api_v1 = APIBlueprint('api_v1', __name__, url_prefix='/api/1')
register_error_handlers(api_v1)


def make_lod_response(data: dict[str, Any]) -> Response:
    accepted = request.accept_mimetypes.best_match(app.config['LOD_HEADER'])
    json_str = app.json.dumps(data)
    if accepted not in [
        'text/turtle', 'application/rdf+xml', 'application/n-triples']:
        return Response(json_str, mimetype='application/ld+json')

    graph = Graph()
    graph.parse(data=json_str, format='json-ld')

    match accepted:
        case 'text/turtle':
            turtle_output = graph.serialize(format='turtle')
            return Response(turtle_output, mimetype='text/turtle')

        case 'application/rdf+xml':
            xml_output = graph.serialize(format='xml')
            return Response(xml_output, mimetype='application/rdf+xml')

        case 'application/n-triples':
            nt_output = graph.serialize(format='nt')
            return Response(nt_output, mimetype='application/n-triples')


@api_v1.get(
    '/entity/<uuid:id>',
    endpoint='entity',
    summary='Get an LOD entity by UUID',
    tags=[lod_tag],
    responses=lod_responses)
@api_v1.get(
    '/entity/<uuid:id>.<ext>',
    endpoint='entity_ext',
    summary='Get an LOD entity by UUID with extension',
    tags=[lod_tag],
    responses=lod_responses)
def get_entity(path: EntityPath) -> dict[str, str] | Response:
    if path.ext:
        ext_map = {
            'json': 'application/ld+json',
            'ttl': 'text/turtle',
            'xml': 'application/rdf+xml',
            'nt': 'application/n-triples'}
        if path.ext in ext_map:
            request.environ['HTTP_ACCEPT'] = ext_map[path.ext]
    entity = Entity.get_by_uuid(path.id, types=True, aliases=True)

    if not entity:
        abort_not_found(path.id)

    parsed_context = parse_loud_context()
    type_references = get_type_references()
    data = [
        get_loud_entities(item, parsed_context, type_references)
        for item in get_links_for_entities([entity]).values()]
    return make_lod_response(data[0])
