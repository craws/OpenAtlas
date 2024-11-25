CIDOC CRM
==========

.. toctree::

The `CIDOC Conceptual reference model <https://www.cidoc-crm.org/>`_ is a
widely used ontology in the digital humanities as well as an
`ISO standard <https://www.iso.org/standard/57832.html>`_.
It is a formal ontology, developed by an developed by an interdisciplinary team
in connection with the International Council of Museums
(`ICOM <https://icom.museum/en/>`_).

In OpenAtlas its current version,
`CIDOC CRM v7.1.2 <https://cidoc-crm.org/Version/version-7.1.2>`_ published in
May 2021, is used as underlying data model of the database.

A script is used to parse the specification and import it into a
`PostgreSQL <https://www.postgresql.org/>`_ database (more information is
available on `GitHub <https://github.com/craws/OpenAtlas/tree/main/install>`_).
In this way all data is mapped to CIDOC CRM automatically without the
users having to familiarise themselves with the ontology.

The ontology consists of classes, linked together by properties.

CIDOC classes
-------------
Classes are indicated by a preceding **E** followed by a numeric code - e.g.
“:cidoc_entity:`E39 - Actor<e39-actor>`” or
“:cidoc_entity:`E67 - Birth<e67-birth>`”.
All entities used within OpenAtlas can be characterised as CIDOC classes.
An overview of all CIDOC CRM classes can be found
`here <https://demo.openatlas.eu/overview/model/cidoc_class_index>`_.
The displayed count indicates how many times each class has been used in
your OpenAtlas instance.
A click on the class name will bring you to an overview of the class with
detailed information, such as a short description, sub- and super classes as
well as possible properties.


CIDOC Properties
----------------
CIDOC properties are indicated by a combination of the letter “P” and a
numerical sequence - think
“:cidoc_property:`P11 - had participant<p11-had-participant>`” or
":cidoc_property:`P2 - has type<p2-has-type>`“. They are used to link a
class to another class. So an activity taking place at a certain location,
can be modelled in the following way

.. image:: properties.png

An overview of all CIDOC CRM properties can be found
`here <https://demo.openatlas.eu/overview/model/property>`_. The displayed
count indicates how many times each property has been used in your OpenAtlas
instance.
A click on the property name will bring you to an overview of the property with
detailed information, such as a short description.

OpenAtlas does not import nor use inverse properties (properties ending with
the letter i) since all used links are directed anyway. Nevertheless their
labels are imported for more convenient browsing possibilities of relations.
Properties with URLs as domain/range are ignored as the system used here
has a foreign key on domain which must match an existing class.
Also some properties are linked as "sub_properties_of" properties with the i
suffix. Since we don't use inverse properties in the database
(direction is determined through domain/range selection) they are linked to
their counterpart without i.

There are some "special" properties that are not included in OpenAtlas, e.g.
:cidoc_property:`P3 - has note<P3-has-note>`. They can be found in the
`OpenAtlas CIDOC parser script <https://github.com/craws/OpenAtlas/blob/main/install/crm/cidoc_rtfs_parser.py>`_
on GitHub, where they are defined on the top:
These properties are not import due to technical reasons, e.g. missing
definitions that "normal" properties have or no defined range.
