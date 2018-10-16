# This script is for merging data from the DPP and Ostalpen project
import copy
import os
import sys
import time

import numpy
import psycopg2.extras
from functions.scripts import (connect, prepare_databases, reset_database, datetime64_to_timestamp,
    import_files, add_licences)

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

do_import_files = False
dict_units = {24: 'Millimeter', 22: 'Meter', 23: 'Centimeter'}

class Entity:
    dim = {}
    system_type = None


start = time.time()
ostalpen_user_id = 38
ostalpen_type_id = 11821

reset_database()

connection_dpp = connect('openatlas_dpp')
connection_ostalpen = connect('ostalpen')
cursor_dpp = connection_dpp.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
cursor_ostalpen = connection_ostalpen.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

prepare_databases(cursor_dpp)

def link(property_code, domain_id, range_id, description=None):
    sql = """
        INSERT INTO model.link (property_code, domain_id, range_id, description)
        VALUES (
            %(property_code)s,
            %(domain_id)s,
            %(range_id)s,
            %(description)s)
        RETURNING id;"""
    cursor_dpp.execute(sql, {
        'property_code': property_code,
        'domain_id': domain_id,
        'range_id': range_id,
        'description': description})
    return cursor_dpp.fetchone()[0]


def link_property(domain_id, type_name):
    sql = """
        INSERT INTO model.link_property (property_code, domain_id, range_id)
        VALUES ('P2', %(domain_id)s, (SELECT id FROM model.entity WHERE name = %(type_name)s))
        RETURNING id;"""
    cursor_dpp.execute(sql,{'domain_id': domain_id, 'type_name': type_name})
    return cursor_dpp.fetchone()[0]


def insert_entity(e, with_case_study=False):
    sql = """
        INSERT INTO model.entity (name, description, class_code, system_type, ostalpen_id, created)
        VALUES (%(name)s, %(description)s, %(class_code)s, %(system_type)s, %(ostalpen_id)s,
            %(created)s)
        RETURNING id;"""
    description = e.description
    dates_comment = ''
    if e.class_code == 'E33':
        dates_comment += e.start_time_text if e.start_time_text else ''
        dates_comment += (' ' + str(e.start_time_abs)) if e.start_time_abs else ''
        if e.end_time_text or e.end_time_abs:
            dates_comment += ' bis '
            dates_comment += e.end_time_text if e.end_time_text else ''
            dates_comment += (' ' + str(e.end_time_abs)) if e.end_time_abs else ''
        if description and dates_comment:
            description = dates_comment + ': ' + description
        elif dates_comment:
            description = dates_comment

    cursor_dpp.execute(sql, {
        'name': e.name,
        'ostalpen_id': e.ostalpen_id,
        'description': description,
        'class_code': e.class_code,
        'created': e.created,
        'system_type': e.system_type})
    e.id = cursor_dpp.fetchone()[0]
    sql = """
        INSERT INTO web.user_log (user_id, action, entity_id, created)
        VALUES (%(ostalpen_user_id)s, 'insert', %(entity_id)s, %(created)s);"""
    cursor_dpp.execute(sql, {
        'ostalpen_user_id': ostalpen_user_id, 'entity_id': e.id, 'created': e.created})
    if with_case_study:
        sql = """
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
        cursor_dpp.execute(sql, {
            'property_code': 'P2', 'domain_id': e.id, 'range_id': ostalpen_type_id})

    if e.class_code != 'E53':
        for dim_label, dim_value in e.dim.items():
            if dim_value:
                if dim_label in ('Width', 'Length', 'Height', 'Thickness', 'Diameter'):
                    try:
                        if e.units == 'Millimeter':
                            dim_value = str(int(dim_value) / 10)
                        if e.units == 'Meter':
                            dim_value = str(int(dim_value) * 100)
                    except Exception as e:
                        print('Error to convert "' + dim_value + '" of id: ' + str(e.id))
                sql = """
                    INSERT INTO model.link (property_code, domain_id, range_id, description)
                    VALUES ('P2', %(domain_id)s, (SELECT id FROM model.entity WHERE name = %(dim_label)s AND class_code = 'E55'), %(dim_value)s);"""
                cursor_dpp.execute(sql, {'domain_id': e.id, 'dim_label': dim_label, 'dim_value': dim_value})

    # Dates
    if e.class_code not in ['E33', 'E53']:
        if e.start_time_abs:
            year = e.start_time_abs
            year = format(year, '03d') if year > 0 else format(year + 1, '04d')
            from_date = datetime64_to_timestamp(numpy.datetime64(year + '-01-01'))
            to_date = datetime64_to_timestamp(numpy.datetime64(year + '-12-31'))
            sql = """
                INSERT INTO model.entity (name, value_timestamp, description, class_code, system_type)
                VALUES (%(value_timestamp)s, %(value_timestamp)s, %(description)s, 'E61', 'from date value')
                    RETURNING id;"""
            cursor_dpp.execute(sql, {
                'value_timestamp': from_date,
                'description': e.start_time_text if e.start_time_text else None})
            from_date_id = cursor_dpp.fetchone()[0]
            sql = """
                INSERT INTO model.link (property_code, domain_id, range_id)
                VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
            cursor_dpp.execute(sql, {
                'property_code': 'OA5' if e.class_code in ('E7', 'E8') else 'OA1',
                'domain_id': e.id,
                'range_id': from_date_id})
            sql = """
                INSERT INTO model.entity (name, value_timestamp, class_code, system_type)
                VALUES (%(value_timestamp)s, %(value_timestamp)s, 'E61', 'to date value')
                    RETURNING id;"""
            cursor_dpp.execute(sql, {'value_timestamp': to_date})
            to_date_id = cursor_dpp.fetchone()[0]
            sql = """
                INSERT INTO model.link (property_code, domain_id, range_id)
                VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
            cursor_dpp.execute(sql, {
                'property_code': 'OA5' if e.class_code in ('E7', 'E8') else 'OA1',
                'domain_id': e.id,
                'range_id': to_date_id})
        if e.end_time_abs:
            year = e.end_time_abs
            year = format(year, '03d') if year > 0 else format(year + 1, '04d')
            from_date = datetime64_to_timestamp(numpy.datetime64(year + '-01-01'))
            to_date = datetime64_to_timestamp(numpy.datetime64(year + '-12-31'))
            sql = """
                INSERT INTO model.entity (name, value_timestamp, description, class_code, system_type)
                VALUES (%(value_timestamp)s, %(value_timestamp)s, %(description)s, 'E61', 'from date value')
                    RETURNING id;"""
            cursor_dpp.execute(sql, {
                'value_timestamp': from_date,
                'description': e.end_time_text if e.end_time_text else None})
            from_date_id = cursor_dpp.fetchone()[0]
            sql = """
                INSERT INTO model.link (property_code, domain_id, range_id)
                VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
            cursor_dpp.execute(sql, {
                'property_code': 'OA6' if e.class_code in ('E7', 'E8') else 'OA2',
                'domain_id': e.id,
                'range_id': from_date_id})
            sql = """
                INSERT INTO model.entity (name, value_timestamp, class_code, system_type)
                VALUES (%(value_timestamp)s, %(value_timestamp)s, 'E61', 'to date value')
                    RETURNING id;"""
            cursor_dpp.execute(sql, {'value_timestamp': to_date})
            to_date_id = cursor_dpp.fetchone()[0]
            sql = """
                INSERT INTO model.link (property_code, domain_id, range_id)
                VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
            cursor_dpp.execute(sql, {
                'property_code': 'OA6' if e.class_code in ('E7', 'E8') else 'OA2',
                'domain_id': e.id,
                'range_id': to_date_id})

    # Types for places
    if e.system_type in ('feature', 'stratigraphic unit', 'find', 'place'):
        if not e.entity_type or e.entity_type in [1, 2, 3, 4]:
            pass
        elif e.entity_type not in ostalpen_place_types:
            missing_ostalpen_place_types.add(e.entity_type)
        else:
            sql = """
                INSERT INTO model.link (property_code, domain_id, range_id) VALUES 
                ('P2', %(id)s, (SELECT id FROM model.entity WHERE ostalpen_id = %(type_id)s));"""
            cursor_dpp.execute(sql, {'id': e.id, 'type_id': e.entity_type})

    return e.id


# Counters
new_entities = {}
missing_classes = {}
count = {
    'Gis point': 0,
    'E21 person': 0,
    'E18 place': 0,
    'E31 document': 0,
    'E33 source': 0,
    'E33 translation': 0,
    'E33 original text': 0,
    'E40 legal body': 0,
    'E74 group': 0,
    'E7 event': 0,
    'E8 acquisition': 0}

# Get DPP types
types = {}
types_double = {}
cursor_dpp.execute("SELECT id, name FROM model.entity WHERE class_code = 'E55';")
for row in cursor_dpp.fetchall():
    if row.name in types:
        types_double[row.name] = row.id
    types[row.name] = row.id

# Get Ostalpen types
ostalpen_types = {}
ostalpen_place_types = []
missing_ostalpen_place_types = set()
ostalpen_types_double = {}
material_types = {}
cursor_ostalpen.execute("SELECT uid, entity_name_uri FROM openatlas.tbl_entities WHERE classes_uid = 13;")
for row in cursor_ostalpen.fetchall():
    if row.entity_name_uri in ostalpen_types:
        ostalpen_types_double[row.uid] = row.entity_name_uri
    ostalpen_types[row.uid] = row.entity_name_uri


def insert_type_subs(openatlas_id, ostalpen_id, root):
    sql = """
        SELECT uid, entity_name_uri FROM openatlas.tbl_entities e
        JOIN openatlas.tbl_links l ON
            e.uid = l.links_entity_uid_from
            AND l.links_cidoc_number_direction = 7
            AND l.links_entity_uid_to = {id};""".format(id=ostalpen_id)
    cursor_ostalpen.execute(sql)
    for row in cursor_ostalpen.fetchall():
        sql = """
            INSERT INTO model.entity (class_code, name, ostalpen_id) VALUES ('E55', '{name}', {uid}) 
            RETURNING id;""".format(name=row.entity_name_uri, uid=row.uid)
        cursor_dpp.execute(sql)
        sub_id = cursor_dpp.fetchone()[0]
        link('P127', sub_id, openatlas_id)
        if root == 'Material':
            sql = """
                UPDATE model.entity SET description = 'weight percentage (0 = unknown)'
                WHERE id = {id};""".format(id=sub_id)
            cursor_dpp.execute(sql)
            material_types[row.uid] = sub_id
        else:
            ostalpen_place_types.append(row.uid)
        insert_type_subs(sub_id, row.uid, root)


# Archeological Subunits
for root in ['Feature', 'Finds', 'Stratigraphical Unit', 'Material']:
    sql = """
        SELECT uid, entity_name_uri FROM openatlas.tbl_entities e
        JOIN tbl_links l ON
            e.uid = l.links_entity_uid_from
            AND l.links_cidoc_number_direction = 7
            AND l.links_entity_uid_to = 
                (SELECT uid FROM openatlas.tbl_entities WHERE entity_name_uri = '{root}');
        """.format(root=root)
    cursor_ostalpen.execute(sql)
    for row in cursor_ostalpen.fetchall():
        if root == 'Finds':
            root = 'Find'
        elif root == 'Stratigraphical Unit':
            root = 'Stratigraphic Unit'
        sql = """
            INSERT INTO model.entity (class_code, name, ostalpen_id) VALUES ('E55', '{name}', {uid}) 
            RETURNING id;""".format(name=row.entity_name_uri, uid=row.uid)
        if row.entity_name_uri in ostalpen_types:
            ostalpen_types_double[row.uid] = row.entity_name_uri
        ostalpen_place_types.append(row.uid)
        cursor_dpp.execute(sql)
        id_ = cursor_dpp.fetchone()[0]
        sql = """
            INSERT INTO model.link(property_code, range_id, domain_id) VALUES ('P127', 
            (SELECT id FROM model.entity WHERE name = '{root}' AND class_code = 'E55'), {id});
            """.format(root=root, id=id_)
        cursor_dpp.execute(sql)
        insert_type_subs(id_, row.uid, root)


# Administrative Units
def insert_place_subs(ostalpen_id, dpp_id):
    sql = """
    SELECT l.links_entity_uid_from, e.entity_name_uri AS name, e.entity_description, e.uid
    FROM openatlas.tbl_links l
    JOIN openatlas.tbl_entities e ON l.links_entity_uid_from = e.uid
    WHERE l.links_entity_uid_to = %(ostalpen_id)s AND l.links_cidoc_number_direction = 5;"""
    cursor_ostalpen.execute(sql, {'ostalpen_id': ostalpen_id})
    for row in cursor_ostalpen.fetchall():
        sql = """
            INSERT INTO model.entity (class_code, name, description, ostalpen_id)
            VALUES('E53', %(name)s, %(description)s, %(ostalpen_id)s) RETURNING id;"""
        cursor_dpp.execute(sql, {'name': row.name, 'description': row.entity_description,
                                 'ostalpen_id': row.uid})
        new_dpp_id = cursor_dpp.fetchone()[0]
        sql = """
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES ('P89', %(new_dpp_id)s, %(dpp_id)s);"""
        cursor_dpp.execute(sql, {'new_dpp_id': new_dpp_id, 'dpp_id': dpp_id})
        insert_place_subs(row.links_entity_uid_from, new_dpp_id)

for root in ['Burgenland', 'Kärnten', 'Niederösterreich', 'Oberösterreich', 'Salzburg',
             'Steiermark', 'Tirol', 'Vorarlberg', 'Wien']:
    sql = 'SELECT uid FROM openatlas.tbl_entities WHERE entity_name_uri = %(root)s;'
    cursor_ostalpen.execute(sql, {'root': root})
    uid = cursor_ostalpen.fetchone()[0]
    sql = """
        UPDATE model.entity SET ostalpen_id = %(ostalpen_id)s
        WHERE name = %(name)s RETURNING id;"""
    cursor_dpp.execute(sql, {'ostalpen_id': uid, 'name': root})
    insert_place_subs(uid, cursor_dpp.fetchone()[0])


# Get ostalpen entities
sql_ = """
    SELECT
        uid, entity_name_uri, cidoc_class_nr, entity_type, entity_description, start_time_abs,
        end_time_abs, start_time_text, end_time_text, timestamp_creation, entity_id,
        dim_width, dim_length, dim_height, dim_thickness, dim_diameter, dim_weight, dim_degrees,
        dim_units
    FROM openatlas.tbl_entities e
    JOIN openatlas.tbl_classes c ON e.classes_uid = c.tbl_classes_uid;"""
cursor_ostalpen.execute(sql_)
entities = []
for row in cursor_ostalpen.fetchall():
    if not row.entity_name_uri:
        continue
    e = Entity()
    e.entity_type = row.entity_type
    e.created = row.timestamp_creation
    e.id_name = row.entity_id
    e.ostalpen_id = row.uid
    e.name = row.entity_name_uri.replace('\n', ' ').replace('\r', ' ')
    e.description = row.entity_description
    e.class_code = row.cidoc_class_nr
    e.start_time_text = row.start_time_text
    e.start_time_abs = row.start_time_abs
    e.end_time_text = row.end_time_text
    e.end_time_abs = row.end_time_abs
    e.units = dict_units[int(row.dim_units)] if row.dim_units else None
    e.dim = {
        'Width': row.dim_width,
        'Length': row.dim_length,
        'Height': row.dim_height,
        'Thickness': row.dim_thickness,
        'Diameter': row.dim_diameter,
        'Weight': row.dim_weight,
        'Degrees': row.dim_degrees}
    entities.append(e)

print('Entities')
for e in entities:
    with_case_study = True
    if e.class_code == 'E021':  # Person
        e.class_code = 'E21'
        count['E21 person'] += 1
    elif e.class_code == 'E033':  # Linguistic Object (Source)
        if e.id_name.startswith('tbl_2_quelle_original'):
            e.system_type = 'source translation'
            count['E33 translation'] += 1
        elif e.id_name.startswith('tbl_2_quelle_uebersetzung'):
            e.system_type = 'source translation'
            count['E33 original text'] += 1
        else:
            e.system_type = 'source content'
            count['E33 source'] += 1
        e.class_code = 'E33'
        with_case_study = True if e.system_type == 'source content' else False
    elif e.class_code == 'E074':  # Group
        e.class_code = 'E74'
        count['E74 group'] += 1
    elif e.class_code == 'E040':  # Legal body
        e.class_code = 'E40'
        count['E40 legal body'] += 1
    elif e.class_code == 'E005':  # Event
        e.class_code = 'E7'
        count['E7 event'] += 1
    elif e.class_code == 'E008':  # Acquisition
        e.class_code = 'E8'
        count['E8 acquisition'] += 1
    elif e.class_code == 'E031':
        e.class_code = 'E31'
        if e.entity_type in [10, 11]:  # Scientific Literature, text
            e.system_type = 'bibliography'
        elif e.entity_type in [11232, 11179, 11180]:  # File (map, photo, drawing)
            if '.' not in e.name:
                continue  # There are two bogus files which are skipped
            (new_file_name, ext) = os.path.splitext(e.name)
            e.name = new_file_name
            e.system_type = 'file'
        elif e.entity_type == 12:  # These 23 have to be checked manually
            continue
        else:
            print('missing id for E031 type:' + str(e.entity_type))
            continue
        count['E31 document'] += 1
    elif e.class_code in ['E018', 'E053', 'E055', 'E052', 'E004', 'E058', 'E030', 'E019', 'E057']:
        continue  # Places and other stuff will be added later in script
    else:
        missing_classes[e.class_code] = e.class_code
        continue
    insert_entity(e, with_case_study=with_case_study)
    new_entities[e.ostalpen_id] = e

print('Places')
sql_ = """
    SELECT
        uid, entity_name_uri, entity_type, entity_description, start_time_abs, srid_epsg,
        end_time_abs, start_time_text, end_time_text, timestamp_creation, name_path,
        x_lon_easting, y_lat_northing,
        dim_width, dim_length, dim_height, dim_thickness, dim_diameter, dim_degrees, dim_units
    FROM openatlas.sites;"""
cursor_ostalpen.execute(sql_)
places = []
for row in cursor_ostalpen.fetchall():
    if not row.entity_name_uri:
        continue
    e = Entity()
    e.entity_type = row.entity_type
    e.created = row.timestamp_creation
    e.ostalpen_id = row.uid
    e.name = row.entity_name_uri.replace('\n', ' ').replace('\r', ' ')
    e.description = row.entity_description
    e.start_time_text = row.start_time_text
    e.start_time_abs = row.start_time_abs
    e.end_time_text = row.end_time_text
    e.end_time_abs = row.end_time_abs
    e.srid_epsg = row.srid_epsg
    e.x = row.x_lon_easting
    e.y = row.y_lat_northing
    e.units = dict_units[int(row.dim_units)] if row.dim_units else None
    e.dim = {
        'Width': row.dim_width,
        'Length': row.dim_length,
        'Height': row.dim_height,
        'Thickness': row.dim_thickness,
        'Diameter': row.dim_diameter,
        'Degrees': row.dim_degrees}
    places.append(e)

for e in places:
    e.class_code = 'E18'
    e.system_type = 'place'
    object_id = insert_entity(e, with_case_study=True)
    new_entities[e.ostalpen_id] = e
    p = copy.copy(e)
    p.system_type = 'place location'
    p.class_code = 'E53'
    p.name = 'Location of ' + e.name
    location_id = insert_entity(p)
    link('P53', object_id, location_id)
    if e.srid_epsg == 32633 and e.x and e.y:
        sql = """
        INSERT INTO gis.point (name, entity_id, type, created, geom)
        VALUES ('', %(entity_id)s, 'centerpoint', %(created)s,(
            SELECT ST_SetSRID(ST_Transform(ST_GeomFromText('POINT({x} {y})',32633),4326),4326)
        ))""".format(x=e.x, y=e.y)
        cursor_dpp.execute(sql, {'entity_id': location_id, 'created': e.created})
        count['Gis point'] += 1
    count['E18 place'] += 1

print('Features')
sql_ = """
    SELECT
        uid, entity_name_uri, entity_type, entity_description, start_time_abs, srid_epsg,
        end_time_abs, start_time_text, end_time_text, timestamp_creation, name_path,
        x_lon_easting, y_lat_northing,
        dim_width, dim_length, dim_height, dim_thickness, dim_diameter, dim_degrees, dim_units
    FROM openatlas.features;"""
cursor_ostalpen.execute(sql_)
features = []
for row in cursor_ostalpen.fetchall():
    if not row.entity_name_uri:
        continue
    e = Entity()
    e.entity_type = row.entity_type
    e.created = row.timestamp_creation
    e.ostalpen_id = row.uid
    e.name = row.entity_name_uri.replace('\n', ' ').replace('\r', ' ')
    e.description = row.entity_description
    e.start_time_text = row.start_time_text
    e.start_time_abs = row.start_time_abs
    e.end_time_text = row.end_time_text
    e.end_time_abs = row.end_time_abs
    e.srid_epsg = row.srid_epsg
    e.x = row.x_lon_easting
    e.y = row.y_lat_northing
    e.units = dict_units[int(row.dim_units)] if row.dim_units else None
    e.dim = {
        'Width': row.dim_width,
        'Length': row.dim_length,
        'Height': row.dim_height,
        'Thickness': row.dim_thickness,
        'Diameter': row.dim_diameter,
        'Degrees': row.dim_degrees}
    features.append(e)

for e in features:
    e.class_code = 'E18'
    e.system_type = 'feature'
    object_id = insert_entity(e, with_case_study=True)
    if e.entity_type:
        sql = "INSERT INTO model.link VALUES "
    new_entities[e.ostalpen_id] = e
    p = copy.copy(e)
    p.system_type = 'place location'
    p.class_code = 'E53'
    p.name = 'Location of ' + p.name
    location_id = insert_entity(p)
    link('P53', object_id, location_id)
    if e.srid_epsg and e.x and e.y:
        sql = """
        INSERT INTO gis.point (name, entity_id, type, created, geom)
        VALUES ('', %(entity_id)s, 'centerpoint', %(created)s,(
            SELECT ST_SetSRID(ST_Transform(ST_GeomFromText('POINT({x} {y})',32633),4326),4326)
        ))""".format(x=e.x, y=e.y)
        cursor_dpp.execute(sql, {'entity_id': location_id, 'created': e.created})
        count['Gis point'] += 1
    count['E18 place'] += 1

print('Stratigraphic units')
sql_ = """
    SELECT
        uid, entity_name_uri, entity_type, entity_description, start_time_abs, srid_epsg,
        end_time_abs, start_time_text, end_time_text, timestamp_creation, name_path,
        x_lon_easting, y_lat_northing,
        dim_width, dim_length, dim_height, dim_thickness, dim_diameter, dim_weight, dim_degrees, dim_units
    FROM openatlas.stratigraphical_units;"""
cursor_ostalpen.execute(sql_)
strati = []
for row in cursor_ostalpen.fetchall():
    if not row.entity_name_uri:
        continue
    e = Entity()
    e.entity_type = row.entity_type
    e.created = row.timestamp_creation
    e.ostalpen_id = row.uid
    e.name = row.entity_name_uri.replace('\n', ' ').replace('\r', ' ')
    e.description = row.entity_description
    e.start_time_text = row.start_time_text
    e.start_time_abs = row.start_time_abs
    e.end_time_text = row.end_time_text
    e.end_time_abs = row.end_time_abs
    e.srid_epsg = row.srid_epsg
    e.x = row.x_lon_easting
    e.y = row.y_lat_northing
    e.units = dict_units[int(row.dim_units)] if row.dim_units else None
    e.dim = {
        'Width': row.dim_width,
        'Length': row.dim_length,
        'Height': row.dim_height,
        'Thickness': row.dim_thickness,
        'Diameter': row.dim_diameter,
        'Weight': row.dim_weight,
        'Degrees': row.dim_degrees}
    strati.append(e)

for e in strati:
    e.class_code = 'E18'
    e.system_type = 'stratigraphic unit'
    object_id = insert_entity(e, with_case_study=True)
    new_entities[e.ostalpen_id] = e
    p = copy.copy(e)
    p.system_type = 'place location'
    p.class_code = 'E53'
    p.name = 'Location of ' + e.name
    location_id = insert_entity(p)
    link('P53', object_id, location_id)
    if e.srid_epsg and e.x and e.y:
        sql = """
        INSERT INTO gis.point (name, entity_id, type, created, geom)
        VALUES ('', %(entity_id)s, 'centerpoint', %(created)s,(
            SELECT ST_SetSRID(ST_Transform(ST_GeomFromText('POINT({x} {y})',32633),4326),4326)
        ))""".format(x=e.x, y=e.y)
        cursor_dpp.execute(sql, {'entity_id': location_id, 'created': e.created})
        count['Gis point'] += 1
    count['E18 place'] += 1

print('Finds')
sql_ = """
    SELECT
        uid, entity_name_uri, entity_type, entity_description, start_time_abs, srid_epsg,
        end_time_abs, start_time_text, end_time_text, timestamp_creation, name_path,
        x_lon_easting, y_lat_northing,
        dim_width, dim_length, dim_height, dim_thickness, dim_diameter, dim_weight, dim_degrees, dim_units
    FROM openatlas.finds;"""
cursor_ostalpen.execute(sql_)
finds = []
for row in cursor_ostalpen.fetchall():
    if not row.entity_name_uri:
        continue
    e = Entity()
    e.entity_type = row.entity_type
    e.created = row.timestamp_creation
    e.ostalpen_id = row.uid
    e.name = row.entity_name_uri.replace('\n', ' ').replace('\r', ' ')
    e.description = row.entity_description
    e.start_time_text = row.start_time_text
    e.start_time_abs = row.start_time_abs
    e.end_time_text = row.end_time_text
    e.end_time_abs = row.end_time_abs
    e.srid_epsg = row.srid_epsg
    e.x = row.x_lon_easting
    e.y = row.y_lat_northing
    e.units = dict_units[int(row.dim_units)] if row.dim_units else None
    e.dim = {
        'Width': row.dim_width,
        'Length': row.dim_length,
        'Height': row.dim_height,
        'Thickness': row.dim_thickness,
        'Diameter': row.dim_diameter,
        'Weight': row.dim_weight,
        'Degrees': row.dim_degrees}
    finds.append(e)

for e in finds:
    e.class_code = 'E22'
    e.system_type = 'find'
    object_id = insert_entity(e, with_case_study=True)
    new_entities[e.ostalpen_id] = e
    p = copy.copy(e)
    p.system_type = 'place location'
    p.class_code = 'E53'
    p.name = 'Location of ' + e.name
    location_id = insert_entity(p)
    link('P53', object_id, location_id)
    if e.srid_epsg and e.x and e.y:
        sql = """
        INSERT INTO gis.point (name, entity_id, type, created, geom)
        VALUES ('', %(entity_id)s, 'centerpoint', %(created)s,(
            SELECT ST_SetSRID(ST_Transform(ST_GeomFromText('POINT({x} {y})',32633),4326),4326)
        ))""".format(x=e.x, y=e.y)
        cursor_dpp.execute(sql, {'entity_id': location_id, 'created': e.created})
        count['Gis point'] += 1
    count['E18 place'] += 1

print('Links')
missing_properties = set()
invalid_type_links = set()
missing_dpp_types = set()
missing_source_link = set()
missing_actor_function = set()
sql_ = """
    SELECT links_uid, links_entity_uid_from, links_cidoc_number_direction, links_entity_uid_to,
        links_annotation, links_creator, links_timestamp_start, links_timestamp_end,
        links_timestamp_creation, links_timespan
    FROM openatlas.tbl_links;"""
cursor_ostalpen.execute(sql_)
for row in cursor_ostalpen.fetchall():
    if row.links_cidoc_number_direction == 33:  # has translation
        domain = new_entities[row.links_entity_uid_from]
        range_ = new_entities[row.links_entity_uid_to]
        if domain.id_name.startswith('tbl_2_quelle_original'):
            link('P73', range_.id, domain.id, row.links_annotation)
            link('P2', domain.id, types['Original text'])
        elif domain.id_name.startswith('tbl_2_quelle_uebersetzung'):
            link('P73', range_.id, domain.id, row.links_annotation)
            link('P2', domain.id, types['Translation'])
        else:
            print('Error missing translation type, id: ' + str(domain.id) + ', ' + domain.id_name)
    elif row.links_cidoc_number_direction == 4:  # documents
        if row.links_entity_uid_to not in new_entities or \
                row.links_entity_uid_from not in new_entities:
                    missing_source_link.add(row.links_uid)
                    continue
        domain = new_entities[row.links_entity_uid_to]
        range_ = new_entities[row.links_entity_uid_from]
        link('P67', domain.id, range_.id ,row.links_annotation)
    elif row.links_cidoc_number_direction == 11:  # subunits
        if row.links_entity_uid_to not in new_entities:
            print('Missing subunit for a link (11, to) for: ' + str(row.links_entity_uid_to))
            continue
        if row.links_entity_uid_from not in new_entities:
            print('Missing subunit for a link (11, from) for: ' + str(row.links_entity_uid_from))
            continue
        domain = new_entities[row.links_entity_uid_to]
        range_ = new_entities[row.links_entity_uid_from]
        link('P46', range_.id, domain.id, row.links_annotation)
    elif row.links_cidoc_number_direction == 1:  # types
        if row.links_entity_uid_to in material_types:
            domain = new_entities[row.links_entity_uid_from]
            link('P2', domain.id, material_types[row.links_entity_uid_to], '0')
            continue
        if row.links_entity_uid_to in ostalpen_place_types:
            continue  # archeological types done with links are invalid
        if row.links_entity_uid_to not in ostalpen_types:
            invalid_type_links.add(row.links_entity_uid_to)
            continue
        type_name = ostalpen_types[row.links_entity_uid_to]
        if row.links_entity_uid_to in ostalpen_types_double:
            print('Double Ostalpen type: ' + type_name)
            continue
        if type_name in types_double:
            print('Use of DPP double type: ' + type_name)
            continue
        if type_name not in types:
            missing_dpp_types.add(type_name)
            continue
        if row.links_entity_uid_from not in new_entities:
            print('Missing entity for type with Ostalpen ID: ' + str(row.links_entity_uid_from))
            continue
        domain = new_entities[row.links_entity_uid_from]
        link('P2', domain.id, types[type_name])
    elif row.links_cidoc_number_direction == 36:
        if row.links_entity_uid_to not in new_entities or row.links_entity_uid_from not in new_entities:
            print('Missing entity for member link id: ' + str(row.links_uid))
            continue
        domain = new_entities[row.links_entity_uid_to]
        range_ = new_entities[row.links_entity_uid_from]
        member_link_id = link('P107', domain.id, range_.id)
        type_id = None
        if row.links_annotation:
            try:
                type_id = int(row.links_annotation)
            except:
                pass
        if type_id:
            if type_id not in ostalpen_types:
                print('Missing type id for actor function:' + str(type_id))
            else:
                type_name = ostalpen_types[type_id]
                if type_name not in types:
                    missing_actor_function.add(type_name)
                else:
                    link_property(member_link_id, type_name)
    elif row.links_cidoc_number_direction == 15:
        sql = """
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES ('P89',
                (SELECT id FROM model.entity WHERE ostalpen_id = %(domain_id)s AND system_type = 'place location'),
                (SELECT id FROM model.entity WHERE ostalpen_id = %(range_id)s));"""
        try:
            id_to = row.links_entity_uid_to
            if id_to == 416:
                id_to = 100
            elif id_to == 417:
                id_to = 99
            elif id_to == 414:
                id_to = 101
            elif id_to == 412:
                id_to = 97
            cursor_dpp.execute(sql, {'domain_id': row.links_entity_uid_from, 'range_id': id_to})
        except:
            pass
    elif row.links_cidoc_number_direction in [2, 5, 7, 9, 13, 17, 19, 25]:
        pass  # Ignore obsolete links
    else:
        missing_properties.add(row.links_cidoc_number_direction)

# Files
if do_import_files:
    add_licences(cursor_dpp, cursor_ostalpen)
    import_files(cursor_dpp)

if missing_classes:
    print('Missing classes:' + ', '.join(missing_classes))
if missing_properties:
    print('Missing property ids:')
    print(missing_properties)
if missing_ostalpen_place_types:
    print('Missing place types:')
    print(missing_ostalpen_place_types)
if missing_actor_function:
    print('Missing actor function:')
    print(missing_actor_function)
if invalid_type_links:
    print('Invalid type links:')
    print(invalid_type_links)
if missing_dpp_types:
    print('Missing DPP types:')
    print(missing_dpp_types)
if missing_source_link:
    print('Missing source links (links_uid):')
    print(missing_source_link)

for name, count in count.items():
    print(str(name) + ': ' + str(count))

connection_dpp.close()
connection_ostalpen.close()
print('Execution time: ' + str(round((time.time()-start)/60, 2)) + ' minutes')
