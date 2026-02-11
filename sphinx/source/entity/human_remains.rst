Human remains
=============

.. toctree::

CIDOC documentation:
:cidoc_entity:`E20 Biological Object<e20-biological-object>`

"Human remains" is used to record anthropological data based on each human
bone. They are subunits of a :doc:`stratigraphic_unit` which itself is a
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
* **Carrier of source** - if a :doc:`source` is depicted on the remains
* :doc:`/tools/map`
* :doc:`reference_system`
* **Super** - a :doc:`place`, :doc:`feature`, :doc:`stratigraphic_unit`, or
  human remains, which it is a part of
* **Owned by** - the :doc:`actor` (person or group) who owns the remains
  such as museum

Can be linked via tabs to
-------------------------
* :doc:`source` - Use, if a human remains is mentioned in a source
* :doc:`event` - Acquisition, modification, move, and/or production can be
  linked
* **Subs** - Use, to add sub human remains
* :doc:`reference`
* :doc:`file`

Super and subunits
------------------
In the OpenAtlas database Human remains can be subunits of a
:doc:`stratigraphic_unit` (e.g. a human femur (human remains) of a skeleton
(stratigraphic unit) in a grave (feature)). A
Stratigraphic unit can consist of one or more Human remains (femur,
humerus and first molar of the same individual etc.) as well as finds (see
:doc:`artifact`).
