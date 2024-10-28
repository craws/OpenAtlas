Import
======

.. toctree::

Import settings are available for admins and managers and offer functionality
to import data directly from
`CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ files.
Lists containing the following fields can be imported currently:

* Name
* Alias
* Description
* Dates
* GIS data
* Types
* Value types
* References
* Reference systems
* Administrative unit
* Historical place
* Origin IDs
* Place hierarchy

Preparation
-----------
Automatic imports cause problems regarding data integrity, so proceed with
caution. Fixing such problems can be time consuming, so we strongly advise
you to:

* Make an SQL backups **before** the import of any data; an existing backup
  not older than a day is enforced
* Use the preview (enabled by default) and check if the data looks alright

The import operation is encapsulated in a transaction. So if there is an
error in the script, nothing will be imported.

**The file:**

* Take a look at the :download:`example.csv` or
  :download:`example_place_hierarchy.csv`
* Make sure the file extension (.csv) is spelled correctly in lower case e.g.
  my_data.csv
* Header names are found in the first row of the table
* Each following row contains one data set; values are separated by commas
* Text should be enclosed in double quotes (**"**), especially if they contain
  commas

Project
-------
To find imported entities after the import, they have to be associated with a
project. If no project is available (or not the right one) you have
to create a new one. Name and description of said project can be updated
later.

Import class
------------
Only one class can be imported at a time, so you have to choose one of the
available classes.

Possible import fields
----------------------
Column headers can contain the following titles. Other titles won't be
imported and an error message will be displayed

* **name** - required, an error will be displayed if name; the data will not
  get imported if a name is missing
* **alias** - only available for person, group and place, see
  :ref:`Alias import`
* **description** - a description can be provided
* **id** - this field has to be **unique per project**; if you have
  same IDs like a person and place with id = 1, you can prefix them in the
  document e.g. person_1, place_1 before importing
* **begin_from** - used for dates, see :ref:`Dates import`
* **begin_to** - used for dates, see :ref:`Dates import`
* **end_from** - used for dates, see :ref:`Dates import`
* **end_to** - used for dates, see :ref:`Dates import`
* **type_ids** - used for linking to a type, see :ref:`Types import`
* **value_types** - used for linking to a value type, see :ref:`Value types
  import`
* **references** - used for linking data to already existing references in
  the database, see :ref:`References import`
* **wkt** - only available for places and artifacts, see :ref:`WKT import`
* **reference_system_*** - used for linking data to already existing external
  reference systems in the database, see :ref:`Reference systems import`
* **administrative_unit** - only available for places, ID of existing
  administrative unit
* **historical_place** - only available for places, ID of existing
  historical place
* **parent_id** - only available for place, ID of a super unit in a place
  hierarchy, see :ref:`Place hierarchy import`
* **openatlas_parent_id** - only available for place, ID of a super unit
  existing in OpenAtlas, see :ref:`Place hierarchy import`
* **openatlas_class** - only available for place and only used with
  **parent_id**, see :ref:`Place hierarchy import`

.. _Alias import:

Alias
+++++
:doc:`/ui/alias` can be entered as string. Multiple aliases can be separated
by semicolon (;). If an :doc:`/ui/alias` contains a comma (,) please
surround the whole string with double quotes(**"**).

.. _Dates import:

Dates
+++++
Dates can be entered in the format **YYYY-MM-DD**. Fill out the **begin_from**
and **end_from** field for a known timeframe. For a timespan you can use
**begin_to** and **end_to** in combination with **begin_from**
and **end_from**. For more information see: :doc:`/ui/date`.

Keep in mind:

* if the date format is incorrect, it will be displayed in red and won't be
  imported
* if the required fields are missing data (**begin_from**
  and/or **end_from**), values entered in the other fields (**begin_to** and
  **end_to**) will be lost without further warning
* There are no advanced checks for dates, so end dates can start before
  begin dates. Check validity after the importing process; for more
  information see :doc:`/admin/data_integrity_checks`

.. _Types import:

Types
+++++
It is possible to link entities to one or multiple :doc:`/entity/type`. This
can be useful for example when you use a custom type **Case studies** you
can link all of the imported data to this.

* :doc:`/entity/type` IDs can be entered in the column **type_ids**
* you can enter multiple IDs, separated by a space
* the ID of a :doc:`/entity/type` can be found at the detail view of the
  specific :doc:`/entity/type` in your OpenAtlas instance

.. _Value types import:

Value types
+++++++++++
It is possible to link entities to one or multiple value :doc:`/entity/type`
when importing.

* a Value :doc:`/entity/type` can be entered via the **value_types** column
* type ID and corresponding value are separated by a semicolon (**;**), e.g.
  1234;-13.65
* for each value :doc:`/entity/type` a value is required
* multiple value type-value pairs are separated by a space
* The ID of a value :doc:`/entity/type` can be found at the detail view of a
  specific value :doc:`/entity/type` in your OpenAtlas instance

.. _References import:

References
++++++++++
The imported data can be linked to an already existing
:doc:`/entity/reference`.

* :doc:`/entity/reference` ID and pages are separated by a semicolon
  (**;**), e.g. 1234;56-78
* to link a :doc:`/entity/reference` with multiple page numbers, wrap the
  whole cell in quotation marks, e.g. "1234;IV, 56-78 542;34-23 66;"
* to link a :doc:`/entity/reference` without page numbers, just add the ID
  and a semicolon (**;**) without further information
* enter multiple :doc:`/entity/reference` separated by a space, e.g. 1234;
  56-78 5678;
* the ID of each :doc:`/entity/reference` can be found at the detail view of
  said reference in your OpenAtlas instance

.. _WKT import:

WKT coordinates
+++++++++++++++
For places and artifact (multi)point, (multi)polygon, and (multi)linestring
coordinates or GeometricCollection can be imported. Keep in mind to use
the `WGS84 <https://gisgeography.com/wgs84-world-geodetic-system/>`_
geodetic system (EPSG 4326).
Coordinates will be imported as `WKT <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_.
It is only possible to import one geometry for each entry. Since the WKT
format uses commas, surround tall coordinates with double quotes (")

Example:
    "LINESTRING (12.458533781141528 41.922205268362234, 12.53062334955289 41.917606998887024, 12.52169797441624 41.888476931243254)"

.. _Reference systems import:

External reference systems
++++++++++++++++++++++++++
It is possible to link the imported entity to an existing :doc:`/entity/reference_system`.
Named the coulmn **reference_system_*** with the *name* of the external
:doc:`/entity/reference_system` appended, e.g. **reference_system_wikidata**.
If spaces occur in the name, please substitute them with underscore (_),
e.g. **reference_system_getty_aat**.
Each entry consist of two values, separated by a semicolon (;). The first
value is the identifier, e.g. Q54123, the second value is the match type
(**close_match** or **exact_match**)

Example:
    Q54123;close_match

.. _Place hierarchy import:

Place hierarchy
+++++++++++++++
Use the **parent_id** or **openatlas_parent_id** to generate a
:doc:`/entity/place` hierarchy together
with :doc:`/entity/feature`, :doc:`/entity/stratigraphic_unit`,
:doc:`/entity/artifact`, and :doc:`/entity/human_remains`.
The **parent_id** has to be an origin **id** of a row in the **current**
import file.
The **openatlas_parent_id** has to be an **existing** OpenAtlas entity ID
with the correct class.
To declare, which entry has a specific class, the **openatlas_class** column
is used. Here the following classes can be entered: :doc:`/entity/place`,
:doc:`/entity/feature`, :doc:`/entity/stratigraphic_unit`,
:doc:`/entity/artifact`, and :doc:`/entity/human_remains`. This is
case-insensitive.
For an example, please see: :download:`example_place_hierarchy.csv`

For questions about the correct place hierarchy structure, please have a
look at **archaeological sub units** at the OpenAtlas :doc:`/model/index`.

Import options
--------------
* **File** - select a file you'll want to import
* **Preview** - if this option is selected, nothing will be imported and you
  see a preview
* **Check for duplicates** - if selected, the chosen class e.g. person will
  be searched for already existing names. The search is not case-sensitive
  e.g. "King Arthur" would be found even it is spelled "KiNg ArThUr". If
  duplicates are found, a warning is printed but doesn't stop the import

After the import
----------------
When the import went through, a summary which data was imported is shown.
You can also browse the projects to see which imported entities are associated
with them.
If advanced layout is enabled, the detail view of an entity shows from which
project the entity was imported, which user did the import and the
origin ID value.

**It is always a good idea to run :doc:`/admin/data_integrity_checks` after
each import.**
