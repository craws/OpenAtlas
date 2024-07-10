Database Structure
==================

.. toctree::

Regarding the database structure, the following PostgreSQL schemas are used:

* **import** - to track entities imported via the backend

* **model** - the main project data

   * CIDOC specifications (classes, properties, translations)
   * OpenAtlas classes (based on CIDOC classes)
   * Entities (OpenAtlas class instances)
   * Links (CIDOC property instances)

* **public** - general PostgreSQL functionality, e.g. PostGIS functions
* **web** - none model data related to the website, e.g.

   * website settings (upload size limit, email configuration, ...)
   * groups, users and their preferences, notes, bookmarks, ...
   * image annotations
   * external reference system specifications
