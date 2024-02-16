from flask_restful import reqparse

from openatlas import app

default = reqparse.RequestParser()
default.add_argument(
    'download',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    default=False,
    choices=('true', 'false'),
    location='args')
default.add_argument(
    'count',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    default=False,
    choices=('true', 'false'),
    location='args')

locale = default.copy()
locale.add_argument(
    'locale',
    type=str,
    help='{error_msg}',
    default='en',
    case_sensitive=False,
    choices=app.config['LANGUAGES'],
    location='args')

entity_ = default.copy()
entity_.add_argument(
    'sort',
    choices=('desc', 'asc'),
    type=str,
    default='asc',
    case_sensitive=False,
    help='{error_msg}. Only "desc" or "asc" will work.',
    location='args')
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
        'end_to'),
    location='args')
entity_.add_argument(
    'search',
    type=str,
    help='{error_msg}',
    action='append',
    location='args')
entity_.add_argument(
    'limit',
    type=int,
    default=20,
    help="Invalid number for limit",
    location='args')
entity_.add_argument(
    'first',
    type=int,
    help="Not a valid ID",
    location='args')
entity_.add_argument(
    'last',
    type=int,
    help="Not a valid ID",
    location='args')
entity_.add_argument(
    'page',
    type=int,
    help="Not a valid page number",
    location='args')
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
        'depictions', 'geonames', 'description', 'none'),
    location='args')
entity_.add_argument(
    'export',
    type=str,
    help='{error_msg}',
    choices=('csv', 'csvNetwork'),
    location='args')
entity_.add_argument(
    'format',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    choices=frozenset(app.config['API_FORMATS']),
    location='args')
entity_.add_argument(
    'type_id',
    type=int,
    help='{error_msg}',
    action='append',
    location='args')
entity_.add_argument(
    'relation_type',
    type=str,
    help='{error_msg}',
    action='append',
    location='args')
entity_.add_argument(
    'centroid',
    type=str,
    case_sensitive=False,
    default=False,
    choices=('true', 'false'),
    location='args')

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
        'gisPolygonAll'),
    location='args')
query = entity_.copy()
query.add_argument(
    'entities',
    type=int,
    action='append',
    help="{error_msg}",
    location='args')
query.add_argument(
    'cidoc_classes',
    type=str,
    action='append',
    help="{error_msg}",
    location='args')
query.add_argument(
    'view_classes',
    type=str,
    action='append',
    help="{error_msg}",
    location='args')
query.add_argument(
    'system_classes',
    type=str,
    action='append',
    help="{error_msg}",
    location='args')

image = default.copy()
image.add_argument(
    'image_size',
    type=str,
    help="{error_msg}",
    case_sensitive=False,
    choices=list(size for size in app.config['IMAGE_SIZE']),
    location='args')

files = default.copy()
files.add_argument(
    'file_id',
    type=int,
    help="{error_msg}",
    action='append',
    location='args')
