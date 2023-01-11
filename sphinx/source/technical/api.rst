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
  under point versioning
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

.. code-block::

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
documentation reasons only with the exception of versions 0.1, 0.2 and 0.3.
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

.. toctree::
   :maxdepth: 1

   Version 0.3 (current) <api_version0_3>
   api_version0_2
   api_version0_1
   Version 1.0 (in development) <api_version1_0>

Parameter definition
--------------------

.. list-table::
   :widths: 20 15 45 20
   :header-rows: 1

   * - Parameter
     - Format
     - Description
     - Values
   * - cidoc_class/cidoc_classes/cidoc-class/cidoc-classes
     - string
     - CIDOC CRM class code (e.g. E21)
     -
   * - column
     - string
     - Results will be sorted by the given column
     - * ID
       * classCode
       * name
       * description
       * created
       * modified
       * systemClass
       * beginFrom
       * beginTo
       * endFrom
       * endTo
   * - count
     - boolean
     - Returns the total count of results as integer
     - True/False
   * - download
     - boolean
     - Triggers file download of the requested data in a file
     - True/False
   * - entities
     - integer
     - Specific entity ID
     -
   * - export
     - string
     - Results will be downloaded in the given format
     - * csv
       * csvNetwork
   * - first
     - integer
     - List of results starting with given ID
     -
   * - format
     - string
     - Select a preferred output format
     -  * lp
        * geojson
        * geojson-v2
        * pretty-xml
        * n3
        * turtle
        * nt
        * xml (subunits endpoint can only handle xml)
   * - geometry
     - string
     - Select a preferred geometry
     -  * gisAll
        * gisPointAll
        * gisPointSupers
        * gisPointSubs
        * gisPointSibling
        * gisLineAll
        * gisPolygonAll
   * - id
     - integer
     - Specific entity ID in OpenAtlas instance
     -
   * - image-size/image_size
     - string
     - Select the size category for the displayed image (can be modified in production.py)
     - * thumbnail
       * table
   * - lang
     - string
     - Select an output language
     - * en
       * de
   * - last
     - integer
     - JSON list of results start with entity after given ID
     -
   * - latest
     - integer
     - Number of last database entries to be returned; only numbers between 1 and 100 are valid
     - 1 - 100
   * - limit
     - integer
     - Number of entities returned per page
     - * 0 corresponds to "no limit set"
       * Default is set to 20 entities
   * - none
     -
     - No parameters are required
     -
   * - page
     - integer
     - Jump to chosen page
     -
   * - relation_type/relation-type
     - string
     - Select which relations are shown
     - E.g. P53
   * - search
     - string
     - Search request with AND/OR logic
     -
   * - show
     - string
     - Select a key to be shown. If using "not", no other keys will be displayed.
     -  * description
        * depictions
        * geometry
        * links
        * names
        * not
        * relations
        * types
        * when
   * - sort
     - string
     - Results will be sorted asc/desc (default column is name)
     -  * asc
        * desc
   * - system_class/system_classes/system-class/system-classes
     - string
     - Needs to be one of the OpenAtlas system classes
     -  * all
        * administrative_unit
        * type
        * acquisition
        * activity
        * actor_actor_relation
        * actor_function
        * appellation
        * artifact
        * bibliography
        * edition
        * external_reference
        * feature
        * file
        * group
        * human_remains
        * involvement
        * move
        * object_location
        * person
        * place
        * production
        * reference_system
        * source
        * source_translation
        * stratigraphic_unit
   * - type_id/type-id
     - integer
     - Output will be filtered by chosen type ID and only entities with this type ID will be displayed; the relation is in logical OR
     -
   * - view_class/view_classes/view-class/view-classes
     - string
     - Needs to be one of the OpenAtlas menu items
     -  * actor
        * all
        * artifact
        * event
        * file
        * object
        * place
        * reference
        * source
        * source_translation
        * type


Error handling
--------------
OpenAtlas uses conventional HTTP response codes to indicate the success or
failure of an API request. Codes in the 2xx range indicate a successful request
while those in the 4xx range signal an error - providing the information was
not possible. Codes in the 5xx range indicate a server error.
If any issues occur when using the OpenAtlas API, a case-specific error message
is provided in JSON format, describing the error in more detail.

Example:

.. code-block::

  {
      "title": "entity does not exist",
       "message": "Requested entity does not exist. Try another ID"
       "timestamp": "Tue, 19 Jul 2022 13:59:13 GMT",
       "status": 404
   }

If an invalid endpoint parameter value e.g. ?sort=kfs instead of ?sort=desc is
entered, Flask catches this via its own
`Flask-RESTful <https://flask-restful.readthedocs.io/en/latest/>`_ extension.
An error message is provided by its own error handler
`error handler <https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling>`_


Authentication guide
--------------------
No authentication is needed to use the OpenAtlas API.
