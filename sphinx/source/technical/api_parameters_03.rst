API parameters 0.3
==================

.. toctree::

.. _cidoc-classes-para-0.3:

.. list-table:: **cidoc_classes**
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
     - | ID
       | classCode
       | name
       | description
       | created
       | modified
       | systemClass
       | beginFrom
       | beginTo
       | endFrom
       | endTo

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
     - | csv
       | csvNetwork

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
     -  | lp
        | loud
        | geojson
        | geojson-v2
        | pretty-xml
        | n3
        | turtle
        | nt
        | xml (subunits endpoint can only handle xml)

.. _geometry-para-0.3:

.. list-table:: **geometry**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Select a preferred geometry
   * - Values
     -  | gisAll
        | gisPointAll
        | gisPointSupers
        | gisPointSubs
        | gisPointSibling
        | gisLineAll
        | gisPolygonAll

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
     - | table
       | thumbnail

.. _lang-para-0.3:

.. list-table:: **lang**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Select an output language
   * - Values
     - | en
       | de

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
     - | Number of last database entries to be returned.
       | Only numbers between 1 and 100 are valid.
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
     - | 0 corresponds to "no limit set"
       | Default is set to 20 entities

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
     - Search request with complex AND/OR logic
   * - Values
     -

The search parameter provides a tool to filter and search the request with logical operators.

**Example**
    The search parameter takes a JSON as value. A key has to be a *filterable category* followed by a list/array.
    This list need to have again JSON values as items. There can be multiple search parameters. E.g:

.. code-block::

    {domain}/api/{api version}/{endpoint}?search={
        "typeID": [{"operator": "equal", "values": [123456]}],
        "typeName": [{"operator": "like", "values": ["Chain", "Bracelet", "Amule"], "logicalOperator": "and"}]
    }& search = {
        "typeName": [{"operator": "equal", "values": ["Gold"]}],
        "beginFrom": [{"operator": "lesserThan", "values": ["0850-05-12"],"logicalOperator": "and"}]}

Every JSON in a search parameter field is logical connected with AND. E.g:

.. code-block::

    ?search={A:[{X}, {Y}], B: [M]} => Entities containing A(X and Y) and B(M)

To build an search start with following parameter:

    ``?search={}``

Now a `categories`_ after which the results are search, has to be selected:

    ``?search={"typeName"}``

After the `categories`_ are selected, next make a list with possible multiple JSONs (JSONs are connected with *OR*)

    ``?search={"typeName": [{},{}]}``

Next a list of `values`_ has to be provided:

    ``?search={"typeName": [{"values": ["Gold", "Silver"]}]}``

Then an `operators`_ has to be selected, how the `values`_ should be treated:

    ``?search={"typeName": [{"operator": "equal", "values": ["Gold", "Silver"]}]}``

At last a `logical`_ operator can be assigned, if the values will be treated with *OR* or *AND*:

    ``?search={"typeName": [{"operator": "equal", "values": ["Gold", "Silver"], "logicalOperator": "and"}]}``

.. _categories:

Filterable categories
^^^^^^^^^^^^^^^^^^^^^

.. hlist::
   :columns: 5

   - entityName
   - entityDescription
   - entityAliases
   - entityCidocClass
   - entitySystemClass
   - entityID
   - typeID
   - valueTypeID
   - typeIDWithSubs
   - typeName
   - beginFrom
   - beginTo
   - endFrom
   - endTo
   - relationToID

.. _values:

Values
^^^^^^

Values has to be a list of items. The items can be either a string, an integer or a tuple (see Note). Strings need to
be marked with "" or '', while integers doesn't allow this.

*Note*: the category valueTypeID can search for values of a type ID. But it takes one or more two valued Tuple as list
entry: (x,y). x is the type id and y is the searched value. This can be an int or a float, e.g:

     ``{"operator":"lesserThan","values":[(3142,543.3)],"logicalOperator":"and"}``

.. _operators:

Compare operators
^^^^^^^^^^^^^^^^^

.. hlist::
   :columns: 4

   - equal
   - notEqual
   - like [1]_
   - greaterThan [2]_
   - greaterThanEqual [2]_
   - lesserThan [2]_
   - lesserThanEqual [2]_

The compare operators work like the mathematical operators.
equal x=y, notEqual x!=y, greaterThan x>y , greaterThanEqual x>=y, lesserThan x<y, lesserThanEqual x<=y.
The like operator searches for occurrence of the string, so a match can also occur in the middle of a word.

.. [1] Only for string based categories
.. [2] Only for beginFrom, beginTo, endFrom, endTo, valueTypeID

.. _logical:

Logical operators
^^^^^^^^^^^^^^^^^

Not mandatory, *OR* is the default value. Logical operators handles, if the `values`_ are treated as *OR* or *AND*.

 ``and, or``


.. _show-para-0.3:

.. list-table:: **show**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Select a key to be shown. If using "not", no other keys will be displayed.
   * - Values
     - | description
       | depictions
       | geometry
       | links
       | names
       | none
       | relations
       | types
       | when

.. _sort-para-0.3:

.. list-table:: **sort**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string
   * - Description
     - Results will be sorted asc/desc (default column is name)
   * - Values
     - | asc
       | desc

.. _system-classes-para-0.3:

.. list-table:: **system_classes**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Needs to be one of the OpenAtlas system classes
   * - Values
     - | all
       | administrative_unit
       | type
       | acquisition
       | activity
       | actor_actor_relation
       | actor_function
       | appellation
       | artifact
       | bibliography
       | edition
       | external_reference
       | feature
       | file
       | group
       | human_remains
       | involvement
       | move
       | object_location
       | person
       | place
       | production
       | reference_system
       | source
       | source_translation
       | stratigraphic_unit

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

.. list-table:: **view_classes**
   :widths: 10 80
   :stub-columns: 1

   * - Format
     - string, multiple
   * - Description
     - Needs to be one of the OpenAtlas menu items
   * - Values
     - | actor
       | all
       | artifact
       | event
       | file
       | object
       | place
       | reference
       | source
       | source_translation
       | type

