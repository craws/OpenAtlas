import os
from os.path import basename
from shutil import copyfile

import subprocess
import psycopg2.extras


def connect(database_name):
    db_pass = open('instance/password.txt').read().splitlines()[0]
    connection = psycopg2.connect(
        database=database_name, user='openatlas', password=db_pass, host='localhost')
    connection.autocommit = True
    return connection


def reset_database():
    subprocess.call('dropdb openatlas_dpp', shell=True)
    subprocess.call('createdb openatlas_dpp -O openatlas', shell=True)
    subprocess.call('psql openatlas_dpp < instance/dpp_origin.sql', shell=True)


def prepare_databases(cursor_dpp):

    # Add comment to ostalpen_id
    sql_ = """
        ALTER TABLE model.entity ADD COLUMN ostalpen_id integer;
        COMMENT ON COLUMN model.entity.ostalpen_id IS 'uid of former Ostalpen table tbl_entities'"""
    cursor_dpp.execute(sql_)

    # Add value types
    sql = """
    INSERT INTO model.entity (class_code, name, description) VALUES
        ('E55', 'Width', 'In centimeters'),
        ('E55', 'Length', 'In centimeters'),
        ('E55', 'Thickness', 'In centimeters'),
        ('E55', 'Diameter', 'In centimeters'),
        ('E55', 'Degrees', '360° for full circle');
    INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Width')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Length')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Height')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Thickness')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Diameter')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Weight')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Degrees'));
    INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
    ((SELECT id FROM web.hierarchy WHERE name LIKE 'Dimensions'),(SELECT id FROM web.form WHERE name LIKE 'Stratigraphic Unit')),
    ((SELECT id FROM web.hierarchy WHERE name LIKE 'Dimensions'),(SELECT id FROM web.form WHERE name LIKE 'Feature'));"""
    cursor_dpp.execute(sql)


def datetime64_to_timestamp(date):
    """Converts a numpy.datetime64 to a timestamp string

    :param date: numpy.datetime64
    :return: PostgreSQL timestamp
    """
    string = str(date)
    postfix = ''
    if string.startswith('-') or string.startswith('0000'):
        string = string[1:]
        postfix = ' BC'
    parts = string.split('-')
    year = int(parts[0]) + 1 if postfix else int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    string = format(year, '04d') + '-' + format(month, '02d') + '-' + format(day, '02d')
    return string + postfix


def import_files(cursor_dpp):
    """
        Loops over files in a folder and tries to find the respective entity.
        If successful, the file will be moved into the upload folder.
    """
    import_path = os.path.dirname(__file__) + '/../../../../instance/finds'
    upload_path = os.path.dirname(__file__) + '/../../../../instance/dpp_uploads'
    for file in [f for f in os.listdir(import_path) if os.path.isfile(os.path.join(import_path, f))]:
        name = basename(file).replace('img_', '')
        (new_file_name, ext) = os.path.splitext(name)
        name = new_file_name
        sql = "SELECT id FROM model.entity WHERE LOWER(name) = LOWER(%(name)s) AND class_code = 'E31';"
        cursor_dpp.execute(sql, {'name': name})
        if cursor_dpp.rowcount < 1:
            print('No entity found for file: ' + name)
        elif cursor_dpp.rowcount > 1:
            print('Multiple entites found for file: ' + name)
        else:
            new_file_name = str(cursor_dpp.fetchone().id) + ext.lower()
            copyfile(import_path + '/' + file, upload_path + '/' + new_file_name)
    return


def add_licences(cursor_dpp, cursor_ostalpen):
    sql = """
        SELECT l.links_entity_uid_from, e.entity_name_uri
        FROM openatlas.tbl_links l
        JOIN openatlas.tbl_entities e ON
            l.links_entity_uid_to = e.uid AND
            l.links_cidoc_number_direction = 17;"""
    cursor_ostalpen.execute(sql)
    for row in cursor_ostalpen.fetchall():
        if row.entity_name_uri == 'Public Domain':
            license_name = 'Public domain'
        elif row.entity_name_uri == 'Copyright protected':
            license_name = 'Bildzitat'
        else:
            license_name = 'CC BY-SA'
        sql = """
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES (
                'P2',
                (SELECT id FROM model.entity WHERE ostalpen_id = %(id)s),
                (SELECT id FROM model.entity WHERE name = %(license_name)s));"""
        cursor_dpp.execute(sql, {'id': row.links_entity_uid_from, 'license_name': license_name})
