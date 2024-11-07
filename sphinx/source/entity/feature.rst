Feature
=======

.. toctree::

CIDOC documentation: :cidoc_entity:`E18 Physical Thing<e18-physical-thing>`

Features are subunit of a :doc:`place` and used in archaeological data
recording. E.g. graves or buildings of an archaeological site would be
considered features.

Form fields
-----------
* :doc:`/ui/name`
* :doc:`type`
* :doc:`/ui/date`
* :doc:`/ui/description`
* Super - :doc:`place` the feature is a part of
* :doc:`/tools/map`

Can be linked via tabs to
-------------------------
* :doc:`source` - use, if a feature is referenced in it
* :doc:`event` - use only for new events. For already existing events link
  the location in the event form
* :doc:`reference` can be used to add a citation
* :doc:`stratigraphic_unit` is used to link a subunit of a feature (e.g. a
  skeleton (stratigraphic unit) in a grave (feature))
* :doc:`file` can be used to add files such as pictures

Super and subunits
------------------
In the OpenAtlas database a feature is a subunit of a :doc:`place`.
A :doc:`place` can consist of one or more subunits called Features
(e.g. buildings, graves, pits, ditches, ramparts etc.).
Features themselves are structured in the same way as Places and can consist
of one or more subunits that are labelled as :doc:`stratigraphic_unit`.

.. image:: sub_unit.jpg
