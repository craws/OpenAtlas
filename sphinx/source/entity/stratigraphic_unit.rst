Stratigraphic unit
==================

.. toctree::

CIDOC documentation: :cidoc_entity:`E18 Physical Thing<e18-physical-thing>`

Stratigraphic units are primarily used to record archaeological data. They are
subunits of a :doc:`feature` which itself is a subunit of a :doc:`place`.
For an archaeological workflow example see
:doc:`/examples/archaeological_data`.

Form fields
-----------
* :doc:`/ui/name`
* :doc:`type`
* :doc:`/ui/date`
* :doc:`/ui/description`
* Super - a :doc:`feature` which it is a part of
* :doc:`/tools/map`

Can be linked via tabs to
-------------------------
* :doc:`source` - link if a stratigraphic unit is referenced in a source
* :doc:`event` - you can link a stratigraphic subunit to a newly created
  event. It's not possible to link to existing events in this way; you can
  link a place to an existing event via the event's form though
* :doc:`reference`
* :doc:`artifact`
* :doc:`human_remains`
* :doc:`file`

Anthropological analyses
------------------------

Clicking on the tools button leads you to the
:doc:`/tools/anthropological_analyses`.

Super and subunits
------------------
In the OpenAtlas database a Stratigraphic unit is a subunit of a :doc:`feature`.
A Feature can consist of one or more Stratigraphic units (e.g. grave as feature
can contain one or more burials, a backfilling, etc.). Stratigraphic units
themselves are structured in the same way and can be connected to
:doc:`artifact` and :doc:`human_remains` as their subunits.

.. image:: sub_unit.jpg
