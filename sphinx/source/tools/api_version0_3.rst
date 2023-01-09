Version 0.3
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
   * - /api/0.3/entity/{id}
     - show, download,export,format
     - Retrieves all information about a single entity

**Query** - Combine several or all entity endpoints in one query

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - api/0.3/entities/query/
     - **ids**, **cidoc-classes**, **menu-item**, **classes**,
       **linked-to-entity**, **linked-to-type**,
       **linked-to-type-including-subtypes**, limit, column, sort, search,
       first, last, show, relation_type, type_id, count, download, format,
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
   * - /api/0.3/view_class/{view_class}
     - limit, column, sort, search, first, last, show, relation_type, type_id,
       count, download, format, export, page
     - Used to retrieve a JSON list of entities based on their OpenAtlas class
       view
   * - /api/0.3/system_class/{system_class}
     - limit, column, sort, search, first, last, show, relation_type, count,
       download, format, export, page
     - Retrieves a list of entities, based on their OpenAtlas system class name
       as JSON (1)(2)
   * - /api/0.3/latest/{n} (n represents a number between 1 and 100)
     - show, relation_type, download, format, export
     - Used to retrieve the last entry/entries made; the number {latest}/{n}
       represents the amount of entities retrieved and can be between 1 and
       100. The pagination information is always **null**
   * - /api/0.3/entities_linked_to_entity/{id}
     - limit, column, sort, search, first, last, show, relation_type, type_id,
       count, download, format, export, page
     - Used to retrieve a JSON list of entities linked to the entity with the
       stated **ID** (2)
   * - /api/0.3/type_entities/{id}
     - limit, column, sort, search, first, last, show, relation_type, type_id,
       count, download, format, export, page
     - Used to retrieve a JSON list of entities, based on their OpenAtlas
       **type** (2)(3)
   * - /api/0.3/type_entities_all/{id}
     - limit, column, sort, search, first, last, show, relation_type, type_id,
       count, download, format, export, page
     - Used to retrieve a JSON list of entities, based on their OpenAtlas
       **type** and includes all connected entities (2)(3)
   * - /api/3.0/cidoc_class/{cidoc_class}
     - limit, column, sort, search, first, last, show, relation_type, type_id,
       count, download, format, export, page
     - Retrieves a JSON list of entities based on their CIDOC CRM class(1)(2)

(1) All codes available in OpenAtlas can be found under
`OpenAtlas and CIDOC CRM class mapping <https://redmine.openatlas.eu/projects/uni/wiki/OpenAtlas_and_CIDOC_CRM_class_mapping?parent=Endpoints>`_
(2) The result can be filtered, sorted, and manipulated through different
parameters. By default 20 entities in alphabetical order are shown.
(3) Available IDs can be obtained by using the type-tree or node-overview
endpoint.
Required parameters are shown as **bold**.

Nodes endpoints
***************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/0.3/subunits/{id}
     - **id**, count, download, format
     - Displays all subunits of a place in a special format used by the
       THANADOS project
   * - /api/0.3/type_by_view_class/
     - download
     - Retrieves a list of all types sorted by view class
   * - /api/0.3/type_overview/
     - download
     - Retrieves a list of all types
   * - /api/0.3/type_tree/
     - download
     - Shows every *type* in an OpenAtlas instance, with its root and subs, so
       a tree can be build

Content endpoints
*****************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/0.3/export_database/{format}
     - none
     - Downloads all information in an OpenAtlas instance as CSV, XML, or JSON
   * - /api/0.3/classes/
     - none
     - Retrieves a detailed list of all available system classes, their CIDOC
       CRM mapping, which view they belong to, which icon is used, and their
       English name
   * - /api/0.3/content/
     - download, lang
     - Retrieves a detailed list of information on available content in an
       OpenAtlas instance - intro, legal notice, contact, and size of processed
       images
   * - /api/0.3/geometric_entities/
     - count, download
     - Retrieves a detailed GeoJSON list of all chosen geometries in an
       OpenAtlas instance; this was implemented for map usage
   * - /api0.3/system_class_count/
     - none
     - Retrieves a list of the numbers of entries connected to a system class

Subunit endpoints
*****************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/0.3/subunits/{id}
     - count, download
     - Retrieves a list of the given place and all of its subunits, provided
       in a format used by the THANADOS project
       (`THANADOS output format <https://redmine.openatlas.eu/projects/uni/wiki/Thanados_Format>`_).
       With the format=xml parameter, a XML can be created. Takes only a valid
       place ID (E18) as parameter

Image endpoints
***************

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

  * - API endpoint
    - Possible parameters
    - Description
  * - /api/0.3/display/{id}
    - image size
    - Provides the image connected to the requested ID. Be aware, the image
      will only be displayed if the request comes from a **logged-in** user or
      API public setting is set to on and the image has a **license**
