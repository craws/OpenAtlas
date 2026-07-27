from typing import Any

from flask import Response, request
from flask_openapi3 import APIBlueprint
from rdflib import Graph

from openatlas import app
from openatlas.api.api_v04.endpoints.endpoint import Endpoint
from openatlas.api.api_v04.resources.parser import entity_
from openatlas.api.api_v1.error_handlers import abort_not_found, register_error_handlers
from openatlas.api.api_v1.models import EntityPath
from openatlas.api.api_v1.openapi_responses import lod_responses
from openatlas.api.api_v1.openapi_tags import lod_tag
from openatlas.models.entity import Entity


api_v1 = APIBlueprint('api_v1', __name__, url_prefix='/api/1')
register_error_handlers(api_v1)


def make_lod_response(data: dict[str, Any]) -> Response:
    accepted = request.accept_mimetypes.best_match(app.config['LOD_HEADER'])

    if accepted not in ['text/turtle', 'application/rdf+xml', 'application/n-triples']:
        return Response(
            app.json.dumps(data),
            mimetype='application/ld+json')

    graph = Graph()

    json_str = app.json.dumps(data)

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
def get_entity(path: EntityPath) -> dict[str, str] | Response:
    entity = Entity.get_by_uuid(path.id, types=True, aliases=True)

    if not entity:
        abort_not_found(path.id)
    parser = entity_.parse_args()
    parser['format'] = 'loud'
    data = Endpoint(
            entity,
            parser,
            single=True).resolve()
    return make_lod_response(data)

# This is a workaround for swagger ui, because we can't use pip/uv
# Todo: look into variants with npm
@app.route('/api/1/docs/swagger')
def custom_swagger_ui():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>OpenAtlas V1 - Swagger UI</title>
      <link rel="stylesheet" 
        href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      
      <script 
    src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
      <script>
        window.onload = () => {
          window.ui = SwaggerUIBundle({
            // HIER saugt sich Swagger deine generierte OpenAPI-Spec rein:
            url: '/api/1/docs/openapi.json',
            dom_id: '#swagger-ui',
          });
        };
      </script>
    </body>
    </html>
    """
    return html

