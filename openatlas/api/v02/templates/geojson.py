from typing import Dict, Type

from flask_restful import fields
from flask_restful.fields import String


class GeoJson:

    @staticmethod
    def geojson_template(show: Dict[str, str]) -> Dict[str, Type[String]]:
        title = {'title': fields.String}

        relations = {'label': fields.String,
                     'relationTo': fields.String,
                     'relationType': fields.String}

        depictions = {'@id': fields.String,
                      'title': fields.String,
                      'license': fields.String,
                      'url': fields.String}

        links = {'type': fields.String,
                 'identifier': fields.String}

        types = {'identifier': fields.String,
                 'label': fields.String,
                 'description': fields.String,
                 'hierarchy': fields.String}

        names = {'alias': fields.String}

        start = {'earliest': fields.String,
                 'latest': fields.String}

        end = {'earliest': fields.String,
               'latest': fields.String}

        description = {'value': fields.String}

        timespans = {'start': fields.Nested(start),
                     'end': fields.Nested(end)}

        when = {'timespans': fields.List(fields.Nested(timespans))}

        geometries = {'type': fields.String,
                      'coordinates': fields.List(fields.Float),
                      'title': fields.String,
                      'description': fields.String}

        geometry = {'type': fields.String,
                    'geometries': fields.Nested(geometries)}

        feature = {'@id': fields.String,
                   'type': fields.String,
                   'crmClass': fields.String,
                   'properties': fields.Nested(title),
                   'description': fields.List(fields.Nested(description))
                   }

        if 'when' in show:
            feature['when'] = fields.Nested(when)

        if 'types' in show:
            feature['types'] = fields.List(fields.Nested(types))

        if 'relations' in show:
            feature['relations'] = fields.List(fields.Nested(relations))

        if 'names' in show:
            feature['names'] = fields.List(fields.Nested(names))

        if 'links' in show:
            feature['links'] = fields.List(fields.Nested(links))

        # ToDo: geometry has to be dynamic, if it is only one geometry than geometries will never be returned. If it is a Point, the coordinates are list of two floats, else it is a list of lists, or maybe a lists of lists of lists...
        # Look into that: https://blog.fossasia.org/dynamically-marshaling-output-in-flask-restplus/
        # https://github.com/flask-restful/flask-restful/issues/212
        # --> Maybe return the geometric with flask_restful.marshal_with_field
        # if 'geometry' in show:
        #    feature['geometry'] = fields.Nested(geometries)

        if 'depictions' in show:
            feature['depictions'] = fields.List(fields.Nested(depictions))

        entity_json = {'@context': fields.String,
                       'type': fields.String,
                       'features': fields.List(fields.Nested(feature))}

        return entity_json
