Import
======

.. toctree::

Import is available for admins and managers and offers functionality to import data
from `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ files.
Currently lists can be imported containing:

* Name
* Description
* Dates
* GIS data
* Types
* origin_id

Preparations
------------
Automatic imports can be dangerous for data integrity and it may be very time consuming to reverse them so we strongly advise:

* SQL backups **before** import, an existing backup not older than a day is enforced
* Use the preview (enabled by default) and check if the data looks alright

The import operation is encapsulated in a transaction, meaning if there is an error in the script,
nothing will be imported.

**The file:**

* Take a look at the :download:`example.csv`
* Make sure the extension is spelled correctly in lower case e.g. my_data.csv
* In the first line should be the header names
* Each following line is one data set. Values are separated by commas
* Text can be enclosed in double quotes, especially if the contain commas

Projects
--------
To retrace imported entities they have to be associated with a project. If there is none (or not
the right one) available you'll have to create a new one. The name and description can be updated
later.

Import class
------------
Only one class can be imported at a time so you have to choose one of the available classes.

Import fields
-------------
The header can contain following titles. Columns with other titles won't get imported but shown as
an error message.

* **name** - required, an error will be displayed if the header is missing. A warning will be displayed, if names in data rows are missing and these wont get imported.
* **alias** - only available for person, group and place, see below
* **description** - a description can be provided
* **origin_id** - optional but useful to trace it back. It has to be **unique per project** so if you have multiple like a person and place with id = 1 you can prefix them in the document e.g. person_1, place_1 before importing them
* **begin_from** - used for dates, see below
* **begin_to** - used for dates, see below
* **end_from** - used for dates, see below
* **end_to** - used for dates, see below
* **type_ids** - used to link to types, see below
* **value_types** - used to link to a value type, see below
* **wkt** - only available for places and artifacts, see below
* **reference_system_*** - used to link existing external reference systems, see below
* **administrative_unit** - only available for places, id of existing administrative unit
* **historical_place** - only available for places, id of existing historical place


Alias
+++++
:doc:`/ui/alias` can be entered as string. Multiple aliases can be separated with semicolon (**;**).
If an alias contains a comma (**,**) please surround the whole filed with double quotes(**"**)

Dates
+++++
Dates can be entered in the format **YYYY-MM-DD** in the fields **begin_from** and **end_from**.
You can also use time spans in combinations with the fields **begin_to** and **end_to**,
see: :doc:`/ui/date`

* If the date format is incorrect they will be displayed in red and won't be imported
* Missing values for time spans will be discarded silently, e.g. a valid value in **begin_to** but an empty value in **begin_from**
* There are no advanced checks between dates e.g. end dates can be before begin dates. You should check them after the import at :doc:`/admin/data_integrity_checks`

Types
+++++
It is possible to link entities to types at the import which can be very useful e.g. if you have
a custom type **Case studies** to link them all in one go.

* Type ids can be entered at the column **type_ids**
* You can enter multiple separated with a space
* The id of a type can be looked up at the detail view of a type

Value types
+++++++++++
It is possible to link entities to value types at the import.

* Value types can be entered at the column **value_types**
* Type id and value are separated with an semicolon (**;**), e.g. 1234;-13.65
* Value types need always a value
* You can enter multiple separated with a space
* The id of a type can be looked up at the detail view of a value type

WKT coordinates
+++++++++++++++
For places and artifact point, polygon or linestring coordinates can be imported. Keep in mind to use
the `WGS84 <https://gisgeography.com/wgs84-world-geodetic-system/>`_ geodetic system.
Coordinates will be imported as `WKT <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_.
It is only possible to import one geometry for each entry. Since the WKT format uses commas (**,**),
surround the coordinates with double quotes (**"**)

Example:
    "LINESTRING (12.458533781141528 41.922205268362234, 12.53062334955289 41.917606998887024, 12.52169797441624 41.888476931243254)"

External reference systems
++++++++++++++++++++++++++
It is possible to link the imported entity to an existing :doc:`/entity/reference_system`.
In this case, the header has to be named **reference_system_*** with the *name* of the
external reference system appended, e.g. **reference_system_wikidata**.
If spaces occur in the name, please substitute them with underscore (**_**), e.g.
**reference_system_getty_aat**.

The entry consist of two values, separated by a semicolon (**;**). First value is
the identifier, e.g. Q54123, the second value is the match type (**close_match** or **exact_match**)

Example:
    Q54123;close_match


Import options
--------------
* **File** - select the file you'll want to import
* **Preview** - if this option is selected, nothing will be imported and you see a preview
* **Check for duplicates** - if selected the chosen class e.g. person will be searched for already existing names. The search is not case sensitive e.g. "King Arthur" would be found even it is spelled "KiNg ArThUr". If duplicates are found a warning is printed but this doesn't stop the import so check it before with the preview.

After the import
----------------
When the import went through you'll see a summary which data was imported (like the preview).
Also you can browse the projects to see which imported entities are associated with them.
If you enabled the advanced layout you can also see in the detail view of an entity from which
project it was imported, which user did the import and the origin_id value.

Although the script makes a lot of validation checks it's always a good idea to run
:doc:`/admin/data_integrity_checks` after each import.
