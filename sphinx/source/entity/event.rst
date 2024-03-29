Event
=====

.. toctree::

CIDOC documentation:
:cidoc_entity:`E7 Activity<e7-activity>`,
:cidoc_entity:`E8 Acquisition<e8-acquisition>`,
:cidoc_entity:`E5 Event<e5-event>`,
:cidoc_entity:`E11 Modification<e11-modification>`,
:cidoc_entity:`E9 Move<e9-move>`,
:cidoc_entity:`E12 Production<e12-production>` and
:cidoc_entity:`E65 Creation<e65-creation>`

* **Activity** (:cidoc_entity:`E7 Activity<e7-activity>`)
  - the most common, e.g. a battle, a meeting or a wedding
* **Acquisition** (:cidoc_entity:`E8 Acquisition<e8-acquisition>`)
  - mapping a change of property
* **Creation** (:cidoc_entity:`E65 Creation<e65-creation>`)
  - creation of documents (files)
* **Event** (:cidoc_entity:`E5 Event<e11-modification>`)
  - used for events not performed by actors, e.g. a natural disaster
* **Modification** (:cidoc_entity:`E11 Event<e5-event>`)
  - used for modification of artifacts, e.g. a conservation treatment
* **Move** (:cidoc_entity:`E9 Move<e9-move>`)
  - movement of artifacts or persons
* **Production** (:cidoc_entity:`E12 Production<e12-production>`)
  - creation of artifacts

.. image:: event_hierarchy.png

`CIDOC CRM <https://www.cidoc-crm.org/>`_ hierarchy for the different types of
events included in OpenAtlas.

.. include:: navigation.rst

Form fields
-----------
* :doc:`/ui/name`
* :doc:`type`
* :doc:`/ui/date`
* :doc:`/ui/description`
* **Location** - a :doc:`place` where the event occurred
* **Sub event of** - events can be part of another event,
  e.g. a battle as a sub event of a war.
* **Preceding event** - events can follow up other events, useful for e.g.
  entering a journey
* :doc:`reference_system`

Can be linked via tabs to
-------------------------
* :doc:`source` - when it is referenced there
* :doc:`actor` - to add participants, or recipient and donor for an acquisition
* :doc:`reference`
* :doc:`file`

For step by step instructions have a look at our :doc:`/examples/index`.

Acquisition
***********
* **Given place** - to select which :doc:`places <place>` changed ownership.
* **Given artifact** - to select which :doc:`artifacts <artifact>`
  changed ownership.

To add **recipients** and **donors** go to the **Actor** tab, add actors and
select as activity:

* **acquired title through** for **recipients**
* **surrendered title through** for **donors**

Creation
********
* Document (:doc:`file`) - to select files that were created

The creators of the document can be added via the **Actor** tab and selecting
the **carried out by** activity while linking them.

Modification
************
* :doc:`artifact` - to select artifacts that were modified

The creators of the artifact can be added via the **Actor** tab and selecting
the **carried out by** activity while linking them.

Move
****

* **From** - a :doc:`place` as a start point
* **To** - a :doc:`place` as a destination point
* Moved :doc:`artifact` - to select moved artifacts
* Moved :doc:`Person <actor>` - to select moved persons

Unfortunately CIDOC CRM doesn't allows a **moved by** relation for groups. It
is still possible to "move" groups via the actor tab which in the background
creates a more general **participated at** relation between actor and move
event. For more information please take a look at :doc:`/examples/journey` or
:doc:`/examples/move_event` tutorial.

Production
**********
* :doc:`artifact` - to select artifacts that were produced

The creators of the artifact can be added via the **Actor** tab and selecting
the **carried out by** activity while linking them.
