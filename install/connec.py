import time
from typing import Any

from psycopg2 import connect, extras

PASSWORD = 'CHANGE ME'

start = time.time()
connection = connect(
    database='openatlas_connec',
    user='openatlas',
    password=PASSWORD)
connection.autocommit = True
cursor = connection.cursor(cursor_factory=extras.DictCursor)
cursor.execute("BEGIN;")

cursor.execute("""
    SELECT id, range_id, domain_id
    FROM model.link 
    WHERE property_code = 'P117';""")

missing_super_ids = set()
successful_transform = 0
link_count = cursor.rowcount

for row in cursor.fetchall():
    link_id = row['id']
    super_id = row['range_id']
    sub_id = row['domain_id']
    artifact_sql = """
        SELECT range_id
        FROM model.link
        WHERE property_code = 'P25' AND domain_id = %(sub_id)s"""
    cursor.execute(artifact_sql, {'sub_id': sub_id})
    if not cursor.rowcount:
        print(sub_id, 'sub has no artifact')
        missing_super_ids.add(super_id)
        continue
    elif cursor.rowcount > 1:
        print(sub_id, 'sub has too many artifacts')
        continue
    data = cursor.fetchone()
    sub_artifact_id = data['range_id']

    source_sql = """
        SELECT artifact_source.range_id
            FROM model.link artifact_source
            JOIN model.link event_artifact 
                ON artifact_source.domain_id = event_artifact.range_id
                AND event_artifact.property_code = 'P25'
                AND artifact_source.property_code = 'P128'    
            WHERE event_artifact.domain_id = %(super_id)s"""
    cursor.execute(source_sql, {'super_id': super_id})
    if not cursor.rowcount:
        print(super_id, 'super has no source')
        missing_super_ids.add(super_id)
        continue
    elif cursor.rowcount > 1:
        print(super_id, 'super has too many sources')
        continue
    data = cursor.fetchone()
    super_source_id = data['range_id']

    cursor.execute(
        """
        INSERT INTO model.link (domain_id, property_code, range_id)
        VALUES (%(domain_id)s, 'P67', %(range_id)s)""",
        {'domain_id': super_source_id, 'range_id': sub_artifact_id})

    cursor.execute(
        'DELETE FROM model.link WHERE id = %(id)s;',
        {'id': link_id})
    successful_transform += 1
cursor.execute("COMMIT;")

print('links to super found: ', link_count)
print('Successful: ', successful_transform)
print(f'Execution time: {int(time.time() - start)} seconds')
