Actor
=====

.. toctree::

CIDOC documentation: :cidoc_entity:`E21 Person<e21-person>` and
:cidoc_entity:`E74 Group<e74-group>`

* **Person** (:cidoc_entity:`E21 Person<e21-person>`) - A single person,
  such as Albert Einstein or Queen Victoria
* **Group** (:cidoc_entity:`E74 Group<e74-group>`) - A group of people,
  e.g. a family, a tribe, Greenpeace or the National Museum of
  Denmark

.. include:: navigation.rst

Form fields
-----------
* :doc:`/ui/name`
* :doc:`/ui/alias`
* :doc:`/ui/date`
* :doc:`/ui/description`
* **Residence** - A :doc:`place`, for a group this might be the location of an
  institute, for a person for example the main residence
* **Born in / Begins in** - The :doc:`place` where a person was born or a
  group came into existence
* **Died in / Ends in** - The :doc:`place` where a person died or a group ended
* :doc:`reference_system`

Can be linked via tabs to
-------------------------
* :doc:`source` - If an actor is mentioned in a source
* **Performed** - If an actor performed in an :doc:`event`, e.g. signed a
  treaty
* **Participated** - If an actor participated in an :doc:`event`, e.g.
  witnessed the signing of a treaty
* **Move** - If a person moved at an move :doc:`event`
* **Donor** - If an actor donated at an acquisition :doc:`event`
* **Recipient** - If an actor received at an acquisition :doc:`event`
* **Relation** - Use to specify relations to other actors such as parent of
  or married to
* **Member of** - Use to specify a group an actor is a member of
* **Member** - Link to actors to specify who was a member in a group (only
  available for groups)
* :doc:`artifact` - Use to specify which artifacts and/or human remains are
  owned by an actor (e.g. human remains that are kept in a museum)
* :doc:`reference` - Use to add citation
* :doc:`file` - Add a file, e.g. a picture of a person or group
