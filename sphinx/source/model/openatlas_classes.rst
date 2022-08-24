OpenAtlas classes
=================

.. toctree::

OpenAtlas uses several shortcuts in order to simplify connections between
entities that are always used the same way. All shortcuts can be resolved
according to :doc:`CIDOC CRM</cidoc_crm>` specifications and are valid
links. These shortcuts are indicated by a preceding OA in combination with a
number. Currently OpenAtlas uses 3 shortcuts:

OA7 - has relationship to
-------------------------

OA7 is used to link two instances of "E39 Actor" via a certain relationship; in
that way an actor can be linked with an actor.
E39 Actor linked with E39 Actor

* Domain: E39 - Actor
* Range: E39 - Actor

.. image:: oa7.png

Example:
[Stefan (E21)] participated in [Relationship from Stefan to Joachim (E5)] had
participant [Joachim (E21)]

The connecting event is defined by an entity of class E55 (Type):
[Relationship from Stefan to Joachim (E5)] has type [Son to Father (E55)]

OA8 - appears for the first time in
-----------------------------------

OA8 is used to link the beginning of a persistent item's (E77) life span
(or time of usage) with a certain place. E.g to document the birthplace of a
person.
E77 Persistent Item linked with a E53 Place.

* Domain: E77 - Persistent item
* Range: E53 - Place

.. image:: oa8.png

Example:
[Albert Einstein (E21)] was brought into existence by [Birth of Albert Einstein
(E12)] took place at [Ulm (E53)]

OA9 - appears for the last time in
----------------------------------

OA9 is used to link the end of a persistent item's (E77) life span
(or time of usage) with a certain place. E.g to document a person's place of
death.
E77 Persistent Item linked with a E53 Place.

* Domain: E77 - Persistent item
* Range: E53 - Place

.. image:: oa9.png

Example:
[Albert Einstein (E21)] was taken out of existence by [Death of Albert Einstein
(E12)] took place at [Princeton (E53)]
