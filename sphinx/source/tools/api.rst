API
===

.. toctree::

Introduction
------------

This page provides an overview of the OpenAtlas Application Programming
Interface (`API <https://en.wikipedia.org/wiki/API>`_). The API provided is
`RESTlike <https://restfulapi.net/rest-architectural-constraints/>`_
to provide easy access to the data included.
For an complete overview of possible endpoints and usage of the OpenAtlas API
also visit our
`Swagger documentation <https://app.swaggerhub.com/apis/ctot-nondef/OpenAtlas/0.3/>`_.

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
  they are added to the end of an URL after the “?” symbol
  (demo.openatlas.eu/api/0.3/entity/5117**?download=true**). For more
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

* Access via an OpenAtlas instance’s user interface
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
       ?entities={id}, ?classes={cidoc_class_code}, ?codes={view_name},
       ?system_classes={system_class}(2)


**Multiple entities** - Results in list form include related entities and
       pagination

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/1.0/entities/cidoc-class/
       {cidoc-class}
     - limit, column, sort, search, first, last, show, relation-type, type-id,
       count, download, format, export, page
     - Retrieve a list of entities, based on their CIDOC CRM class code(1)(2),
       e.g. “E18” or “E22” (see :doc:`CIDOC CRM </model/cidoc_crm>`)
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




Version 0.3
-----------


