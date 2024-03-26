Human remains
=============

.. toctree::

CIDOC documentation:
:cidoc_entity:`E20 Biological Object<e20-biological-object>`

Human remains are used to record anthropological data based on single human
bones. They are subunits of a :doc:`stratigraphic_unit` which itself is a
subunit of :doc:`feature`. Please note that information on the biological sex,
gender, and age of an individual can be entered in the stratigraphic unit
entry mask. For an archaeological workflow example see
:doc:`/examples/archaeological_data`.

Form fields
-----------
* :doc:`/ui/name`
* :doc:`type`
* :doc:`/ui/date`
* :doc:`/ui/description`
* :doc:`/tools/map`
* :doc:`reference_system`
* **Super** - a :doc:`place`, :doc:`feature`, :doc:`stratigraphic_unit` or
  human remains, which it is a part of
* **Owned by** - the :doc:`actor` who owns the artifact

Can be linked via tabs to
-------------------------
* :doc:`source` - when it is referenced there
* :doc:`event` - acquisition, modification, move or production
* :doc:`artifact` - here sub artifacts or human remains can be added
* :doc:`reference`
* :doc:`file`

Super and subunits
------------------
In the OpenAtlas database Human remains can be subunits of a
:doc:`stratigraphic_unit`. A Stratigraphic unit can consist of one or more
Human remains (e.g. femur, humerus and first molar of the same individual,
etc.) as well as finds (see :doc:`artifact`).
