CIDOC CRM
==========

.. toctree::

The `CIDOC Conceptual reference model <https://www.cidoc-crm.org/>`_ is a
widely used ontology in the digital humanities as well as an
`ISO standard <https://www.iso.org/standard/57832.html>`_.
It is a formal ontology, developed by an developed by an interdisciplinary team
in connection with the International Council of Museums
(`ICOM <https://icom.museum/en/>`_).

The ontology consists of classes, linked together by properties.

CIDOC classes
-------------
Classes are indicated by a preceding **E** followed by a numeric code-e.g. “E29
Actor” or “E67 Birth”.
All entities used within OpenAtlas can be characterised as CIDOC classes.
An overview of all CIDOC CRM classes can be found
`at <https://demo.openatlas.eu/overview/model/cidoc_class_index>`_. The count
indicates how many times each class has been used in this database instance.
A click on the class name will get you to an overview of the class with
detailed information, such as a short description, sub- and super classes as
well as possible properties.


CIDOC Properties
----------------
CIDOC entities are indicated by a combination of “P” and a numerical sequence -
think “P26 moved to” or “P52 has current owner”. They are used to link classes
to other classes. So when an activity to place at a certain location, this can
be modelled in the following way

.. image:: properties.png

An overview of all CIDOC CRM properties can be found
`here <https://demo.openatlas.eu/overview/model/property>`_. The count
indicates how many times each property has been used in this database instance.
A click on the property name will get you to an overview of the property with
detailed information, such as a short description.
