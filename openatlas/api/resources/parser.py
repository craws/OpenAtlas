from flask_restful import reqparse

from openatlas import app

default = reqparse.RequestParser()
default.add_argument(
    'download',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    default=False,
    choices=('true', 'false'))
default.add_argument(
    'count',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    default=False,
    choices=('true', 'false'))

language = default.copy()
language.add_argument(
    'lang',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    choices=app.config['LANGUAGES'])

entity_ = default.copy()
entity_.add_argument(
    'sort',
    choices=('desc', 'asc'),
    type=str,
    default='asc',
    case_sensitive=False,
    help='{error_msg}. Only "desc" or "asc" will work.')
entity_.add_argument(
    'column',
    type=str,
    default='name',
    case_sensitive=False,
    help='{error_msg}',
    choices=(
        'id',
        'name',
        'cidoc_class',
        'system_class',
        'begin_from',
        'begin_to',
        'end_from',
        'end_to'))
entity_.add_argument(
    'search',
    type=str,
    help='{error_msg}',
    action='append')
entity_.add_argument(
    'limit',
    type=int,
    default=20,
    help="Invalid number for limit")
entity_.add_argument(
    'first',
    type=int,
    help="Not a valid ID")
entity_.add_argument(
    'last',
    type=int,
    help="Not a valid ID")
entity_.add_argument(
    'page',
    type=int,
    help="Not a valid page number")
entity_.add_argument(
    'show',
    type=str,
    help='{error_msg}.',
    action='append',
    case_sensitive=False,
    default=[
        'when', 'types', 'relations', 'names', 'links', 'geometry',
        'depictions', 'geonames', 'description'],
    choices=(
        'when', 'types', 'relations', 'names', 'links', 'geometry',
        'depictions', 'geonames', 'description', 'none'))
entity_.add_argument(
    'export',
    type=str,
    help='{error_msg}',
    choices=('csv', 'csvNetwork'))
entity_.add_argument(
    'format',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    choices=frozenset(app.config['API_FORMATS']))
entity_.add_argument(
    'type_id',
    type=int,
    help='{error_msg}',
    action='append')
entity_.add_argument(
    'relation_type',
    type=str,
    help='{error_msg}',
    action='append')
entity_.add_argument(
    'centroid',
    type=str,
    case_sensitive=False,
    default=False,
    choices=('true', 'false'))

gis = default.copy()
gis.add_argument(
    'geometry',
    type=str,
    help='{error_msg}',
    default='gisAll',
    action='append',
    choices=(
        'gisAll',
        'gisPointAll',
        'gisPointSupers',
        'gisPointSubs',
        'gisPointSibling',
        'gisLineAll',
        'gisPolygonAll'))
query = entity_.copy()
query.add_argument(
    'entities',
    type=int,
    action='append',
    help="{error_msg}")
query.add_argument(
    'cidoc_classes',
    type=str,
    action='append',
    help="{error_msg}")
query.add_argument(
    'view_classes',
    type=str,
    action='append',
    help="{error_msg}")
query.add_argument(
    'system_classes',
    type=str,
    action='append',
    help="{error_msg}")

image = default.copy()
image.add_argument(
    'image_size',
    type=str,
    help="{error_msg}",
    case_sensitive=False,
    choices=(list(size for size in app.config['IMAGE_SIZE'])))
