Version 0.3
===========

.. toctree::

Entity endpoints
****************

Single entity
^^^^^^^^^^^^^^^

/api/0.3/entity/{id}
""""""""""""""""""""

Retrieves all information about a single entity


 ======================== ====================== ====================== ====================
  **Optional Parameters**
 -------------------------------------------------------------------------------------------
 :ref:`download-para-0.3` :ref:`export-para-0.3` :ref:`format-para-0.3` :ref:`show-para-0.3`
 ======================== ====================== ====================== ====================


Query
^^^^^

/api/0.3/query/
""""""""""""""""""""""""

Combine several or all entity endpoints in one query.

Retrieves a list with entity ID, CIDOC CRM code, system class, or menu
item. Combine up to four of the aforementioned endpoints in a single
query; each request has to be a new parameter.

 ============================= ======================== ============================== ============================
  **Required Parameters** - At least one is required for a successful request
 ------------------------------------------------------------------------------------------------------------------
 :ref:`cidoc-classes-para-0.3` :ref:`entities-para-0.3` :ref:`system-classes-para-0.3` :ref:`view-classes-para-0.3`
 ============================= ======================== ============================== ============================

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================


Multiple entities
^^^^^^^^^^^^^^^^^

Results in list form include related entities and pagination

/api/3.0/cidoc_class/{cidoc_class}
""""""""""""""""""""""""""""""""""

Retrieves a JSON list of entities based on their CIDOC CRM class [1]_ [2]_

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================

/api/0.3/entities_linked_to_entity/{id}
"""""""""""""""""""""""""""""""""""""""

Used to retrieve a JSON list of entities linked to the entity with the stated **ID** [2]_

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================

/api/0.3/latest/{n}
"""""""""""""""""""

Used to retrieve the last entry/entries made. The number {n} represents the amount of entities retrieved.
{n} can be between 1 and 100. The pagination information is always **null**

 ======================== ======================== ====================== ======================= =============================
  **Optional Parameters**
 ------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`download-para-0.3` :ref:`export-para-0.3` :ref:`format-para-0.3`  :ref:`relation_type-para-0.3`
   :ref:`search-para-0.3` :ref:`show-para-0.3`     :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================== ====================== ======================= =============================

/api/0.3/system_class/{system_class}
""""""""""""""""""""""""""""""""""""

Retrieves a list of entities, based on their OpenAtlas system class name as JSON [1]_ [2]_

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================

/api/0.3/type_entities/{id}
"""""""""""""""""""""""""""

Used to retrieve a JSON list of entities, based on their OpenAtlas **type** [2]_ [3]_

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================

/api/0.3/type_entities_all/{id}
"""""""""""""""""""""""""""""""

Used to retrieve a JSON list of entities, based on their OpenAtlas **type** and includes all connected entities [2]_ [3]_

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================

/api/0.3/view_class/{view_class}
""""""""""""""""""""""""""""""""

Used to retrieve a JSON list of entities based on their OpenAtlas class view

 ======================== ======================= ======================== ============================= ====================== ======================
  **Optional Parameters**
 -----------------------------------------------------------------------------------------------------------------------------------------------------
   :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
   :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
   :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
 ======================== ======================= ======================== ============================= ====================== ======================


.. [1] All codes available in OpenAtlas can be found under `OpenAtlas and CIDOC CRM class mapping <https://redmine.openatlas.eu/projects/uni/wiki/OpenAtlas_and_CIDOC_CRM_class_mapping?parent=Endpoints>`_
.. [2] The result can be filtered, sorted, and manipulated through different parameters. By default 20 entities in alphabetical order are shown.
.. [3] Available IDs can be obtained by using the type-tree or node-overview endpoint.


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
