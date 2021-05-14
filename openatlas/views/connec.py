import subprocess
from typing import Any, Dict

from flask import g
from psycopg2 import connect, extras

from openatlas import app
from openatlas.models.entity import Entity

# Script to restructure CONNEC letter data, used locally, using a view to get setup
# How to:
# Place fresh online SQL dump to instance/connec.sql
# Set database in instance/production.py to openatlas_connec
# http://127.0.0.1:5000/connec - to start script
# To view results switch database in instance/production.oy to openatlas_connec_test

source_artifact: Dict[int, Any] = {}
sources: Dict[int, Entity] = {}
source_move_links = []
artifact_type_id = 9417
move_ids_to_ignore = [
    8220, 8383, 8436, 8585, 8593, 8597, 8614, 8631, 8660, 8675, 8811, 8817, 8820, 8830, 8831, 8837,
    8870, 8880, 9075, 9078, 9195, 9238, 9241, 9243, 9246, 9252, 9268, 9275, 9276, 9279, 9280, 9281,
    9283, 9284, 9285, 9286, 9294, 9299, 9300, 9301, 9313, 9314, 9317, 9320, 9321, 9336, 9341, 9344]


@app.route('/connec')
def restructure_connec():
    output = ['Setup database']
    setup()
    sql = """
        SELECT m.id AS move_id, l.id AS link_id, s.id AS source_id, m.system_class
        FROM model.entity m
        JOIN model.link l ON l.range_id = m.id
            AND l.property_code = 'P67'
            AND m.system_class = 'move'
        JOIN model.entity s ON l.domain_id = s.id
        WHERE m.id NOT IN %(ignore_ids)s;"""
    g.cursor.execute(sql, {'ignore_ids': tuple(move_ids_to_ignore)})
    for row in g.cursor.fetchall():
        source_move_links.append({
            'move_id': row['move_id'],
            'link_id': row['link_id'],
            'source_id': row['source_id']})
    for link_ in source_move_links:
        if link_['source_id'] not in source_artifact:
            source_artifact[link_['source_id']] = None
    for source in Entity.get_by_ids(source_artifact.keys(), nodes=True):
        sources[source.id] = source
    output.append(f'Links for moves: {len(source_move_links)}')
    output.append(f'Sources for moves: {len(sources)}')
    insert_artifacts()
    add_artifact_letter_type()
    copy_case_study_type_links()
    output.append(update_links())
    output.append('Done')
    return '<br>'.join(output)


def copy_case_study_type_links():
    # Link case study to artefact form
    g.connec_cursor.execute(
        "INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES (137, 20);")
    sql = ''
    for source_id, source in sources.items():
        for node in source.nodes:
            if node.root and node.root[-1] == 137:
                sql += f"""
                    INSERT INTO model.link(property_code, domain_id, range_id)
                    VALUES ('P2', {source_artifact[source_id]}, {node.id});"""
    g.connec_cursor.execute(sql)


def update_links():
    # Link source to artifact
    sql = ''
    for source_id, artifact_id in source_artifact.items():
        sql += f"""
        INSERT INTO model.link (property_code, domain_id, range_id)
        VALUES ('P128', {artifact_id}, {source_id});"""

    # Change "source - move link" to "artifact - move link"
    counter = 0
    missing_type = ''
    for link_ in source_move_links:
        if link_['source_id'] not in sources:
            missing_type += \
                f'missing type?: {link_.domain.id}, class={link_.domain.class_.name}<br>'
            continue
        counter += 1
        sql += f"""
            UPDATE model.link
            SET
                domain_id = {link_['move_id']},
                range_id = {source_artifact[link_['source_id']]},
                property_code = 'P25'
            WHERE
                domain_id = {link_['source_id']}
                AND range_id = {link_['move_id']}
                AND property_code = 'P67';"""
    g.connec_cursor.execute(sql)
    return f'Move links updated: {counter}<br>{missing_type}'


def insert_artifacts():
    for source in sources.values():
        sql = """
            INSERT INTO model.entity (name, description, system_class, class_code)
            VALUES (%(name)s, %(description)s, 'artifact', 'E22') RETURNING id;"""
        g.connec_cursor.execute(sql, {'name': source.name, 'description': source.description})
        artifact_id = g.connec_cursor.fetchone()['id']
        source_artifact[source.id] = artifact_id
        sql = """
            INSERT INTO model.entity (name, system_class, class_code)
            VALUES (%(name)s, 'object_location', 'E53') RETURNING id;"""
        g.connec_cursor.execute(sql, {'name': 'Location of ' + source.name})
        location_id = g.connec_cursor.fetchone()['id']
        sql = f"""
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES ('P53', {artifact_id}, {location_id})"""
        g.connec_cursor.execute(sql)


def add_artifact_letter_type():  # Create artifact type "letter", connect entries
    sql = """
        INSERT INTO model.entity (name, system_class, class_code)
        VALUES ('Letter', 'type', 'E55') RETURNING id;"""
    g.connec_cursor.execute(sql)
    letter_type_id = g.connec_cursor.fetchone()['id']
    sql = f"""
        INSERT INTO model.link (property_code, domain_id, range_id)
        VALUES ('P127', {letter_type_id}, {artifact_type_id});"""
    for artifact_id in source_artifact.values():
        sql += f"""
            INSERT INTO model.link (property_code, domain_id, range_id)
            VALUES ('P2', {artifact_id}, {letter_type_id});"""
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
