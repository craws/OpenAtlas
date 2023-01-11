Version 1.0
===========

.. toctree::

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
     - Retrieves the last entered entities. n represents the amount of entities
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
     - Retrieve a list of entities, based on their OpenAtlas type ID including
       all connected subtypes(2)(3)

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
     - Retrieves a list of all OpenAtlas types, sorted by custom, place,
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
   * - /api/1.0/openatlas-classes/
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
       `THANADOS <https://thanados.net>`_ project. This can only be used for
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
