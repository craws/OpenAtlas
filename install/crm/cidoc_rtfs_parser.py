# Created by Alexander Watzinger and others. Please see README.md for licensing information

# This is script is for developing purposes and is not needed to install OpenAtlas.
# CIDOC CRM is used as basis for the underlying data model of OpenAtlas.
# Currently we are using CIDOC CRM v6.2.1
# The rdfs file was downloaded from http://www.cidoc-crm.org/versions-of-the-cidoc-crm

# In this script the rdfs is parsed and entered to a PostgreSQL database
# apt-get install python3-rdflib

# Todo: Add and document shortcuts

import time

import psycopg2.extras
from rdflib import URIRef
from rdflib.graph import Graph

FILENAME = 'cidoc_crm_v6.2.1.rdfs'
CRM_URL = 'http://www.cidoc-crm.org/cidoc-crm/'

DATABASE_NAME = 'cidoc'
DATABASE_USER = 'openatlas'
DATABASE_PORT = '5432'
DATABASE_HOST = 'localhost'
DATABASE_PASS = 'CHANGE ME'


def connect():
    try:
        connection_ = psycopg2.connect(database=DATABASE_NAME, user=DATABASE_USER,
                                       password=DATABASE_PASS, port=DATABASE_PORT,
                                       host=DATABASE_HOST)
        return connection_
    except Exception as e:  # pragma: no cover
        print("Database connection error.")
        raise Exception(e)


class Item:
    def __init__(self, code, name, comment) -> None:
        self.code = code
        self.name = name
        self.comment = comment
        self.label = {}


def import_cidoc():  # pragma: no cover
    start = time.time()
    classes = {}
    properties = {}
    graph = Graph()
    graph.parse(FILENAME, format='application/rdf+xml')

    # Get classes and properties
    for subject, predicate, object_ in graph:
        code, name = subject.replace(CRM_URL, '').split('_', 1)
        item = Item(code, name.replace('_', ' '), graph.comment(subject))
        # for language in ['de', 'en', 'fr', 'ru', 'el', 'pt', 'zh']:
        #    translation = graph.preferredLabel(subject, lang=language)
        #    if translation:
        #        item.label[language] = translation[0][1]
        if code[0] == 'E':
            classes[code] = item
        elif name[0] == 'P':
            properties[code] = item
        # print(item.label['en'])
        # print(item.label['de'])

    # Get all subClassOf
    # sub_class_triples = graph.triples((None,
    #                                   URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
    #                                   None))
    # for subject__, predicate__, object__ in sub_class_triples:
        # pprint(subject__.replace(CRM_URL, '').split('_', 1)[0])
        # pprint(object__.replace(CRM_URL, '').split('_', 1)[0])

    connection = connect()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('BEGIN;')
    cursor.execute("""
        ALTER TABLE IF EXISTS ONLY model.entity DROP CONSTRAINT IF EXISTS entity_class_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_super_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_sub_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.class_i18n DROP CONSTRAINT IF EXISTS class_i18n_class_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.property DROP CONSTRAINT IF EXISTS property_range_class_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_super_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_sub_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.property_i18n DROP CONSTRAINT IF EXISTS property_i18n_property_code_fkey;
        ALTER TABLE IF EXISTS ONLY model.property DROP CONSTRAINT IF EXISTS property_domain_class_code_fkey;
        TRUNCATE model.class_inheritance, model.class_i18n, model.class, model.property_inheritance,
            model.property_i18n;""")

    for code, class_ in classes.items():
        print(class_.code)
        print(class_.name)
        print(class_.comment)
        sql = 'INSERT INTO model.class (code, name, comment) VALUES (%(code)s, %(name)s, %(comment)s);'
        cursor.execute(sql, {'code': class_.code, 'name': class_.name, 'comment': class_.comment})

    cursor.execute('COMMIT;')

    print('Execution time: ' + str(int(time.time() - start)) + ' seconds')


import_cidoc()
