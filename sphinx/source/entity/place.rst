Place
=====

.. toctree::

CIDOC documentation:
:cidoc_entity:`E18 Physical Thing<e18-physical-thing>` and
:cidoc_entity:`E53 Place<e53-place>`

A place can be e.g. a continent, a city, or a graveyard.
For step by step instructions have a look at our :doc:`/examples/places`.

.. include:: navigation.rst

Form fields
-----------
* :doc:`/ui/name`
* :doc:`/ui/alias`
* :doc:`type` including place hierarchies
* :doc:`/ui/date`
* :doc:`/ui/description`
* :doc:`/tools/map`
* :doc:`reference_system`

Can be linked via tabs to
-------------------------
* :doc:`source` - if a source refers to a place
* :doc:`event` - you can link a place to a newly created event. It's not
  possible to link to existing events in this way; you can link a place to
  an existing event via the event's form though
* :doc:`reference`
* :doc:`artifact`
* :doc:`actor` - you can link a place to a newly created actor. It's not
  possible to link to existing actors in this way; you can link a place to
  an existing actor via the actor's form though
* :doc:`feature` - as subunit of a place (for more information see below)
* :doc:`file`

Places and their subunits
-------------------------
In OpenAtlas a place is a "physical thing" (CIDOC CRM
:cidoc_entity:`E18Physical Thing<e18-physical-thing>`) that has a certain
position and/or extends in space. It can be connected to various
other information (temporal, spatial, events, sources, etc.). Furthermore,
places can be divided into multiple subunits to record archaeological
information. For more information on subunits see :doc:`feature`,
:doc:`stratigraphic_unit`, :doc:`artifact`, and :doc:`/entity/human_remains`
as well as a detailed workflow example (:doc:`/examples/archaeological_data`).

An example of a place would be a graveyard. The place is the superior unit.
Each grave of this cemetery is considered a :doc:`feature` that forms the
cemetery. Each of those graves is composed of one or many subunits
(:doc:`stratigraphic_unit`)such as burials in the very grave
(e.g. a primary and a secondary burial) and its back filling. Each
stratigraphic unit may have associated :doc:`artifact`, e.g. the grave goods
of one of the burials or artifacts found in the back filling.
Anthropological information can be added via
:doc:`/entity/human_remains` - another subunit of stratigraphic unit.

.. image:: sub_unit.jpg

Adding multiple places
----------------------
It is not possible to link more than one place (or their subunits) to one
artifact. This problem can be solved by using :doc:`/examples/move_event`.
Please go to :doc:`/examples/artifacts` for more information.
