import requests
from flask import request, jsonify, Response
from flask_restful import Resource

from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.api.resources.util import get_license_name
from openatlas import app


def getManifest(id_):
    entity = get_entity_by_id(id_)
    url_root = app.config['IIIF_URL'] or f"{request.url_root}iiif/"
    # get metadata from the image api
    req = requests.get(
        f"{url_root}{app.config['IIIF_PREFIX']}{id_}/info.json")
    image_api = req.json()
    iiif_id = f"{url_root}{id_}"
    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": f"{request.base_url}",
        "@type": "sc:Manifest",
        "label": entity.name,
        "metadata": [],
        "description": [{
            "@value": entity.description,
            "@language": "en"}],
        "license": get_license_name(entity),
        "attribution": "By OpenAtlas",
        "sequences": [{
            "@id": "http://c8b09ce6-df6d-4d5e-9eba-17507dc5c185",
            "@type": "sc:Sequence",
            "label": [{
                "@value": "Normal Sequence",
                "@language": "en"}],
            "canvases": [{
                "@id": "http://251a31df-761d-46df-85c3-66cb967b8a67",
                "@type": "sc:Canvas",
                "label": entity.name,
                "height": image_api['height'],
                "width": image_api['width'],
                "description": {
                    "@value": entity.description,
                    "@language": "en"},
                "images": [{
                    "@context":
                        "http://iiif.io/api/presentation/2/context.json",
                    "@id": "http://a0a3ec3e-2084-4253-b0f9-a5f87645e15d",
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@id": f"{iiif_id}/full/full/0/default.jpg",
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "service": {
                            "@context":
                                "http://iiif.io/api/image/2/context.json",
                            "@id": iiif_id,
                            "profile": image_api['profile']
                        },
                        "height": image_api['height'],
                        "width": image_api['width']},
                    "on": "http://251a31df-761d-46df-85c3-66cb967b8a67"}],
                "related": ""}]}],
        "structures": []}


    return manifest


class IIIFManifest(Resource):
    @staticmethod
    def get(id_: int) -> Response:
        # content = gzip.compress(json.dumps(getManifest(id_)).encode(
        # 'utf8'), 5)
        # response = Response(content)
        # response.headers['Content-length'] = len(content)
        # response.headers['Content-Encoding'] = 'gzip'
        return jsonify(getManifest(id_))
