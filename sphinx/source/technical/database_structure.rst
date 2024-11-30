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

* **public** - general PostgreSQL functionality such as PostGIS functions
* **web** - non-model data related to the website such as:

   * website settings (upload size limit, email configuration, ...)
   * groups, users, user's preferences, notes, bookmarks, ...
   * image annotations
   * external reference system specifications
