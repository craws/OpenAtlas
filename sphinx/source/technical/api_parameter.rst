API parameter 0.3
========================

.. toctree::

.. _cidoc-classes-para-0.3:

.. list-table:: **cidoc_class / cidoc_classes**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - CIDOC CRM class code (e.g. E21)
   * - Values
     - E5, E7, E8, E9, E12, E18, E20, E21, E22, E31, E32, E33, E41, E53, E54, E55, E65, E74

.. _column-para-0.3:

.. list-table:: **column**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Results will be sorted by the given column
   * - Values
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

.. _count-para-0.3:

.. list-table:: **count**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - boolean
   * - Description
     - Returns the total count of results as integer
   * - Values
     - True/False

.. _download-para-0.3:

.. list-table:: **download**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - boolean
   * - Description
     - Triggers file download of the requested data in a file
   * - Values
     - True/False

.. _entities-para-0.3:

.. list-table:: **entities**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer, multiple
   * - Description
     - Specific entity ID
   * - Values
     - e.g. 89

.. _export-para-0.3:

.. list-table:: **export**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Results will be downloaded in the given format
   * - Values
     - * csv
       * csvNetwork

.. _first-para-0.3:

.. list-table:: **first**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer
   * - Description
     - List of results starting with given ID
   * - Values
     - e.g. 89

.. _format-para-0.3:

.. list-table:: **format**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Select a preferred output format
   * - Values
     -  * lp
        * loud
        * geojson
        * geojson-v2
        * pretty-xml
        * n3
        * turtle
        * nt
        * xml (subunits endpoint can only handle xml)

.. _geometry-para-0.3:

.. list-table:: **geometry**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Select a preferred geometry
   * - Values
     -  * gisAll
        * gisPointAll
        * gisPointSupers
        * gisPointSubs
        * gisPointSibling
        * gisLineAll
        * gisPolygonAll

.. _id-para-0.3:

.. list-table:: **id**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer
   * - Description
     - Specific entity ID in OpenAtlas instance
   * - Values
     - e.g. 89

.. _image_size-para-0.3:

.. list-table:: **image_size**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Select the size category for the displayed image (can be modified in production.py)
   * - Values
     - * thumbnail
       * table

.. _lang-para-0.3:

.. list-table:: **lang**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Select an output language
   * - Values
     - * en
       * de

.. _last-para-0.3:

.. list-table:: **last**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer
   * - Description
     - JSON list of results start with entity after given ID
   * - Values
     - e.g. 90

.. _latest-para-0.3:

.. list-table:: **latest**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer
   * - Description
     - * Number of last database entries to be returned.
       * Only numbers between 1 and 100 are valid.
   * - Values
     - 1 - 100

.. _limit-para-0.3:

.. list-table:: **limit**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer
   * - Description
     - Number of entities returned per page
   * - Values
     - * 0 corresponds to "no limit set"
       * Default is set to 20 entities

.. _none-para-0.3:

.. list-table:: **none**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     -
   * - Description
     - No parameters are required
   * - Values
     -

.. _page-para-0.3:

.. list-table:: **page**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer
   * - Description
     - Jump to chosen page
   * - Values
     - e.g. 2

.. _relation_type-para-0.3:

.. list-table:: **relation_type**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Select which relations are shown
   * - Values
     - E.g. P53

.. _search-para-0.3:

.. list-table:: **search**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Search request with AND/OR logic
   * - Values
     -

.. _show-para-0.3:

.. list-table:: **show**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Select a key to be shown. If using "not", no other keys will be displayed.
   * - Values
     - * description
       * depictions
       * geometry
       * links
       * names
       * none
       * relations
       * types
       * when

.. _sort-para-0.3:

.. list-table:: **sort**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Results will be sorted asc/desc (default column is name)
   * - Values
     - * asc
       * desc

.. _system-classes-para-0.3:

.. list-table:: **system_class / system_classes**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Needs to be one of the OpenAtlas system classes
   * - Values
     - * all
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

.. _type_id-para-0.3:

.. list-table:: **type_id**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - integer, multiple
   * - Description
     - | Output will be filtered by chosen type ID.
       | Only entities with this type ID will be displayed.
       | The relation is in logical OR.
   * - Values
     - e.g. 90

.. _view-classes-para-0.3:

.. list-table:: **view_class / view_classes**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Needs to be one of the OpenAtlas menu items
   * - Values
     - * actor
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

