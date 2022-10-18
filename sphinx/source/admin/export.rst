Export
======

.. toctree::

Available for admins and managers

Export SQL
----------
When clicking the **Export SQL** button a new SQL dump will be created with
pg_dump.

* Be aware, especially when sharing, that **user data**, e.g. email addresses,
  is included.
* Existing files are shown in a list and can be downloaded or deleted
  (only admins can delete)
* If the directory isn't writable, a warning will be shown
* SQL dumps are saved in the **export/sql** folder
* File names begin with date and time e.g. 2018-08-23_1533_dump.sql.


Export CSV
----------
When the **Export CSV** button is clicked, a **ZIP** file containing several
**CSV** files is downloaded. The CSV files are:

* All entities divided by their OpenAtlas class
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The file name of the **ZIP** file starts with the current date and time, for
example 2022-10-04_1610-export.zip. This process can take some time.


Export JSON
-----------
When the **Export JSON** button is clicked, the download of a **JSON** file
begins. This file contains following keys:

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
When the **Export XML** button is clicked, the download of an
**XML** file begins. This file contains following tags:

* Entities
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The file name starts with the current date and time, for example
2022-10-04_1610-export.xml. This process can take some time.

