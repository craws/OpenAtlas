from flask_restful import reqparse

from openatlas import app

app.config['BUNDLE_ERRORS'] = True

default = reqparse.RequestParser()
default.add_argument('download', type=bool, help='{error_msg}', default=False)
default.add_argument('count', type=bool, help='{error_msg}', default=False)

language = default.copy()
language.add_argument(
    'lang',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    choices=app.config['LANGUAGES'].keys())

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
    default=['name'],
    action='append',
    case_sensitive=False,
    help='{error_msg}', choices=(
        'id', 'class_code', 'name', 'description', 'created', 'modified',
        'system_class', 'begin_from', 'begin_to', 'end_from', 'end_to'))
entity_.add_argument(
    'filter',
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
    'show',
    type=str,
    help='{error_msg}.',
    action='append',
    case_sensitive=False,
    default=[
        'when', 'types', 'relations', 'names', 'links', 'geometry',
        'depictions', 'geonames'],
    choices=(
        'when', 'types', 'relations', 'names', 'links', 'geometry',
        'depictions', 'geonames', 'none'))
entity_.add_argument(
    'export',
    type=str,
    help='{error_msg}',
    choices='csv')
entity_.add_argument(
    'format',
    type=str,
    help='{error_msg}',
    case_sensitive=False,
    default='lp',
    choices=('lp', 'geojson'))
entity_.add_argument(
    'type_id',
    type=int,
    help='{error_msg}',
    action='append'
)

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
    'classes',
    type=str,
    action='append',
    help="{error_msg}")
query.add_argument(
    'codes',
    type=str,
    action='append',
    help="{error_msg}",
    case_sensitive=False,
    choices=('actor', 'event', 'place', 'reference', 'source', 'artifact'))
query.add_argument(
    'system_classes',
    type=str,
    action='append',
    help="{error_msg}",
    case_sensitive=False,
    choices=(
        'acquisition', 'activity', 'actor_appellation', 'administrative_unit',
        'appellation', 'artifact', 'bibliography', 'edition', 'find', 'file',
        'external_reference', 'feature', 'group', 'human_remains', 'move',
        'object_location', 'person', 'place', 'source', 'reference_system',
        'stratigraphic_unit', 'source_translation', 'type'))

image = default.copy()
image.add_argument(
    'image_size',
    type=str,
    help="Not a valid size")
