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
    help="{error_msg}",
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
        'type',
        'checkbox',
        'class',
        'created',
        'creator',
        'content',
        'count',
        'description',
        'extension',
        'icon',
        'group',
        'license_holder',
        'license',
        'public',
        'size',
        'begin_from',
        'begin_to',
        'end_from',
        'end_to',
        'end',
        'begin'),
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
    default='lp',
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
    choices=(
        'P43', 'P140', 'P99', 'P112', 'P113', 'P17', 'P104', 'P142',
        'P195', 'P164', 'P129', 'P33', 'P53', 'P42', 'P48', 'P37', 'P182',
        'P132', 'P56', 'P148', 'P150', 'P100', 'P180', 'P98', 'P74', 'P124',
        'P152', 'OA8', 'P20', 'P25', 'P144', 'P2', 'P54', 'P97', 'P34', 'P175',
        'P51', 'P123', 'P55', 'P70', 'P8', 'P11', 'P196', 'P126', 'P105',
        'P44', 'P109', 'P12', 'P9', 'P156', 'P86', 'P111', 'P4', 'P197',
        'P179', 'P128', 'P141', 'P19', 'P65', 'P103', 'P59', 'P183', 'P15',
        'P89', 'P184', 'P94', 'P92', 'P110', 'P16', 'P130', 'P72', 'P1', 'P68',
        'P188', 'P23', 'P125', 'P93', 'P160', 'P50', 'P95', 'P40', 'P62',
        'P198', 'P49', 'P145', 'P139', 'P174', 'P31', 'P28', 'P177', 'P21',
        'P26', 'P5', 'P135', 'P22', 'P14', 'P136', 'P189', 'P137', 'P106',
        'P166', 'P69', 'P27', 'P101', 'P38', 'P35', 'P10', 'P143', 'P173',
        'P75', 'P176', 'P127', 'P108', 'P76', 'P91', 'P24', 'P73', 'P133',
        'P29', 'OA9', 'P191', 'P96', 'P71', 'P165', 'P7', 'P67', 'P161',
        'P186', 'P107', 'P134', 'P146', 'P13', 'P121', 'P46', 'P185', 'P39',
        'P45', 'P32', 'P187', 'P147', 'P157', 'P122', 'P30', 'P52', 'P151',
        'OA7', 'P167', 'P102', 'P41', 'P138'),
    location='args')
entity_.add_argument(
    'centroid',
    type=str,
    case_sensitive=False,
    default='false',
    choices=('true', 'false'),
    location='args')
entity_.add_argument(
    'table_columns',
    type=str,
    action='append',
    help="{error_msg}",
    location='args')
entity_.add_argument(
    'checked',
    type=int,
    action='append',
    help="{error_msg}",
    location='args')

properties = entity_.copy()
properties.add_argument(
    'properties',
    type=str,
    case_sensitive=True,
    action='append',
    default='all',
    choices=(
        'all', 'P43', 'P140', 'P99', 'P112', 'P113', 'P17', 'P104', 'P142',
        'P195', 'P164', 'P129', 'P33', 'P53', 'P42', 'P48', 'P37', 'P182',
        'P132', 'P56', 'P148', 'P150', 'P100', 'P180', 'P98', 'P74', 'P124',
        'P152', 'OA8', 'P20', 'P25', 'P144', 'P2', 'P54', 'P97', 'P34', 'P175',
        'P51', 'P123', 'P55', 'P70', 'P8', 'P11', 'P196', 'P126', 'P105',
        'P44', 'P109', 'P12', 'P9', 'P156', 'P86', 'P111', 'P4', 'P197',
        'P179', 'P128', 'P141', 'P19', 'P65', 'P103', 'P59', 'P183', 'P15',
        'P89', 'P184', 'P94', 'P92', 'P110', 'P16', 'P130', 'P72', 'P1', 'P68',
        'P188', 'P23', 'P125', 'P93', 'P160', 'P50', 'P95', 'P40', 'P62',
        'P198', 'P49', 'P145', 'P139', 'P174', 'P31', 'P28', 'P177', 'P21',
        'P26', 'P5', 'P135', 'P22', 'P14', 'P136', 'P189', 'P137', 'P106',
        'P166', 'P69', 'P27', 'P101', 'P38', 'P35', 'P10', 'P143', 'P173',
        'P75', 'P176', 'P127', 'P108', 'P76', 'P91', 'P24', 'P73', 'P133',
        'P29', 'OA9', 'P191', 'P96', 'P71', 'P165', 'P7', 'P67', 'P161',
        'P186', 'P107', 'P134', 'P146', 'P13', 'P121', 'P46', 'P185', 'P39',
        'P45', 'P32', 'P187', 'P147', 'P157', 'P122', 'P30', 'P52', 'P151',
        'OA7', 'P167', 'P102', 'P41', 'P138'),
    location='args')

presentation = entity_.copy()
presentation.add_argument(
    'remove_empty_values',
    type=str,
    case_sensitive=False,
    default='false',
    choices=('true', 'false'),
    location='args')
presentation.add_argument(
    'place_hierarchy',
    case_sensitive=False,
    type=str,
    default='false',
    choices=('true', 'false'),
    location='args')
presentation.add_argument(
    'map_overlay',
    case_sensitive=False,
    type=str,
    default='false',
    choices=('true', 'false'),
    location='args')

query = entity_.copy()
query.add_argument(
    'entities',
    type=int,
    action='append',
    help="{error_msg}",
    location='args')
query.add_argument(
    'linked_entities',
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

network = default.copy()
network.add_argument(
    'exclude_system_classes',
    type=str,
    help="{error_msg}",
    action='append',
    location='args',
    choices=(
        "acquisition",
        "activity",
        "administrative_unit",
        "appellation",
        "artifact",
        "bibliography",
        "creation",
        "edition",
        "event",
        "external_reference",
        "feature",
        "file",
        "group",
        "human_remains",
        "modification",
        "move",
        "person",
        "place",
        "production",
        "reference_system",
        "source",
        "source_translation",
        "stratigraphic_unit",
        "type",
        "type_tools"))
network.add_argument(
    'linked_to_ids',
    type=int,
    help='{error_msg}',
    action='append',
    location='args')
network.add_argument(
    'depth',
    type=int,
    default=1,
    help='{error_msg}',
    location='args')

iiif = reqparse.RequestParser()
iiif.add_argument(
    'url',
    type=str,
    help='{error_msg}',
    location='args')

openapi = reqparse.RequestParser()
openapi.add_argument(
    'format',
    type=str,
    help='{error_msg}',
    location='args',
    default='json',
    choices=('json', 'yaml'))

search_parser = entity_.copy()
search_parser.add_argument(
    'term',
    type=str,
    default='',
    help='{error_msg}',
    location='args')
