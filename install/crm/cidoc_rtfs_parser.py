# pylint: disable-all
#
# This script is for developing purposes and not needed to install OpenAtlas.
#
# CIDOC CRM is used as basis for the underlying data model of OpenAtlas.
# Currently, we are using CIDOC CRM 7.1.3 (February 2024):
# https://cidoc-crm.org/Version/version-7.1.3
#
# The script parses the rdfs file and imports it to a PostgreSQL database.
# Installation of needed package:
# apt-get install python3-rdflib
#
# Create a database named cidoc (as postgres user)
# createdb cidoc -O openatlas
# psql cidoc -c "CREATE EXTENSION postgis; CREATE EXTENSION unaccent;"
# cd install
# cat 1_structure.sql 2_data_model.sql | psql -d cidoc -f -
#
# Execute the script:
# cd crm
# python3 cidoc_rtfs_parser.py
#
# Table data can than be extracted to be joined in an upgrade SQL (see last CIDOC upgrade script) with e.g.
# pg_dump --column-inserts --data-only --rows-per-insert=1000 --table=model.cidoc_class cidoc > class.sql
# pg_dump --column-inserts --data-only --rows-per-insert=1000 --table=model.cidoc_class_i18n cidoc > class_i18n.sql
# pg_dump --column-inserts --data-only --rows-per-insert=1000 --table=model.cidoc_class_inheritance cidoc > class_inheritance.sql
# pg_dump --column-inserts --data-only --rows-per-insert=1000 --table=model.property cidoc > property.sql
# pg_dump --column-inserts --data-only --rows-per-insert=1000 --table=model.property_i18n cidoc > property_i18n.sql
# pg_dump --column-inserts --data-only --rows-per-insert=1000 --table=model.property_inheritance cidoc > property_inheritance.sql

# Following has to be added manually to the upgrade SQL
# UPDATE model.property_i18n set text_inverse = 'ist erster Ort von' WHERE property_code = 'OA8' AND language_code = 'de';
# UPDATE model.property_i18n set text_inverse = 'is first appearance of' WHERE property_code = 'OA8' AND language_code = 'en';
# UPDATE model.property_i18n set text_inverse = 'ist letzter Ort von' WHERE property_code = 'OA9' AND language_code = 'de';
# UPDATE model.property_i18n set text_inverse = 'is last appearance of' WHERE property_code = 'OA9' AND language_code = 'en';
#

import time
from typing import Any, Dict, List, Optional

import psycopg2.extras
from rdflib import URIRef
from rdflib.graph import Graph

FILENAME = 'CIDOC_CRM_v7.1.3.rdf'
CRM_URL = 'http://www.cidoc-crm.org/cidoc-crm/'

EXCLUDE_PROPERTIES = [
    'P3', 'P57', 'P79', 'P80', 'P81', 'P81a', 'P81b', 'P82', 'P82a', 'P82b',
    'P90', 'P90a', 'P90b', 'P168', 'P169', 'P170', 'P171', 'P172', 'P190']

DATABASE_NAME = 'cidoc'
DATABASE_USER = 'openatlas'
DATABASE_PORT = '5432'
DATABASE_HOST = 'localhost'
DATABASE_PASS = 'CHANGE ME'


def connect() -> Any:
    return psycopg2.connect(
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        port=DATABASE_PORT,
        host=DATABASE_HOST)


class Item:
    domain_code: str
    range_code: str

    def __init__(self, code: str, name: str, comment: str) -> None:
        self.code = code
        self.name = name
        self.comment = comment
        self.name_inverse: Optional[str] = None
        self.label: Dict[str, str] = {}
        self.sub_class_of: List[str] = []
        self.sub_property_of: List[str] = []


def import_cidoc() -> None:
    start = time.time()
    classes = {}
    properties: Dict[str, Item] = {}
    properties_inverse: Dict[str, Item] = {}
    graph: Any = Graph()
    graph.parse(FILENAME, format='application/rdf+xml')

    # Get classes and properties
    for subject, _predicate, _object in graph:
        try:
            code, name = subject.replace(CRM_URL, '').split('_', 1)
        except Exception:
            print(f'Not able to parse subject: {subject}')
            continue
        item = Item(code, name.replace('_', ' '), graph.comment(subject))

        # Translations
        for language in ['de', 'en', 'fr', 'ru', 'el', 'pt', 'zh']:
            translation = graph.preferredLabel(subject, lang=language)
            if translation and translation[0][1]:
                item.label[language] = translation[0][1]

        if code[0] == 'E':
            classes[code] = item
        elif code[0] == 'P':
            if code in EXCLUDE_PROPERTIES:
                pass
            elif code[-1] == 'i':
                properties_inverse[code[:-1]] = item
            else:
                properties[code] = item

    for code, property_inverse in properties_inverse.items():
        if code in properties:
            properties[code].name_inverse = property_inverse.name
        else:
            print(f'Missing property code: {code}')

    # Get subClassOf
    subs = graph.triples((
        None,
        URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
        None))
    for subject__, _predicate, object__ in subs:
        class_ = subject__.replace(CRM_URL, '').split('_', 1)[0]
        sub_class_of = object__.replace(CRM_URL, '').split('_', 1)[0]
        classes[class_].sub_class_of.append(sub_class_of)

    # Get subPropertyOf
    subs = graph.triples((
        None,
        URIRef('http://www.w3.org/2000/01/rdf-schema#subPropertyOf'),
        None))
    for subject__, _predicate, object__ in subs:
        property_ = subject__.replace(CRM_URL, '').split('_', 1)[0]
        if property_[-1] == 'i' or property_ in EXCLUDE_PROPERTIES:
            continue
        sub_property_of = object__.replace(CRM_URL, '').split('_', 1)[0]
        sub_property_of = sub_property_of.replace('i', '')  # P10i, P130i, P59i
        properties[property_].sub_property_of.append(sub_property_of)

    # Get domain for properties
    domains = graph.triples((
        None,
        URIRef('http://www.w3.org/2000/01/rdf-schema#domain'),
        None))
    for subject__, _predicate, object__ in domains:
        property_ = subject__.replace(CRM_URL, '').split('_', 1)[0]
        if property_[-1] == 'i' or property_ in EXCLUDE_PROPERTIES:
            continue
        properties[property_].domain_code = \
            object__.replace(CRM_URL, '').split('_', 1)[0]

    # Get range for properties
    ranges = graph.triples((
        None,
        URIRef('http://www.w3.org/2000/01/rdf-schema#range'),
        None))
    for subject__, _predicate, object__ in ranges:
        property_ = subject__.replace(CRM_URL, '').split('_', 1)[0]
        if property_[-1] == 'i' or property_ in EXCLUDE_PROPERTIES:
            continue
        properties[property_].range_code = \
            object__.replace(CRM_URL, '').split('_', 1)[0]

    # OpenAtlas shortcuts
    properties['OA7'] = Item(
        'OA7',
        'has relationship to',
        'OA7 is used to link two Actors (E39) via a certain relationship E39 '
        'Actor linked with E39 Actor: E39 (Actor) - P11i (participated in) - '
        'E5 (Event) - P11 (had participant) - E39 (Actor) Example: [ Stefan '
        '(E21)] participated in [ Relationship from Stefan to Joachim (E5)] '
        'had participant [Joachim (E21)] The connecting event is defined by '
        'an entity of class E55 (Type): [Relationship from Stefan to Joachim '
        '(E5)] has type [Son to Father (E55)]')
    properties['OA7'].domain_code = 'E39'
    properties['OA7'].range_code = 'E39'
    properties['OA7'].label = {
        'en': 'has relationship to',
        'de': 'hat Beziehung zu'}
    properties['OA8'] = Item(
        'OA8',
        'begins in',
        "OA8 is used to link the beginning of a persistent item's (E77) life "
        "span (or time of usage) with a certain place. E.g to document the "
        "birthplace of a person. E77 Persistent Item linked with a E53 Place: "
        "E77 (Persistent Item) - P92i (was brought into existence by) - E63 "
        "(Beginning of Existence) - P7 (took place at) - E53 (Place) Example: "
        "[Albert Einstein (E21)] was brought into existence by [Birth of "
        "Albert Einstein (E12)] took place at [Ulm (E53)]")
    properties['OA8'].name_inverse = 'is first appearance of'
    properties['OA8'].domain_code = 'E77'
    properties['OA8'].range_code = 'E53'
    properties['OA8'].label = {'en': 'begins in', 'de': 'beginnt in'}

    properties['OA9'] = Item(
        'OA9',
        'ends in',
        "OA9 is used to link the end of a persistent item's (E77) life span "
        "(or time of usage) with a certain place. E.g to document a person's "
        "place of death. E77 Persistent Item linked with a E53 Place: E77 "
        "(Persistent Item) - P93i (was taken out of existence by) - E64 "
        "(End of Existence) - P7 (took place at) - E53 (Place) Example: "
        "[Albert Einstein (E21)] was taken out of by [Death of Albert "
        "Einstein (E12)] took place at [Princeton (E53)]")
    properties['OA9'].name_inverse = 'is last appearance of'
    properties['OA9'].domain_code = 'E77'
    properties['OA9'].range_code = 'E53'
    properties['OA9'].label = {'en': 'ends in', 'de': 'endet in'}

    connection = connect()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute("""
        BEGIN;

        ALTER TABLE model.entity 
            DROP CONSTRAINT IF EXISTS entity_class_code_fkey;
        ALTER TABLE model.entity 
            DROP CONSTRAINT IF EXISTS entity_openatlas_class_name_fkey;
        ALTER TABLE model.link 
            DROP CONSTRAINT IF EXISTS link_property_code_fkey;
        ALTER TABLE model.cidoc_class_inheritance 
            DROP CONSTRAINT IF EXISTS class_inheritance_super_code_fkey;
        ALTER TABLE model.cidoc_class_inheritance 
            DROP CONSTRAINT IF EXISTS class_inheritance_sub_code_fkey;
        ALTER TABLE model.cidoc_class_i18n 
            DROP CONSTRAINT IF EXISTS class_i18n_class_code_fkey;
        ALTER TABLE model.property 
            DROP CONSTRAINT IF EXISTS property_domain_class_code_fkey;
        ALTER TABLE model.property 
            DROP CONSTRAINT IF EXISTS property_range_class_code_fkey;
        ALTER TABLE model.property_inheritance 
            DROP CONSTRAINT IF EXISTS property_inheritance_super_code_fkey;
        ALTER TABLE model.property_inheritance 
            DROP CONSTRAINT IF EXISTS property_inheritance_sub_code_fkey;
        ALTER TABLE model.property_i18n 
            DROP CONSTRAINT IF EXISTS property_i18n_property_code_fkey;
        ALTER TABLE model.openatlas_class 
            DROP CONSTRAINT IF EXISTS openatlas_class_cidoc_class_code_fkey;
        ALTER TABLE web.reference_system_openatlas_class 
            DROP CONSTRAINT IF EXISTS 
                reference_system_openatlas_class_openatlas_class_name_fkey;

        TRUNCATE 
            model.cidoc_class_inheritance,
            model.cidoc_class_i18n,
            model.cidoc_class,
            model.property_inheritance,
            model.property_i18n,
            model.property;

        ALTER SEQUENCE model.cidoc_class_id_seq RESTART;
        ALTER SEQUENCE model.cidoc_class_inheritance_id_seq RESTART;
        ALTER SEQUENCE model.cidoc_class_i18n_id_seq RESTART;
        ALTER SEQUENCE model.property_id_seq RESTART;
        ALTER SEQUENCE model.property_inheritance_id_seq RESTART;
        ALTER SEQUENCE model.property_i18n_id_seq RESTART;""")

    # Classes
    for code, class_ in classes.items():
        sql = """
            INSERT INTO model.cidoc_class (code, name, comment)
            VALUES (%(code)s, %(name)s, %(comment)s);"""
        cursor.execute(sql, {
            'code': class_.code,
            'name': class_.name,
            'comment': class_.comment})
    for code, class_ in classes.items():
        for sub_code_of in class_.sub_class_of:
            if sub_code_of != class_.code:  # Prevent circular relations
                sql = """
                    INSERT INTO model.cidoc_class_inheritance
                        (super_code, sub_code)
                    VALUES (%(super_code)s, %(sub_code)s);"""
                cursor.execute(sql, {
                    'super_code': sub_code_of,
                    'sub_code': class_.code})
        for language, label in class_.label.items():
            sql = """
                INSERT INTO model.cidoc_class_i18n
                    (class_code, language_code, text)
                VALUES (%(class)s, %(language)s, %(text)s);"""
            cursor.execute(sql, {
                'class': class_.code,
                'language': language,
                'text': label})

    # Properties
    for code, property_ in properties.items():
        sql = """
            INSERT INTO model.property (
                code, name, name_inverse, comment, domain_class_code,
                range_class_code)
            VALUES (
                %(code)s, %(name)s, %(name_inverse)s, %(comment)s,
                %(domain_code)s, %(range_code)s);"""
        cursor.execute(sql, {
            'code': property_.code,
            'name': property_.name,
            'name_inverse': property_.name_inverse,
            'comment': property_.comment,
            'domain_code': property_.domain_code,
            'range_code': property_.range_code})
    for code, property_ in properties.items():
        for sub_property_of in property_.sub_property_of:
            sql = """
                INSERT INTO model.property_inheritance (super_code, sub_code)
                VALUES (%(super_code)s, %(sub_code)s);"""
            cursor.execute(sql, {
                'super_code': sub_property_of,
                'sub_code': property_.code})

        for language, label in property_.label.items():
            text_inverse = None
            if property_.code in properties_inverse \
                    and language in properties_inverse[property_.code].label:
                text_inverse = \
                    properties_inverse[property_.code].label[language]
            sql = """
                INSERT INTO model.property_i18n
                    (property_code, language_code, text, text_inverse)
                VALUES
                    (%(property)s, 
                    %(language)s, 
                    %(text)s, 
                    %(text_inverse)s);"""
            cursor.execute(sql, {
                'property': property_.code,
                'language': language,
                'text': label,
                'text_inverse': text_inverse})
    cursor.execute("""
        ALTER TABLE ONLY model.entity 
            ADD CONSTRAINT entity_class_code_fkey 
            FOREIGN KEY (cidoc_class_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.link 
            ADD CONSTRAINT link_property_code_fkey 
            FOREIGN KEY (property_code) 
            REFERENCES model.property(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.cidoc_class_inheritance 
            ADD CONSTRAINT class_inheritance_super_code_fkey 
            FOREIGN KEY (super_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.cidoc_class_inheritance 
            ADD CONSTRAINT class_inheritance_sub_code_fkey 
            FOREIGN KEY (sub_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.cidoc_class_i18n 
            ADD CONSTRAINT class_i18n_class_code_fkey 
            FOREIGN KEY (class_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.property 
            ADD CONSTRAINT property_domain_class_code_fkey 
            FOREIGN KEY (domain_class_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.property 
            ADD CONSTRAINT property_range_class_code_fkey 
            FOREIGN KEY (range_class_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.property_inheritance 
            ADD CONSTRAINT property_inheritance_super_code_fkey 
            FOREIGN KEY (super_code) 
            REFERENCES model.property(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.property_inheritance 
            ADD CONSTRAINT property_inheritance_sub_code_fkey 
            FOREIGN KEY (sub_code) 
            REFERENCES model.property(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.property_i18n 
            ADD CONSTRAINT property_i18n_property_code_fkey 
            FOREIGN KEY (property_code) 
            REFERENCES model.property(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.entity 
            ADD CONSTRAINT entity_openatlas_class_name_fkey 
            FOREIGN KEY (openatlas_class_name) 
            REFERENCES model.openatlas_class(name) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY model.openatlas_class 
            ADD CONSTRAINT openatlas_class_cidoc_class_code_fkey 
            FOREIGN KEY (cidoc_class_code) 
            REFERENCES model.cidoc_class(code) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        ALTER TABLE ONLY web.reference_system_openatlas_class 
            ADD CONSTRAINT 
            reference_system_openatlas_class_openatlas_class_name_fkey 
            FOREIGN KEY (openatlas_class_name) 
            REFERENCES model.openatlas_class(name) 
            ON UPDATE CASCADE ON DELETE CASCADE;
        """)
    cursor.execute("COMMIT")
    print(f'Execution time: {int(time.time() - start)} seconds')


import_cidoc()
