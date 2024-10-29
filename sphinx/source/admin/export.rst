Export
======

.. toctree::

Available for admins and managers

Export SQL
----------

* Be aware, especially when sharing, that **user data**, e.g. email addresses,
  are included in the database backups
* SQL dumps are saved in the **files/export** folder
* A warning will appear if the directory isn't writable
* File names begin with date and time e.g. 2018-08-23_1533_export.sql
* Existing backups are shown in a list and can be downloaded or deleted

Export SQL
**********
A SQL dump will be created with **pg_dump** in a plain text format. The
resulting file can be used to fill an existing empty database, such as

.. code-block::

   psql openatlas < export.sql

Export database dump
********************

A SQL dump will be created with **pg_dump** in a custom archiving format (-Fc).
In this format **pg_restore** can be used to restore the database regardless
of used operating system and if line breaks are used or not

.. code-block::

   pg_restore -d openatlas -1 export.dump


Export CSV
----------
When the **Export CSV** button is clicked, a **ZIP** file containing several
**CSV** files is downloaded. The ZIP file contains:

* All entities divided by their OpenAtlas class
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The **ZIP** file's name starts with the current date and time, for
example 2022-10-04_1610-export.zip. This process can take some time.

Export JSON
-----------
When the **Export JSON** button is clicked, a **JSON** file is downloaded.
This file contains the following keys:

* Entities
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The file name starts with the current date and time, for example
2022-10-04_1610-export.json. This process can take some time.

Export XML
----------
When the **Export XML** button is clicked, an **XML** file is
downloaded. This file contains the following tags:

* Entities
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The file name starts with the current date and time, for example
2022-10-04_1610-export.xml. This process can take some time.
