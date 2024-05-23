Import
======

.. toctree::

Import is available for admins and managers and offers functionality to import data
from `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ files.
Currently lists can be imported containing:

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
* origin_id
* Place hierarchy

Preparations
------------
Automatic imports can be dangerous for data integrity and it may be very time consuming to reverse them so we strongly advise:

* SQL backups **before** import, an existing backup not older than a day is enforced
* Use the preview (enabled by default) and check if the data looks alright

The import operation is encapsulated in a transaction, meaning if there is an error in the script,
nothing will be imported.

**The file:**

* Take a look at the :download:`example.csv` or :download:`example_place_hierarchy.csv`
* Make sure the extension is spelled correctly in lower case e.g. my_data.csv
* In the first row should be the header names
* Each following row is one data set. Values are separated by commas
* Text can be enclosed in double quotes (**"**), especially if the contain commas

Projects
--------
To retrace imported entities they have to be associated with a project. If there is none (or not
the right one) available, you'll have to create a new one. The name and description can be updated
later.

Import class
------------
Only one class can be imported at a time, so you have to choose one of the available classes.

Possible import fields
----------------------
The header can contain the following titles. Columns with other titles won't get imported but shown as
an error message.

* **name** - required, an error will be displayed if the header is missing. A warning will be displayed, if names in data rows are missing and these won't get imported.
* **alias** - only available for person, group and place, see :ref:`Alias import`
* **description** - a description can be provided
* **origin_id** - It has to be **unique per project** so if you have multiple like a person and place with id = 1 you can prefix them in the document e.g. person_1, place_1 before importing them
* **begin_from** - used for dates, see :ref:`Dates import`
* **begin_to** - used for dates, see :ref:`Dates import`
* **end_from** - used for dates, see :ref:`Dates import`
* **end_to** - used for dates, see :ref:`Dates import`
* **type_ids** - used to link to types, see :ref:`Types import`
* **value_types** - used to link to a value type, see :ref:`Value types import`
* **references** - used to link existing references, see :ref:`References import`
* **wkt** - only available for places and artifacts, see :ref:`WKT import`
* **reference_system_*** - used to link existing external reference systems, see :ref:`Reference systems import`
* **administrative_unit** - only available for places, id of existing administrative unit
* **historical_place** - only available for places, id of existing historical place
* **parent_id** - only available for place, id of a super unit in a place hierarchy, see :ref:`Place hierarchy import`
* **openatlas_class** - only available for place and only used with **parent_id**, see :ref:`Place hierarchy import`

.. _Alias import:

Alias
+++++
:doc:`/ui/alias` can be entered as string. Multiple aliases can be separated with semicolon (**;**).
If an :doc:`/ui/alias` contains a comma (**,**) please surround the whole filed with double quotes(**"**)

.. _Dates import:

Dates
+++++
Dates can be entered in the format **YYYY-MM-DD** in the fields **begin_from** and **end_from**.
You can also use time spans in combinations with the fields **begin_to** and **end_to**,
see: :doc:`/ui/date`

* If the date format is incorrect, they will be displayed in red and won't be imported
* Missing values for time spans will be discarded silently, e.g. a valid value in **begin_to**, but an empty value in **begin_from**
* There are no advanced checks between dates, e.g. end dates can be before begin dates. You should check them after the import at :doc:`/admin/data_integrity_checks`

.. _Types import:

Types
+++++
It is possible to link entities to :doc:`/entity/type` at the import which can be very useful e.g. if you have
a custom type **Case studies** to link them all in one go.

* :doc:`/entity/type` ids can be entered at the column **type_ids**
* You can enter multiple separated with a space
* The id of a :doc:`/entity/type` can be looked up at the detail view of a :doc:`/entity/type`

.. _Value types import:

Value types
+++++++++++
It is possible to link entities to value :doc:`/entity/type` at the import.

* Value :doc:`/entity/type` can be entered at the column **value_types**
* Type id and value are separated with a semicolon (**;**), e.g. 1234;-13.65
* Value :doc:`/entity/type` need always a value
* You can enter multiple separated with a space
* The id of a value :doc:`/entity/type` can be looked up at the detail view of a value :doc:`/entity/type`

.. _References import:

References
++++++++++
It is possible to link existing :doc:`/entity/reference` to imported entities.

* :doc:`/entity/reference` ID and pages are separated with a semicolon (**;**), e.g. 1234;56-78
* To link :doc:`/entity/reference` without page number, just add the ID without semicolon (**;**)
* You can enter multiple :doc:`/entity/reference` separated with a space, e.g. 1234;56-78 5678
* The ID of a :doc:`/entity/reference` can be looked up at the detail view of the entity

.. _WKT import:

WKT coordinates
+++++++++++++++
For places and artifact (multi)point, (multi)polygon, (multi)linestring coordinates or
GeometricCollection can be imported. Keep in mind to use
the `WGS84 <https://gisgeography.com/wgs84-world-geodetic-system/>`_ geodetic system (EPSG 4326).
Coordinates will be imported as `WKT <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_.
It is only possible to import one geometry for each entry. Since the WKT format uses commas (**,**),
surround the coordinates with double quotes (**"**)

Example:
    "LINESTRING (12.458533781141528 41.922205268362234, 12.53062334955289 41.917606998887024, 12.52169797441624 41.888476931243254)"

.. _Reference systems import:

External reference systems
++++++++++++++++++++++++++
It is possible to link the imported entity to an existing :doc:`/entity/reference_system`.
In this case, the header has to be named **reference_system_*** with the *name* of the
external :doc:`/entity/reference_system` appended, e.g. **reference_system_wikidata**.
If spaces occur in the name, please substitute them with underscore (**_**), e.g.
**reference_system_getty_aat**.

The entry consist of two values, separated by a semicolon (**;**). The first value is
the identifier, e.g. Q54123, the second value is the match type (**close_match** or **exact_match**)

Example:
    Q54123;close_match

.. _Place hierarchy import:

Place hierarchy
+++++++++++++++++++++++++++++
The **parent_id** is used to generate a :doc:`/entity/place` hierarchy together with :doc:`/entity/feature`, :doc:`/entity/stratigraphic_unit`,
:doc:`/entity/artifact`, and :doc:`/entity/human_remains`.
The **parent_id** has to be an **origin_id** of a row in the **current** import file.
To declare, which entry has a specific class, the **openatlas_class** column is used.
Here the following classes can be entered: :doc:`/entity/place`, :doc:`/entity/feature`, :doc:`/entity/stratigraphic_unit`,
:doc:`/entity/artifact`, and :doc:`/entity/human_remains`. This is case-insensitive.
For an example, please see: :download:`example_place_hierarchy.csv`

For questions about the correct place hierarchy structure, please see the **archaeological sub units** at the OpenAtlas :doc:`/model/index`.

Import options
--------------
* **File** - select the file you'll want to import
* **Preview** - if this option is selected, nothing will be imported and you see a preview
* **Check for duplicates** - if selected, the chosen class e.g. person will be searched for already existing names. The search is not case-sensitive e.g. "King Arthur" would be found even it is spelled "KiNg ArThUr". If duplicates are found a warning is printed but this doesn't stop the import so check it before with the preview.

After the import
----------------
When the import went through, you'll see a summary which data was imported (like the preview).
Also, you can browse the projects to see which imported entities are associated with them.
If you enabled the advanced layout you can also see in the detail view of an entity from which
project it was imported, which user did the import and the origin_id value.

Although the script makes a lot of validation checks it's always a good idea to run
:doc:`/admin/data_integrity_checks` after each import.
