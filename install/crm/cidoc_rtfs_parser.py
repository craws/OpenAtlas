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


def import_cidoc():  # pragma: no cover
    start = time.time()
    classes = []
    properties = []

    graph = Graph()
    graph.parse(FILENAME, format='application/rdf+xml')

    for subject, predicate, object_ in graph:
        code, name = subject.replace(CRM_URL, '').split('_', 1)
        name = name.replace('_', ' ')
        print(name)
        print(code)
        label = graph.preferredLabel(subject, lang='de')[0][1]
        print(label)

        if name[0] == 'E':
            classes.append(object_)
        elif name[0] == 'P':
            properties.append(object_)
        break

        #print(subject)
        #print(predicate)
        # print(object_)




    #connection = connect()
    #cursor = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    #cursor.execute('BEGIN;')
    #cursor.execute('COMMIT;')
    print('Execution time: ' + str(int(time.time() - start)) + ' seconds')


import_cidoc()
