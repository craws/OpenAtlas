Reference System
================

.. toctree::

CIDOC documentation:
:cidoc_entity:`E32 Authority Document<e32-authority-document>`

Reference systems can be used to link entities to external sources. You can
see a list of available systems by clicking the **Reference system** button on
the start page.

Linking entities to external reference systems has many advantages like
being able to find or provide more information from other sources and it makes
it a lot easier to merge/compare data from other projects using the same
reference systems.

For step by step instructions to add a reference system have a look at our
:doc:`/examples/reference_systems` example.

Included by default
-------------------
These systems are all included in the default application. Furthermore,
it was made use of their APIs to provide search functionality inside of
OpenAtlas and display their information about already linked entities at the
corresponding entity detail view.

Wikidata
********
`Wikidata <https://wikidata.org/>`_ is a collaboratively edited multilingual
knowledge graph hosted by the Wikimedia Foundation. It is a common source of
open data that Wikimedia projects such as Wikipedia, and anyone else, is able
to use under the CC0 public domain license.

By default it is usable for **places, persons and groups**.

GeoNames
********
`GeoNames <https://www.geonames.org/>`_ is a user-editable geographical
database available and accessible through various web services, under a
Creative Commons attribution license. The GeoNames database contains over
25,000,000 geographical names corresponding to over 11,800,000 unique features.

For GeoNames the search is integrated in search at the map and it is also
possible to take over their coordinates for specific places.

By default it is usable for **places**.

GND
***
The `GND <https://d-nb.info/standards/elementset/gnd>`_ or Gemeinsame Normdatei
(translated as Integrated Authority File) is an international authority
file for the organisation of personal names, subject headings and corporate
bodies from catalogues. It is used mainly for documentation in libraries and
increasingly also by archives and museums.

By default it is usable for **persons**.

Usage
-----
Links consists of an identifier (ID) and a precision and can be entered when
adding or updating an entity.

ID
**
The identifier of the entity in the external reference system. For GeoNames
and Wikidata it will be checked for a valid format.

Precision
*********
When linking to an external reference a precision is required. Available
options are the `SKOS <https://www.w3.org/TR/skos-primer/>`_ based definitions
of the confidence degree that concepts can be used interchangeable.

* **Close match**: Concepts are sufficiently similar that they can be used
  interchangeably in some information retrieval applications
* **Exact match**: High degree of confidence that the concepts can be used
  interchangeably

E.g. if a historical project links the city of Vienna to Wikidata, a
**close match** would be more suitable, because the Wikidata entry is more
about the current city and not the historical one.

Configuration
-------------
Admins and manager can add, update and delete external reference systems.

* **Name** - e.g. Wikipedia; can not be changed for Wikidata or GeoNames
* **Website URL** - an URL to the project site of the reference system
* **Resolver URL** - an URL that can be linked to in combination with an ID,
  e.g. the resolver URL **https://www.wikidata.org/wiki/** would create
  together with a **Q123**
  identifier the external link: https://www.wikidata.org/wiki/Q123
* **Example ID** - an example id to show the desired format e.g. Q123
  for Wikidata
* **External reference match** - default precision selected in forms
* **Description** - a short description, shown in forms when mouse over
  the **i** icon
* **Classes** - a checkbox list of available classes, for GeoNames only place
  is available

Classes can be removed from a system by clicking on the tab with the
corresponding class name and clicking the **Remove** button. This button is
only available if there are no entities of this class linked to the reference
system.

Reference systems can be deleted only if no classes are attached to it.
Wikidata and GeoNames are integrated and cannot be deleted but if desired they
can be disabled by removing the classes.
