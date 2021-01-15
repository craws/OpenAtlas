Actor
=====

.. toctree::

Available event classes based on `CIDOC CRM <http://www.cidoc-crm.org/>`_:

* **Person**
* **Group** - e.g. a family or the Association for the Preservation of the Coelacanth
* **Legal Body** - e.g. Greenpeace or the National Museum of Denmark

.. include:: navigation.rst

Form fields
-----------
* :doc:`/form/name`
* :doc:`/form/alias`
* :doc:`/form/date`
* :doc:`/form/description`
* **Residence** - a :doc:`place`, e.g. the location of an institute or the main residence of an actor
* **Born in / Begins in** - the :doc:`place` where a person was born or a group/legal body began
* **Died in / Ends in** - the :doc:`place` where a person died or a group/legal body ended
* :doc:`/form/reference_system`

Can be linked via tabs to
-------------------------
* :doc:`source` - when it is referenced there
* :doc:`event` - for participation
* **Relation** - to other actors
* **Member of** - to groups or legal bodies it is member of
* **Member** - to actors who are members (only available for groups and legal bodies)
* :doc:`reference`
* :doc:`/tools/file`
