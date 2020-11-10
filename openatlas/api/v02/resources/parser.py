from flask_restful import reqparse

from openatlas import app

app.config['BUNDLE_ERRORS'] = True  # Every parser shows bundled errors

# Parser
default_parser = reqparse.RequestParser()
default_parser.add_argument('download', type=bool, help='{error_msg}', default=False)
default_parser.add_argument('count', type=bool, help='{error_msg}', default=False)

language_parser = default_parser.copy()
language_parser.add_argument('lang', type=str,
                             help='{error_msg}',
                             case_sensitive=False,
                             choices=app.config['LANGUAGES'].keys())

entity_parser = default_parser.copy()  # inherit the default parser
entity_parser.add_argument('sort', choices=('desc', 'asc'), type=str, default='asc',
                           case_sensitive=False,
                           help='{error_msg}. Only "desc" or "asc" will work.')
entity_parser.add_argument('column', type=str, default=['name'], action='append',
                           case_sensitive=False,
                           help='{error_msg}', choices=(
        'id', 'class_code', 'name', 'description', 'created', 'modified', 'system_type',
        'begin_from', 'begin_to', 'end_from', 'end_to'))
# Todo: Dismiss negative value
entity_parser.add_argument('limit', type=int, default=20, help="Invalid number for limit")
# Todo: Either first or last
entity_parser.add_argument('first', type=int, help="Not a valid ID")
entity_parser.add_argument('last', type=int, help="Not a valid ID")
entity_parser.add_argument('show', type=str, help='{error_msg}.', action='append',
                           case_sensitive=False,
                           default=['when', 'types', 'relations', 'names', 'links', 'geometry',
                                    'depictions', 'geonames'],
                           choices=('when', 'types', 'relations', 'names', 'links', 'geometry',
                                    'depictions', 'geonames', 'none'))
entity_parser.add_argument('filter', type=str, help='{error_msg}', action='append',
                           default='and|id|gt|1')
