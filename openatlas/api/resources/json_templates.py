from flask_restful import fields

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

timespans = {'start': fields.Nested(start),
             'end': fields.Nested(end)}

when = {'timespans': fields.List(fields.Nested(timespans))}

geometries = {'type': fields.String,
              'coordinates': fields.List,
              'title': fields.String,
              'description': fields.String}

geometry = {'type': fields.String,
            'geometries': fields.List(fields.Nested(geometries)) }

feature = {'@id': fields.String,
           'type': fields.String,
           'crmClass': fields.String,
           'properties': fields.Nested(title),
           'description': fields.String,
           'types': fields.List(fields.Nested(types)),
           'names': fields.List(fields.Nested(names)),
           'when': fields.Nested(when),
           'relations': fields.List(fields.Nested(relations)),
           'depictions': fields.List(fields.Nested(depictions)),
           'links': fields.List(fields.Nested(links)),
           'geometry': fields.Nested(geometry)
           }

entity_json = {'@context': fields.String,
               'type': fields.String,
               'features': fields.List(fields.Nested(feature))}
