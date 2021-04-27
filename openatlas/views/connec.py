import subprocess

from flask import g
from psycopg2 import connect, extras

from openatlas import app

# Script to restructure CONNEC letter data, used locally, using a view to get setup
# Make sure to set database in instance/production.py to openatlas_connec

# To do
# add case study to artifact form
# copy case study types from source to artifacts
# create source - artifact links
# create artifact - move event links
# delete source - move event links
# make manual page for entering letters

# Check
# got all letters? which types are still needed (ask CONNEC, check move event sources)
# relevant custom types which should move from source to artifact?
from openatlas.models.entity import Entity
from openatlas.models.link import Link

source_type_id = 35
artifact_type_id = 9417
letter_type_root_ids = [38, 1255]


@app.route('/connec')
def restructure_connec():
    output = ['Setup database']
    setup()
    letter_type_ids = letter_type_root_ids + g.nodes[38].subs + g.nodes[1255].subs
    output.append(f'Letter tye ids: {letter_type_ids}')
    letter_sources = []
    for id_ in letter_type_ids:
        letter_sources += g.nodes[id_].get_linked_entities('P2', inverse=True, nodes=True)
    output.append(f'Sources with letter type: {len(letter_sources)}')
    source_artifact_ids = insert_artifacts(letter_sources)
    update_types(source_artifact_ids, letter_type_ids, letter_sources)
    output.append('Done')
    return '<br>'.join(output)


def update_types(source_artifact_ids, letter_type_ids, letter_sources):
    sql = ''
    for source_id, artifact_id in source_artifact_ids.items():
        sql += f"""
            UPDATE model.link SET domain_id = {artifact_id} 
            WHERE 
                domain_id = {source_id} 
                AND property_code = 'P2'
                AND range_id in {tuple(letter_type_ids)};"""
    # Move letter root types from source super to artifact super
    for id_ in letter_type_root_ids:
        sql += f"""
            UPDATE model.link SET range_id = {artifact_type_id}
            WHERE property_code = 'P127' AND domain_id = {id_} AND range_id = {source_type_id};"""
    g.connec_cursor.execute(sql)

    # Create source type "letter", connect entries
    sql = """
        INSERT INTO model.entity (name, system_class, class_code)
        VALUES ('Letter', 'type', 'E55') RETURNING id;"""
    g.connec_cursor.execute(sql)
    letter_type_id = g.connec_cursor.fetchone()['id']
    sql = f"""
        INSERT INTO model.link (property_code, domain_id, range_id)
        VALUES ('P127', {letter_type_id}, {source_type_id});"""
    for letter in letter_sources:
        sql += f"""
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES ('P2', {letter.id}, {letter_type_id});"""
    g.connec_cursor.execute(sql)


def insert_artifacts(letters):
    source_artifact_ids = {}
    for letter in letters:
        sql = """
            INSERT INTO model.entity (name, description, system_class, class_code)
            VALUES (%(name)s, %(description)s, 'artifact', 'E33') RETURNING id;"""
        g.connec_cursor.execute(sql, {'name': letter.name, 'description': letter.description})
        source_artifact_ids[letter.id] = g.connec_cursor.fetchone()['id']
    return source_artifact_ids


def setup():
    commands = [
        'dropdb openatlas_connec_test',
        'createdb openatlas_connec_test -O openatlas',
        'psql openatlas_connec_test < instance/connec.sql']
    for command in commands:
        subprocess.Popen(command, shell=True, stdin=subprocess.PIPE).wait()
    g.connec_db = connect(
        database='openatlas_connec_test',
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASS'],
        port=app.config['DATABASE_PORT'],
        host=app.config['DATABASE_HOST'])
    g.connec_db.autocommit = True
    g.connec_cursor = g.connec_db.cursor(cursor_factory=extras.DictCursor)
