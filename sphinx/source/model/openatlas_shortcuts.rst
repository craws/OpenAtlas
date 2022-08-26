OpenAtlas shortcuts
===================

.. toctree::

OpenAtlas uses several shortcuts in order to simplify connections between
entities that are always used the same way. All shortcuts can be resolved
according to :doc:`CIDOC CRM<cidoc_crm>` specifications and are valid
links. These shortcuts are indicated by a preceding OA in combination with a
number. Currently OpenAtlas uses 3 shortcuts:

OA7 - has relationship to
-------------------------

OA7 is used to link two instances of "E39 Actor" via a certain relationship; in
that way an actor can be linked with an actor.
E39 Actor linked with E39 Actor

* Domain: **E39 - Actor**
* Range: **E39 - Actor**

.. image:: oa7.png

::

   E39(Actor) - P11i(participated in) - E5(Event) - P11(had participant) - E39(Actor)

Example:
[Stefan (E21)] participated in [Relationship from Stefan to Joachim (E5)] had
participant [Joachim (E21)]

The connecting event is defined by an entity of class E55 - Type:
[Relationship from Stefan to Joachim (E5)] has type [Son to Father (E55)]

OA8 - appears for the first time in
-----------------------------------

OA8 is used to link the beginning of a Persistent Item's (E77) life span
(or time of usage) with a certain place. E.g to document the birthplace of a
person.

E77 Persistent Item linked with a E53 Place.

* Domain: **E77 - Persistent Item**
* Range: **E53 - Place**

.. image:: oa8.png

::

   E77(Persistent Item) - P92i(was brought into existence by) - E63(Beginning of Existence) - P7(took place at) - E53(Place)

Example:
[Albert Einstein (E21)] was brought into existence by [Birth of Albert Einstein
(E12)] took place at [Ulm (E53)]

OA9 - appears for the last time in
----------------------------------

OA9 is used to link the end of a Persistent Item's (E77) life span
(or time of usage) with a certain place (E53). E.g to document a person's place of
death.
E77 Persistent Item linked with a E53 Place.

* Domain: **E77 - Persistent Item**
* Range: **E53 - Place**

.. image:: oa9.png

::

   E77(Persistent Item) - P93i(was taken out of existence by) - E64(End of Existence) - P7(took place at) - E53(Place)

Example:
[Albert Einstein (E21)] was taken out of existence by [Death of Albert Einstein
(E12)] took place at [Princeton (E53)]

Dates
-----

For dates, data is stored in the table model.entity respectively model.link in
the fields begin_from, begin_to, begin_comment, end_from, end_to, end_comment
as timestamps.
Depending on class of the entity respectively the domain and range classes of
the link, these dates can be mapped as CIDOC CRM **E61 - Time Primitive**
entities.

E77 - Persistent Item
+++++++++++++++++++++

E77 Persistent Item **begin** linked with a E61 Time Primitive:

* Domain: **E77 - Persistent Item**
* Range: **E61 - Time Primitive**

.. image:: e77_begin.png

::

   E77(Persistent Item) - P92i(was brought into existence by) - E63(Beginning of Existence) - P4(has time span) - E52(Time Span) - P81(ongoing throughout) - E61(Time Primitive)

Example: [Holy Lance (E22)] was brought into existence by [forging of Holy
Lance (E12)] has time span [Moment/Duration of Forging of Holy Lance (E52)]
ongoing throughout [0770-12-24 (E61)]

E77 Persistent Item **end** linked with a E61 Time Primitive:

* Domain: **E77 - Persistent Item**
* Range: **E61 - Time Primitive**

.. image:: e77_end.png

::

   E77(Persistent Item) - P93i(was taken out of existence by) - E64(End of Existence) - P4(has time span) - E52(Time Span) - P81(ongoing throughout) - E61(Time Primitive)

Example: [The one ring (E22)] was destroyed by [Destruction of the one ring
(E12)] has time span [Moment of throwing it down the lava (E52)] ongoing
throughout [3019-03-25 (E61)]

E21 Person
++++++++++

E21 Person's **Birth** linked with a E61 Time Primitive:

* Domain: **E21 - Person**
* Range: **E61 - Time Primitive**

.. image:: e21_birth.png

::

   E21(Person) - P98i(was born) by - E67(Birth) - P4(has time span) - E52(Time Span) - P81(ongoing throughout) - E61(Time Primitive)

Example: [Stefan (E21)] was born by [birth of Stefan (E12)] has time span
[Moment/Duration of Stefan's birth (E52)] ongoing throughout [1981-11-23 (E61)]

E21 Person's **Death** linked with a E61 Time Primitive:

* Domain: **E21 - Person**
* Range: **E61 - Time Primitive**

.. image:: e21_death.png

::

   E21(Person) - P100i(died in) - E69(Death) - P4(has time span) - E52(Time Span) - P81(ongoing throughout) - E61(Time Primitive)

Example: [Lady Diana (E21)] died in [death of Diana (E69)] has time span
[Moment/Duration of Diana's death (E52)] ongoing throughout [1997-08-31 (E61)]

E2 Temporal Entity
++++++++++++++++++

E2 Temporal Entity (also property) **begin** linked with a E61 Time Primitive:

* Domain: **E2 - Temporal Entity**
* Range: **E61 - Time Primitive**

.. image:: e2_begin.png

::

   E2(Temporal Entity) - P4(has time span) - E52(Time Span) - P81(ongoing throughout) - E61(Time Primitive)

Example: [Thirty Years' War (E7)] has time span [Moment/Duration of Beginning
of Thirty Years' War (E52)] ongoing throughout [1618-05-23 (E61)]

E2 temporal entity (also property) **end** linked with a E61 Time Primitive:

* Domain: **E2 - Temporal Entity**
* Range: **E61 - Time Primitive**

.. image:: e2_begin.png

::

   E2(temporal entity) - P4(has time span) - E52(Time Span) - P81(ongoing throughout) - E61(Time Primitive)

Example: [Thirty Years' War (E7)] has time span [Moment/Duration of End of
Thirty Years' War (E52)] ongoing throughout [1648-10-24 (E61)]
