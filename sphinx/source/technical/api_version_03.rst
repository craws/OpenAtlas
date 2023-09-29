.. _version_0_3:

Version 0.3
===========

Entity endpoint
****************

.. code::

  /api/0.3/entity/{id}

Endpoint provide information about one entity in the OpenAtlas instance. The requested information is provided in Linked
Places format (LPF). Alternatively, Linked Open Art (LOUD), GeoJSON or RDFs, derived from the LPF data, can be accessed.


======================== ====================== ====================== ====================
**Optional Parameters**
-------------------------------------------------------------------------------------------
:ref:`download-para-0.3` :ref:`export-para-0.3` :ref:`format-para-0.3` :ref:`show-para-0.3`
======================== ====================== ====================== ====================

**Example**
    https://demo.openatlas.eu/api/0.3/entity/4840?format=loud

Query
*****

Endpoint provide information about one entity in the OpenAtlas instance. The requested information is provided in
Linked Places format (LPF). Alternatively, Linked Open Art (LOUD), GeoJSON or RDFs, derived from the LPF data, can be accessed. Combine several or all entities endpoints in one query.

.. code::

  /api/0.3/query?

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

**Example**
    https://demo.openatlas.eu/api/0.3/query?cidoc_classes=E18&cidoc_classes=E31&system_classes=person&limit=120

Multiple entities
*****************

Endpoints provide information about entities in the OpenAtlas instance. The requested information is provided in Linked
Places format (LPF). Alternatively, Linked Open Art (LOUD), GeoJSON or RDFs, derived from the LPF data, can be accessed.

CIDOC class
"""""""""""

.. code::

  /api/3.0/cidoc_class/{cidoc_class}

Retrieves a JSON list of entities based on their CIDOC CRM class [1]_ [2]_

======================== ======================= ======================== ============================= ====================== ======================
 **Optional Parameters**
-----------------------------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
  :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
  :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================= ======================== ============================= ====================== ======================

**Example**
    https://demo.openatlas.eu/api/0.3/cidoc_class/E18

Entities linked to entity
"""""""""""""""""""""""""

.. code::

  /api/0.3/entities_linked_to_entity/{id}

Used to retrieve a JSON list of entities linked to the entity with the stated **ID** [2]_

======================== ======================= ======================== ============================= ====================== ======================
 **Optional Parameters**
-----------------------------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
  :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
  :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================= ======================== ============================= ====================== ======================

**Example**
    https://demo.openatlas.eu/api/0.3/entities_linked_to_entity/4840

Latest
""""""

.. code::

  /api/0.3/latest/{n}

Used to retrieve the last entry/entries made. The number {n} represents the amount of entities retrieved.
{n} can be between 1 and 100. The pagination information is always **null**

======================== ======================== ====================== ======================= =============================
 **Optional Parameters**
------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`download-para-0.3` :ref:`export-para-0.3` :ref:`format-para-0.3`  :ref:`relation_type-para-0.3`
  :ref:`search-para-0.3` :ref:`show-para-0.3`     :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================== ====================== ======================= =============================

**Example**
    https://demo.openatlas.eu/api/0.3/latest/25

System class
""""""""""""

.. code::

  /api/0.3/system_class/{system_class}

Retrieves a list of entities, based on their OpenAtlas system class name as JSON [1]_ [2]_

======================== ======================= ======================== ============================= ====================== ======================
 **Optional Parameters**
-----------------------------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
  :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
  :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================= ======================== ============================= ====================== ======================

**Example**
    https://demo.openatlas.eu/api/0.3/system_class/person

Type entities
"""""""""""""

.. code::

  /api/0.3/type_entities/{id}

Used to retrieve a JSON list of entities, based on their OpenAtlas **type** [2]_ [3]_

======================== ======================= ======================== ============================= ====================== ======================
 **Optional Parameters**
-----------------------------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
  :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
  :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================= ======================== ============================= ====================== ======================

**Example**
    https://demo.openatlas.eu/api/0.3/type_entities/47

Type entities all
"""""""""""""""""

.. code::

  /api/0.3/type_entities_all/{id}

Used to retrieve a JSON list of entities, based on their OpenAtlas **type** and includes all connected entities [2]_ [3]_

======================== ======================= ======================== ============================= ====================== ======================
 **Optional Parameters**
-----------------------------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
  :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
  :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================= ======================== ============================= ====================== ======================

**Example**
    https://demo.openatlas.eu/api/0.3/type_entities_all/47

View class
""""""""""

.. code::

  /api/0.3/view_class/{view_class}

Used to retrieve a JSON list of entities based on their OpenAtlas class view

======================== ======================= ======================== ============================= ====================== ======================
 **Optional Parameters**
-----------------------------------------------------------------------------------------------------------------------------------------------------
  :ref:`column-para-0.3` :ref:`count-para-0.3`   :ref:`download-para-0.3` :ref:`export-para-0.3`        :ref:`first-para-0.3`  :ref:`format-para-0.3`
  :ref:`last-para-0.3`   :ref:`limit-para-0.3`   :ref:`page-para-0.3`     :ref:`relation_type-para-0.3` :ref:`search-para-0.3` :ref:`show-para-0.3`
  :ref:`sort-para-0.3`   :ref:`type_id-para-0.3`
======================== ======================= ======================== ============================= ====================== ======================

**Example**
    https://demo.openatlas.eu/api/0.3/view_class/actor


.. [1] All codes available in OpenAtlas can be found under `OpenAtlas and CIDOC CRM class mapping <https://redmine.openatlas.eu/projects/uni/wiki/OpenAtlas_and_CIDOC_CRM_class_mapping?parent=Endpoints>`_
.. [2] The result can be filtered, sorted, and manipulated through different parameters. By default 20 entities in alphabetical order are shown.
.. [3] Available IDs can be obtained by using the type-tree or node-overview endpoint.


Type endpoints
***************

Provide information about Types of an OpenAtlas instance. The results are in JSON and in a custom format.

Type by view class
""""""""""""""""""

.. code::

  /api/0.3/type_by_view_class/

Retrieves a list of all types sorted by view class

======================== ==
 **Optional Parameters**
---------------------------
:ref:`download-para-0.3`
======================== ==

**Example**
    https://demo.openatlas.eu/api/0.3/type_by_view_class/

Type overview
""""""""""""""""""

.. code::

  /api/0.3/type_overview/

Retrieves a list of all type

======================== ==
 **Optional Parameters**
---------------------------
:ref:`download-para-0.3`
======================== ==

**Example**
    https://demo.openatlas.eu/api/0.3/type_overview/

Type tree
""""""""""""""""""

.. code::

  /api/0.3/type_tree/

Shows every *type* in an OpenAtlas instance in hierarchical order.

======================== ==
 **Optional Parameters**
---------------------------
:ref:`download-para-0.3`
======================== ==

**Example**
    https://demo.openatlas.eu/api/0.3/type_tree/

Administrative endpoints
************************

Provide metadata of the OpenAtlas instance for presentation sites.

Classes
""""""""""""""""""

.. code::

  /api/0.3/classes/

Retrieves a detailed list of all available system classes, their CIDOC CRM mapping, which view they belong to,
which icon is used, and their english name.

**Example**
    https://demo.openatlas.eu/api/0.3/classes/

Content
""""""""""""""""""

.. code::

  /api/0.3/content/

Retrieves a detailed list of information on available content in an OpenAtlas instance -
intro, legal notice, contact, and size of processed images.

======================== ====================
 **Optional Parameters**
---------------------------------------------
:ref:`download-para-0.3` :ref:`lang-para-0.3`
======================== ====================

**Example**
    https://demo.openatlas.eu/api/0.3/content/

System class count
""""""""""""""""""

.. code::

  /api/0.3/system_class_count/

Retrieves a list of the numbers of entries connected to a system class

**Example**
    https://demo.openatlas.eu/api/0.3/system_class_count/

Special endpoints
*****************

Provides project-specific formats.

Export database
"""""""""""""""

.. code::

  /api/0.3/export_database/{format}

Downloads all information in an OpenAtlas instance as CSV, XML, or JSON

**Example**
    https://demo.openatlas.eu/api/0.3/export_database/json

Geometric entities
""""""""""""""""""

.. code::

  /api/0.3/geometric_entities/

Retrieves a detailed GeoJSON list of all chosen geometries in an OpenAtlas instance; this was implemented for map usage

======================== ======================== ========================
 **Optional Parameters**
--------------------------------------------------------------------------
:ref:`count-para-0.3`    :ref:`download-para-0.3` :ref:`geometry-para-0.3`
======================== ======================== ========================

**Example**
    https://demo.openatlas.eu/api/0.3/geometric_entities/

Subunits
""""""""

.. code::

  /api/0.3/subunits/{id}

Displays all subunits of a place in a special format used by the `THANADOS <http://thanados.net/>`_ project

======================== ========================
 **Optional Parameters**
-------------------------------------------------
:ref:`count-para-0.3`    :ref:`download-para-0.3`
======================== ========================

Image endpoints
***************

Display
"""""""

.. code::

  /api/0.3/display/{id}

Provides the image connected to the requested ID. Be aware, the image will only be displayed if the request comes
from a **logged-in** user or API public setting is set to on and the image has a **license**.

=========================== ========================
 **Optional Parameters**
----------------------------------------------------
:ref:`image_size-para-0.3`
=========================== ========================


Licensed file overview
""""""""""""""""""""""

.. code::

  /api/0.3/licensed_file_overview/

Provides a list of all images, or images provided by:ref:`file_id-para-0.3`, with their data used to implement in a
presentation site (display URL, thumbnail URL, file extension, license).

======================== ======================== ========================
 **Optional Parameters**
--------------------------------------------------------------------------
:ref:`count-para-0.3`    :ref:`download-para-0.3` :ref:`file_id-para-0.3`
======================== ======================== ========================
