Feature
=======

.. toctree::

CIDOC documentation: :cidoc_entity:`E18 Physical Thing<e18-physical-thing>`

Features are subunit of a :doc:`place` and used in archaeological data
  recording. E.g. graves or buildings of a site would be considered Features.

Form fields
-----------
* :doc:`/form/name`
* :doc:`type`
* :doc:`/form/date`
* :doc:`/form/description`
* :doc:`/tools/map`

Can be linked via tabs to
-------------------------
* :doc:`source` - when it is referenced there
* :doc:`event` - only for new events. For existing the location at the event
  itself can be edited.
* :doc:`reference`
* :doc:`stratigraphic_unit`
* :doc:`file`

Super and subunits
------------------
In the OpenAtlas database a feature is a subunit of a :doc:`place`.
A :doc:`place` can consist of one or more subunits called Features
(e.g. buildings, graves, pits, ditches, ramparts etc.).
Features themselves are structured in the same way as Places and can consist
of one or more subunits that are labelled as :doc:`stratigraphic_unit`.

.. image:: sub_unit.jpg
