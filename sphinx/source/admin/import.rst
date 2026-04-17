Import
======

.. toctree::

Import settings are available for admins and managers and offer functionality
to import data directly from
`CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ files.

Preparation
-----------
Automatic imports can cause problems regarding data integrity, so proceed with
caution. Fixing such problems can be time consuming, so we strongly advise
you to:

* Make an SQL backups **before** the import of any data; an existing backup
  not older than a day is enforced
* Use the preview (enabled by default) and check if the data looks alright

The import operation is encapsulated in a transaction. So if there is an
error in the script, nothing will be imported.

**The file:**

* Use UTF-8 encoding for your CSV files to ensure special characters (e.g. ä, ö, ü) are correctly imported.
* Make sure the file extension (.csv) is spelled correctly in lower case e.g.
  my_data.csv
* Header names are found in the first row of the table
* Each following row contains one data set; values are separated by commas (**,**)
* Text should be enclosed in double quotes (**"**), especially if they contain
  commas

General Concepts
----------------

Import Workflow
+++++++++++++++

For complex datasets, it is highly recommended to follow a specific import order to ensure all links
(e.g., to types or literature) are established correctly. Always import your data in this sequence:

1. **Types**: Import your custom types first, as entities in other files will refer to them.
2. **Bibliography / References**: Import your literature next.
3. **Entities**: Finally, import your main entities (Places, Persons, Events, Artifacts).

Identifiers (ID vs. OpenAtlas ID)
+++++++++++++++++++++++++++++++++

One of the most important concepts to understand is how OpenAtlas links
data during import:

* **id** (in CSV): This is a **temporary** identifier you provide (e.g., `person_1`, `abbey_01`). It is only used *within the import project* to link entries together (e.g., to assign a parent place or a source). After the import, the system assigns its own internal IDs but keeps the ID as *Origin ID*.
* **OpenAtlas ID**: This is the unique number an entity already has in the
  database (visible in the URL or the detail view). You use this when you want
  to link new data to *existing* records.

Linking Limitations
+++++++++++++++++++

Currently, the CSV import only supports linking to **References/Bibliography** and **Types** during the
import of an entity. It is **not** possible to link to other entity classes (e.g., linking an event to
a person or a place) within the CSV file, with one exception:

*   **Place Hierarchies**: Within a single CSV file, places can be linked to each other using the
    `parent_id` field.

For all other relationships (e.g., Person - Event), the links must be created manually in the
OpenAtlas interface after the import.

Import Project
++++++++++++++
To find imported entities after the import, they have to be associated with a
project. If no project is available (or not the right one) you have
to create a new one. Name and description of said project can be updated
later.

Supported Fields
-----------------------

Not every field is allowed for every class. The following table provides an
overview of which column headers (attributes) are supported for which import class:

.. csv-table:: Supported Import Fields
   :file: ../../../openatlas/static/import_field_matrix.csv
   :header-rows: 1
   :class: tight-table

Class Specific Descriptions
---------------------------

The following sections describe the fields and their requirements for different entity classes.

ID
++
.. _id_import:

* **id**: This field has to be **unique per project**. Please use only characters, numbers, underscore (_) or hyphen (-).
  It is a **temporary** identifier used *within the import project* to link entries together.

.. _Name_import:

Names
+++++
* **name**: Required for every entry. The import will fail for rows without a name.
* **alias**: Multiple names separated by semicolon (**;**), e.g., `Notker Balbulus;Notker the Stammerer`.

.. _Dates_import:

Dates
+++++
Dates can be entered in the format **YYYY-MM-DD**, **YYYY-MM** or **YYYY**.

* **begin_from / begin_to**: Start of the event (as a point in time or timespan).
* **end_from / end_to**: End of the event.

See :doc:`/ui/date` for more details.

.. _Types_import:

Types & Value Types
+++++++++++++++++++

* **type_ids**: Link to existing system types (e.g., `765 <https://demo.openatlas.eu/entity/765>`_). Enter one or more IDs, separated by space.
* **origin_type_ids**: Link to types *imported within the same project*.
* **value_types**: Pair of `Type-ID;Value`, e.g., `26188;45.5 <https://demo-dev.openatlas.eu/entity/26188>`_. Multiple pairs separated by space.
* **origin_...**: Same as above, but using the temporary `id` from your CSV instead of system IDs.

.. _References_import:

References
++++++++++
Format: `Reference-ID;Pages`.

* Example: `1603;56-78 <https://demo.openatlas.eu/entity/1603>`_
* Multiple references: `1234;56-78 5678;` (separated by space)
* If using commas in pages, wrap in quotes: `"1234;IV, 56-78"`

.. _Reference_systems_import:

External Reference Systems
++++++++++++++++++++++++++
Column name format: `reference_system_<name>`, e.g., `reference_system_wikidata`.
Value format: `Identifier;Match-Type` (Match-Type: `exact_match` or `close_match`).

* Example: `Q54123;exact_match`

.. _Geometries_import:

Geometries & Hierarchies (Places & Artifacts)
+++++++++++++++++++++++++++++++++++++++++++++
For geographical entities and physical objects:

* **wkt**: Well-Known Text geometry (e.g., `POINT(9.3 47.4)`). Only one
  geometry per entry, but also GeometryCollection and Multi geometries are allowed.
* **parent_id**: Links to the `id` of a super-unit *within the same file*.
* **openatlas_parent_id**: Links to the `ID` of an *existing* OpenAtlas entity.
* **openatlas_class**: Required when using `parent_id` to specify the target class (e.g., `place`, `feature`, `artifact`).

Example Datasets (St. Gallen)
-----------------------------
To better understand how these fields work together, you can download and inspect
these example files based on the historical Abbey of Saint Gall.

.. note::
   These examples use specific OpenAtlas IDs for type hierarchies that are only valid
   on the **demo-dev** instance (`https://demo-dev.openatlas.eu/ <https://demo-dev.openatlas.eu/>`_).

* :download:`Types <../../../openatlas/static/examples/example_types.csv>`
* :download:`Bibliography <../../../openatlas/static/examples/example_bibliography.csv>`
* :download:`Places (Place hierarchy)<../../../openatlas/static/examples/example_places.csv>`
* :download:`Persons <../../../openatlas/static/examples/example_persons.csv>`
* :download:`Modifications (Events) <../../../openatlas/static/examples/example_modifications.csv>`
* :download:`Sources <../../../openatlas/static/examples/example_sources.csv>`

Import Options
--------------
* **File**: Select your CSV file.
* **Preview**: (Enabled by default) Shows what would happen without actually changing the database.
* **Check for duplicates**: Searches for existing names (case-insensitive) and provides warnings.

After the Import
----------------
A summary of imported data is shown. It is highly recommended to run :doc:`/admin/data_integrity_checks` to ensure everything is correct.
