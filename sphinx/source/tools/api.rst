API
===

.. toctree::

Introduction
------------

This page provides an overview of the OpenAtlas Application Programming
Interface (`API <https://en.wikipedia.org/wiki/API>`_). The API is
`RESTlike <https://restfulapi.net/rest-architectural-constraints/>`_
to provide easy access to the data included.
For an complete overview of possible endpoints and usage of the OpenAtlas API
also visit our
`Swagger documentation <https://app.swaggerhub.com/apis/ctot-nondef/OpenAtlas/>`_.

Quick Start Guide
-----------------

The API can be accessed via the following schema:
**{domain}/api/{api version}/{endpoint}?{parameter}&{parameter}**
Example: **demo.openatlas.eu/api/0.3/entity/5117**

* **Domain**: Location of the OpenAtlas instance from which information should
  be retrieved; e.g. **demo-openatlas.eu/** for the demo-version
* **API Version**: Input without version number leads to the current stable
  version (demo.openatlas.eu/api/entity/5117). If another version of the API is
  to be used, the version number can be specified
  (demo.openatlas.eu/api/**0.3**/entity/5117 or
  demo.openatlas.eu/api/**1**/entity/5117). A version overview can be found
  above under point versioning
* **Endpoint**: Specific data can be queried by attaching an endpoint
  (demo.openatlas.eu/api/0.3/**entity**/5117). The information is provided in a
  human - and machine-readable form, for possible endpoints, see below
* **Required values**: Must be included to create a valid URL; different
  endpoints require different values
  (demo.openatlas.eu/api/0.3/entity/**5117**; 5117 is an ID as required by the
  entity endpoint) - all required values are stated in the list below
* **Parameters**: Used to structure additional information for a given URL;
  they are added to the end of an URL after the "?" symbol
  (demo.openatlas.eu/api/0.3/entity/5117?download=true). For more
  information see this `article <https://www.botify.com/learn/basics/what-are-url-parameters#:~:text=URL%20parameters%20(also%20known%20as,by%20the%20'%26'%20symbol.>`_.

Using the above-mentioned **https://demo.openatlas.eu/api/1/entity/5117**
yields the following result:

..code-block::

  {
    "@context": "https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld",
    "type": "FeatureCollection",
    "features": [
      {
        "@id": "https://demo.openatlas.eu/entity/5117",
        "type": "Feature",
        "crmClass": "crm:E21 Person",
        "systemClass": "person",
        "properties": {
          "title": "Albrecht, Herzog von Sachsen"
        },
        "descriptions": [
          {
            "value": "OGV 96"
          }
        ],
        "when": {
          "timespans": [
            {
              "start": {
                "earliest": "1443-07-31T00:00:00",
                "latest": "None"
              },
              "end": {
                "earliest": "1500-09-12T00:00:00",
                "latest": "None"
              }
            }
          ]
        },
        "types": null,
        "relations": [
          {
            "label": "de Smedt, Chevaliers",
            "relationTo": "https://demo.openatlas.eu/api/0.3/entity/2525",
            "relationType": "crm:P67i is referred to by",
            "relationSystemClass": "bibliography",
            "relationDescription": "Nr. 96",
            "type": null,
            "when": {
              "timespans": [
                {
                  "start": {
                    "earliest": "None",
                    "latest": "None"
                  },
                  "end": {
                    "earliest": "None",
                    "latest": "None"
                  }
                }
              ]
            }
          },
          {
            "label": "Fest des Ordens vom Goldenen Vlies 1478",
            "relationTo": "https://demo.openatlas.eu/api/0.3/entity/5646",
            "relationType": "crm:P11i participated in",
            "relationSystemClass": "activity",
            "relationDescription": "Wahl zum Mitglied",
            "type": "Recipient",
            "when": {
              "timespans": [
                {
                  "start": {
                    "earliest": "1478-04-29T00:00:00",
                    "latest": "None"
                  },
                  "end": {
                    "earliest": "None",
                    "latest": "None"
                  }
                }
              ]
            }
          },
          {
            "label": "Fest des Ordens vom Goldenen Vlies 1481",
            "relationTo": "https://demo.openatlas.eu/api/0.3/entity/5659",
            "relationType": "crm:P11i participated in",
            "relationSystemClass": "activity",
            "relationDescription": "Tag der Wahl",
            "type": "Recipient",
            "when": {
              "timespans": [
                {
                  "start": {
                    "earliest": "1481-05-01T00:00:00",
                    "latest": "1481-05-20T00:00:00"
                  },
                  "end": {
                    "earliest": "None",
                    "latest": "None"
                  }
                }
              ]
            }
          },
          {
            "label": "Fest des Ordens vom Goldenen Vlies 1491",
            "relationTo": "https://demo.openatlas.eu/api/0.3/entity/5570",
            "relationType": "crm:P11i participated in",
            "relationSystemClass": "activity",
            "relationDescription": "Wahl zum neuen Mitglied",
            "type": "Recipient",
            "when": {
              "timespans": [
                {
                  "start": {
                    "earliest": "1491-05-19T00:00:00",
                    "latest": "None"
                  },
                  "end": {
                    "earliest": "1491-05-31T00:00:00",
                    "latest": "None"
                  }
                }
              ]
            }
          },
          {
            "label": "First appearance of Albrecht, Herzog von Sachsen",
            "relationTo": "https://demo.openatlas.eu/api/0.3/entity/15852",
            "relationType": "crm:P11i participated in",
            "relationSystemClass": "activity",
            "relationDescription": null,
            "type": null,
            "when": {
              "timespans": [
                {
                  "start": {
                    "earliest": "None",
                    "latest": "None"
                  },
                  "end": {
                    "earliest": "None",
                    "latest": "None"
                  }
                }
              ]
            }
          },
          {
            "label": "Orden vom Goldenen Vlies",
            "relationTo": "https://demo.openatlas.eu/api/0.3/entity/553",
            "relationType": "crm:P107i is current or former member of",
            "relationSystemClass": "group",
            "relationDescription": null,
            "type": "Member",
            "when": {
              "timespans": [
                {
                  "start": {
                    "earliest": "1430-01-10T00:00:00",
                    "latest": "None"
                  },
                  "end": {
                    "earliest": "None",
                    "latest": "None"
                  }
                }
              ]
            }
          }
        ],
        "names": null,
        "links": null,
        "depictions": null,
        "geometry": {
          "type": "GeometryCollection",
          "geometries": []
        }
      }
    ]
  }

Versioning
----------

The OpenAtlas API follows the notion of
`sequenced based versioning <https://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
and reflects the significance: **major.minor.fix** e.g. **3.11.1**. Only the
**major** number is used for the URL path. **Minor** and **fix** are used for
documentation reasons only with the exeption of versions 0.1, 0.2 and 0.3.
A **stable** version of the API will be available at all times. In addition,
**previous** versions will still be usable but tagged as **deprecated**. A
warning will be posted in the
`roadmap <https://redmine.openatlas.eu/projects/uni/roadmap>`_ and
`release notes <https://redmine.openatlas.eu/projects/uni/news>`_ before
these versions will be discontinued. **Unstable** versions are currently
developed, so breaking changes may occur at any time without prior notice.

Endpoint definition
-------------------

Two different methods are provided to access the OpenAtlas API:

* Access via an OpenAtlas instance's user interface
* Access via another application if settings allow for it

Endpoints provide information about one or more entities in the OpenAtlas
instance. The requested information is provided in Linked Places format
(`LPF <https://github.com/LinkedPasts/linked-places-format>`_). Alternatively,
GeoJSON or RDFs, derived from the LPF data, can be accessed.

Version 1.0
-----------

Entity endpoint
***************

**Single entities**

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/entity/{id}
     - show, download,export,format
     - Retrieves all information about a single entity

**Query** - Combine several or all entity endpoints in one query

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/entities/query/
     - **ids**, **cidoc-classes**, **menu-item**, **classes**,
       **linked-to-entity**, **linked-to-type**,
       **linked-to-type-including-subtypes**, limit, column, sort, search,
       first, last, show, relation-type, type-id, count, download, format,
       export, page
     - Retrieves a list with entity ID, CIDOC CRM code, system class, or menu
       item. Combine up to four of the aforementioned endpoints in a single
       query; each request has to be a new parameter; Possible parameters are:
       entities={id}, classes={cidoc-class-code}, codes={view-name},
       system_classes={system-class}(2)


**Multiple entities** - Results in list form include related entities and
pagination

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/entities/cidoc-class/{cidoc-class}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieve a list of entities, based on their CIDOC CRM class code(1)(2),
       e.g. "E18" or "E22" (see :doc:`CIDOC CRM </model/cidoc_crm>`)
   * - /api/1.0/entities/menu-item/{menu-item}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieves a list of entities based on their OpenAtlas menu items
       (available menu items are: source, event, actor, place, artifact,
       reference, source_translation, file, and type)
   * - /api/1.0/entities/class/{class}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieves a list of entities, based on their OpenAtlas class name
       (available system classes are: acquisition', 'activity',
       'actor_appellation','administrative_unit', 'appellation', 'artifact',
       'bibliography', 'edition', 'external_reference', 'feature','file',
       'find', 'group', 'human_remains', 'move', 'object_location', 'person',
       'place', 'reference_system', 'source', 'stratigraphic_unit',
       'source_translation', 'type')(1)(2).
   * - /api/1.0/entities/last-entered/{n} (n represents a number between 1
       and 100)
     - show, relation-type, download, format, export
     - Retrieves the last entered ebtities. n represents the amount of entities
       retrieved (up to 100). The pagination information is always **null**
   * - /api/1.0/entities/linked-to-entity/{id}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieves a list of entities linked to the stated entity (2)
   * - /api/1.0/entities/linked-to-type/{id}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieves a list of entities based on their OpenAtlas type ID (2)(3).
       For an endpoint that lists all available  types, see "type endpoints"
   * - /api/entities/1.0/linked-to-type-including-subtypes/{id}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieve a list of entities, based on their OpenAtlas type ID including all connected subtypes(2)(3)

(1) All codes available in OpenAtlas can be found under
`OpenAtlas and CIDOC CRM class mapping <https://redmine.openatlas.eu/projects/uni/wiki/OpenAtlas_and_CIDOC_CRM_class_mapping?parent=Endpoints>`_
(2) The result can be filtered, sorted, and manipulated through different
parameters. By default 20 entities in alphabetical order are shown.
(3) Available IDs can be obtained by using the type-tree or node-overview
endpoint.
Required parameters are shown as **bold**.

Type endpoints
**************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/types/hierarchy/
     - download
     - Retrives a list of all OpenAtlas types, sorted by custom, place,
       standard, and value; replaces the older /api/node_overview endpoint
   * - /api/1.0/types/hierarchy/standard/
     - download
     - Retrieves a list of all standard types
   * - /api/1.0/types/hierarchy/value/
     - download
     - Retrieves a list of all value types
   * - /api/1.0/types/hierarchy/custom/
     - download
     - Retrieves a list of all custom types
   * - /api/1.0/types/hierarchy/place/
     - download
     - Retrieves a list of all place types
   * - /api/1.0/types/hierarchy/reference-system/
     - download
     - Retrieves a list of all reference system types
   * - /api/1.0/types/hierarchy/system-types/
     - download
     - Retrieves a list of all system types
   * - /api/1.0/types/list/
     - download
     - Retrieves a list of all OpenAtlas types, including their information

Administrative endpoints
************************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/export-database/{format}
     - none
     - Downloads all information in an OpenAtlas instance as CSV, XML or JSON
   * - api/1.0/openatlas-classes/
     - download
     - Retrieves a list of all available classes, their CIDOC CRM mapping,
       their view, which icon can be used, if aliases and reference systems are
       allowed, which standard type it has, and how many entities are linked
   * - /api/1.0/content/
     - download, lang
     - Retrieves a detailed list of information on available frontend content
       in an OpenAtlas instance - intro, legal, notice, contact, and size of
       processed images
   * - /api/1.0/system-class-count/
     - download
     - Retrieves a detailed list of the number of entities connected to a
       system class

Special entities and output formats
***********************************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/subunits/{id}
     - download, format, count
     - Displays all subunits of a place in a special format as used by the
       `THANADOS <https://thanados.net>`_ project. This cann only be used for
       **Places**. As format only XML can be chosen
   * - /api/1.0/geometric-entities/
     - count, download, geometry
     - Retrieves a **GeoJSON** of all chosen geometries in an OpenAtlas
       instance

Image endpoints
***************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/display/{id}
     - download, image-size
     - Retrieves the respective image if it has a license


:doc:`Version 0.3<api_version0_3>`
----------------------------------

:doc:`Version 0.2<api_version0_2>`
----------------------------------

:doc:`Version 0.1<api_version0_1>`
----------------------------------

Error handling
--------------
OpenAtlas uses conventional HTTP response codes to indicate the success or
failure of an API request. Codes in the 2xx range indicate a successful request
while those in the 4xx range signal an error - providing the information was
not possible. Codes in the 5xx range indicate a server error.
If any issues occur when using the OpenAtlas API, a case-specific error message
is provided in JSON format, describing the error in more detail.

Example:

..code-block::

  {
      “title”: “entity does not exist”,
       “message”: “Requested entity does not exist. Try another ID”
       “timestamp”: “Tue, 19 Jul 2022 13:59:13 GMT”,
       “status”: 404
   }

If an invalid endpoint parameter value e.g. ?sort=kfs instead of ?sort=desc is
entered, Flask catches this via its own
`Flask-RESTful <https://flask-restful.readthedocs.io/en/latest/>`_ extension.
An error message is provided by its own error handler
`error handler <https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling>`_


Authentification guide
----------------------
No authentication is needed to use the OpenAtlas API.



