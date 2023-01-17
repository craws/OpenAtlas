Version 0.1
===========

.. toctree::

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - API endpoint
     - Possible parameters
     - Description
   * - /api/0.1/entity/{id}
     -
     - Retrieves all information about a single entity
   * - /api/0.1/entity/download/{id}
     -
     - Triggers a download function for the specific entity
   * - /api/0.1/query/
     - entities, classes, items, limit, column, sort, filter, first, last,
       show, count, download
     - Retrieves a list based on multiple query parameters
   * - /api/0.1/code/{code}
     - limit, column, sort, filter, first, last, show, count, download
     - Retrieves a list of geojson representations which share a menu item
   * - /api/0.1/class/{class}
     - limit, column, sort, filter, string, first, last, show, count, download
     - Retrieves a list of geojson representations which share a specified
       class code
   * - /api/0.1/latest/{limit}
     - download
     - Retrieves a list of geojson representations which were edited last
   * - /api/0.1/node_entities/{id}
     - count, download
     - Retrieves a list of entities linked to that node
   * - /api/0.1/node_entities_all/{id}
     - count, download
     - Retrieves a list of entities linked to that node and subnode
   * - /api/0.1/stratographic_node/{id}
     - count, download
     - Retrieves a list of entities linked to that place as stratigraphy,
       feature, find etc.
   * - /api/0.1/stratographic_node_all/{id}
     - count, download
     - Retrieves a list of all entities and sub entities linked to that place
       as stratigraphy, feature, find etc.
   * - /api/0.1/content
     - download, lang
     - Retrieves a detailed list of information on available content
       in an OpenAtlas instance - intro, legal notice, contact, and size of
       processed images
