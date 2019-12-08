# This is script is for developing purposes and is not needed to install OpenAtlas.
# CIDOC CRM is used as basis for the underlying data model of OpenAtlas.
# Currently we are using CIDOC CRM v6.2.1
# The rdfs file was downloaded from http://www.cidoc-crm.org/versions-of-the-cidoc-crm

# In this script the rdfs is parsed and entered to a PostgreSQL database
# apt-get install python3-rdflib

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
    def __init__(self, code: str, name: str, comment: str) -> None:
        self.code = code
        self.name = name
        self.comment = comment
        self.label: dict = {}
        self.sub_class_of: list = []


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

        # Translations
        for language in ['de', 'en', 'fr', 'ru', 'el', 'pt', 'zh']:
            translation = graph.preferredLabel(subject, lang=language)
            if translation and translation[0][1]:
                item.label[language] = translation[0][1]

        if code[0] == 'E':
            classes[code] = item
        elif name[0] == 'P':
            properties[code] = item

    # Get subClassOf
    sub_class_triples = graph.triples((None,
                                       URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
                                       None))
    for subject__, predicate__, object__ in sub_class_triples:
        class_ = subject__.replace(CRM_URL, '').split('_', 1)[0]
        sub_class_of = object__.replace(CRM_URL, '').split('_', 1)[0]
        classes[class_].sub_class_of.append(sub_class_of)

    connection = connect()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute("""
        BEGIN;
        ALTER TABLE model.class DROP COLUMN IF EXISTS comment;
        ALTER TABLE model.class ADD COLUMN comment text;
        ALTER TABLE model.entity DROP CONSTRAINT IF EXISTS entity_class_code_fkey;
        ALTER TABLE model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_super_code_fkey;
        ALTER TABLE model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_sub_code_fkey;
        ALTER TABLE model.class_i18n DROP CONSTRAINT IF EXISTS class_i18n_class_code_fkey;
        ALTER TABLE model.property DROP CONSTRAINT IF EXISTS property_range_class_code_fkey;
        ALTER TABLE model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_super_code_fkey;
        ALTER TABLE model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_sub_code_fkey;
        ALTER TABLE model.property_i18n DROP CONSTRAINT IF EXISTS property_i18n_property_code_fkey;
        ALTER TABLE model.property DROP CONSTRAINT IF EXISTS property_domain_class_code_fkey;
        ALTER TABLE model.class_i18n DROP COLUMN IF EXISTS attribute;
        ALTER TABLE model.property_i18n DROP COLUMN IF EXISTS attribute;
        TRUNCATE model.class_inheritance, model.class_i18n, model.class, model.property_inheritance, model.property_i18n;
        ALTER SEQUENCE model.class_id_seq RESTART;
        ALTER SEQUENCE model.class_inheritance_id_seq RESTART;
        ALTER SEQUENCE model.class_i18n_id_seq RESTART;
        ALTER SEQUENCE model.property_id_seq RESTART;
        ALTER SEQUENCE model.property_inheritance_id_seq RESTART;
        ALTER SEQUENCE model.property_i18n_id_seq RESTART;

        """)

    for code, class_ in classes.items():
        sql = 'INSERT INTO model.class (code, name, comment) VALUES (%(code)s, %(name)s, %(comment)s);'
        cursor.execute(sql, {'code': class_.code, 'name': class_.name, 'comment': class_.comment})
    for code, class_ in classes.items():
        for sub_code_of in class_.sub_class_of:
            sql = 'INSERT INTO model.class_inheritance (super_code, sub_code) VALUES (%(super_code)s, %(sub_code)s);'
            cursor.execute(sql, {'super_code': sub_code_of, 'sub_code': class_.code})
    for code, class_ in classes.items():
        for language, label in class_.label.items():
            sql = """
                INSERT INTO model.class_i18n (class_code, language_code, text)
                VALUES (%(class)s, %(language)s, %(text)s);"""
            cursor.execute(sql, {'class': class_.code, 'language': language, 'text': label})

    cursor.execute("""
        ALTER TABLE ONLY model.class_i18n ADD CONSTRAINT class_i18n_class_code_fkey FOREIGN KEY (class_code) REFERENCES model.class(code) ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.class_inheritance ADD CONSTRAINT class_inheritance_sub_code_fkey FOREIGN KEY (sub_code) REFERENCES model.class(code) ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.class_inheritance ADD CONSTRAINT class_inheritance_super_code_fkey FOREIGN KEY (super_code) REFERENCES model.class(code) ON UPDATE CASCADE ON DELETE CASCADE;
        COMMIT;""")

    print('Execution time: ' + str(int(time.time() - start)) + ' seconds')


import_cidoc()
