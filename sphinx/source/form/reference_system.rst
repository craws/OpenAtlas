Reference Systems
=================

.. toctree::

Reference systems can be used to link entities to external sources e.g. to Wikidata or GeoNames
which are already included in the default application. You can see a list of available systems when
clicking the **Reference system** button on the start page. Links consists of an identifier (id)
and a precision.

Id
--
The identifier of the entity in the external reference system. For GeoNames and Wikidata it will be
checked for a valid format.

Precision
---------
The precision is a required field. There may be a default set already. The two possible
(`SKOS <https://www.w3.org/TR/skos-primer/>`_) values are:

* Close match: Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.
* Exact match: High degree of confidence that the concepts can be used interchangeably.

E.g. if a historical project links the city Vienna to Wikidata a close match would be more suitable
because the Wikidata entry is more about the current city and not the historical one.

Configuration
-------------
Admins and manager can add, updated and delete external reference systems.

* Name - e.g. Wikipedia, can not be changed for Wikidata or GeoNames
* Website URL - an URL to the project site of the reference system
* Resolver URL - if available an URL that can be linked to in combination with the id
* Example ID - an example id to show the desired format e.g. Q123 for Wikidata
* External Reference Match - a default can be set here, e.g. close match for GeoNames at an historical project
* Description - a short description which will be shown in forms when hovering the mouse over the **i** icon


