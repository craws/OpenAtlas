Database Structure
==================

.. toctree::

Regarding the database structure, the following PostgreSQL schemas are used:

* **import** - to track entities imported via the backend
* **model** - CIDOC specifications (classes, properties) and OpenAtlas classed
  base on them, entities and links
* **public** - general PostgreSQL functionality, e.g. PostGIS functions
* **web** - none model data related to the website, e.g. users with their
  preferences and permissions
