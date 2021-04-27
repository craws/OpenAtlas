import subprocess
from typing import Dict

from flask import g
from psycopg2 import connect, extras

from openatlas import app

# Script to restructure CONNEC letter data, used locally, using a view to get setup
# Make sure to set database in instance/production.py to openatlas_connec

from openatlas.models.entity import Entity

source_artifact: Dict[int, int] = {}
sources: Dict[int, Entity] = {}
source_type_id = 35
artifact_type_id = 9417
letter_type_root_ids = [38, 1255, 201, 6098, 6103]
invalid_entries_ids = [8998]


@app.route('/connec')
def restructure_connec():
    output = ['Setup database']
    setup()
    letter_type_ids = []
    for type_id in letter_type_root_ids:
        letter_type_ids += [type_id] + g.nodes[type_id].subs
    output.append(f'Letter tye ids: {letter_type_ids}')
    for id_ in letter_type_ids:
        items = g.nodes[id_].get_linked_entities('P2', inverse=True, nodes=True)
        for source in items:
            source_artifact[source.id] = None
            sources[source.id] = source
    output.append(f'Sources with letter type: {len(source_artifact)}')
    insert_artifacts()
    update_types(letter_type_ids)
    output.append(update_links())
    output.append('Done')
    return '<br>'.join(output)


def update_links():
    # Link source to artifact
    sql = ''
    for source_id, artifact_id in source_artifact.items():
        sql += f"""
        INSERT INTO model.link (property_code, domain_id, range_id)
        VALUES ('P128', {artifact_id}, {source_id});"""

    # Change source - move link to artifact - move link
    counter = 0
    invalid = ''
    missing_type = ''
    for move in Entity.get_by_class('move'):
        for link_ in move.get_links('P67', inverse=True):
            if link_.domain.class_.name != 'source':
                invalid += f'invalid id: {link_.domain.id}, class={link_.domain.class_.name}<br>'
            elif link_.domain.id not in source_artifact:
                missing_type += f'missing type?: {link_.domain.id}, class={link_.domain.class_.name}<br>'
            else:
                counter += 1
                sql += f"""
                    UPDATE model.link
                    SET
                        domain_id = {link_.range.id},
                        range_id = {source_artifact[link_.domain.id]},
                        property_code = 'P25'
                    WHERE
                        domain_id = {link_.domain.id}
                        AND range_id = {link_.range.id}
                        AND property_code = 'P67';"""
    g.connec_cursor.execute(sql)
    return f'Move links updated: {counter}.<br>{invalid}<br>{missing_type}'


def insert_artifacts():
    for source in sources.values():
        sql = """
            INSERT INTO model.entity (name, description, system_class, class_code)
            VALUES (%(name)s, %(description)s, 'artifact', 'E33') RETURNING id;"""
        g.connec_cursor.execute(sql, {'name': source.name, 'description': source.description})
        source_artifact[source.id] = g.connec_cursor.fetchone()['id']


def update_types(letter_type_ids):
    sql = ''
    for source_id, artifact_id in source_artifact.items():
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
    for source in sources.values():
        sql += f"""
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES ('P2', {source.id}, {letter_type_id});"""
    g.connec_cursor.execute(sql)


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
