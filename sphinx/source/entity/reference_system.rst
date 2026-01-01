Reference System
================

.. toctree::

CIDOC documentation:
:cidoc_entity:`E32 Authority Document<e32-authority-document>`

Reference systems can be used to link entities to external sources. A list with
available reference systems is provided when clicking the
**Reference system** button on the start page.

Linking entities to external reference systems has many advantages such as
being able to find or provide more information from other sources. Furthermore,
they facilitate the merge of data sets. By using reference systems LOD (Linked
Open Data) can be created.
Furthermore, analogue reference systems such as library catalogues or
inventory numbers of a museum can be used in this way.

For step by step instructions how to add a reference system have a look at our
:doc:`/examples/reference_systems` example.

Included by default
-------------------
The following reference systems are pre-installed. By using their provided
APIs, OpenAtlas can provide search functionality in the respective form fields
and display information about already linked entities in the corresponding
entity detail view.

Wikidata
********
`Wikidata <https://wikidata.org/>`_ is a collaboratively edited multilingual
knowledge graph hosted by the Wikimedia Foundation. It is a common source of
open data for Wikimedia projects such as Wikipedia. Everyone is able
to use the information under the CC0 public domain license.

By default it is usable for **places, persons and groups** within OpenAtlas.

GeoNames
********
`GeoNames <https://www.geonames.org/>`_ is a user-editable geographical
database available and accessible through various web services, under a
Creative Commons attribution license. The GeoNames database contains over
25,000,000 geographical names corresponding to over 11,800,000 unique features.

The GeoNames search functionality is integrated in the map search field.
This enables users to automatically use the provided coordinates and
identifiers for specific places.

By default it is usable for **places** in OpenAtlas.

GND
***
The `GND <https://d-nb.info/standards/elementset/gnd>`_ or Gemeinsame Normdatei
(translated as Integrated Authority File) is an international authority
file for the organisation of personal names, subject headings, and corporate
bodies from catalogues. It is used mainly for documentation in libraries and
increasingly also by archives and museums.

By default it is usable for **persons** in OpenAtlas.

Usage
-----
Links consists of an identifier (ID) and a precision and can be entered when
adding or updating an entity.

ID
**
The identifier of an entity in the external reference system. For GeoNames
and Wikidata IDs will be checked for a valid format.

Precision
*********
When linking to an external reference a precision is required. Available
options are the `SKOS <https://www.w3.org/TR/skos-primer/>`_ based definitions
of confidence degree.

* **Close match**: Concepts (here a dataset in OpenAtlas and a dataset in an
  external reference system) are sufficiently similar, therefore they can be
  used interchangeably in some information retrieval applications
* **Exact match**: High degree of confidence that the concepts (a dataset in
  OpenAtlas and a dataset in an external reference system) can be used
  interchangeably

E.g. if a historical project links the city of Vienna in Wikidata, a
**close match** would be more suitable, as the Wikidata entry deals
primarily with the current city Vienna and not the historical place.

Configuration
-------------
Admins and manager can add, update, and delete external reference systems.

* **Name** - e.g. Wikipedia; the name can not be changed for the
  pre-installed reference systems Wikidata and GeoNames
* **External reference match** - default precision selected in forms
* **Website URL** - URL of the reference system (e.g.
  `Wikidata <https://wikidata.org/>`_ for Wikidata)
* **Resolver URL** - URL that - in combination with the ID - links to an
  entity in the reference system (e.g. the resolver URL
  **https://www.wikidata.org/wiki/** in combination with the ID **Q123**
  creates the external link: https://www.wikidata.org/wiki/Q123 (September)
* **Example ID** - an example id to show the desired format (e.g. Q123
  for Wikidata)
* **Classes** - a checkbox list of available classes, for GeoNames only place
  is available
* **Description** - a short description, shown in forms when mouse over
  the **i** icon

Classes can be removed from a reference system by clicking on the tab with the
corresponding class name and clicking the **Remove** button. This button is
only available if there are no entities of this class linked to it yet.

Reference systems can be deleted only if no classes are attached to it.
Wikidata and GeoNames are integrated into OpenAtlas and cannot be deleted but,
if desired, can be disabled by removing the classes.
