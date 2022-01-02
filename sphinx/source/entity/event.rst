Event
=====

.. toctree::

Available event classes based on `CIDOC CRM <http://www.cidoc-crm.org/>`_:

* **Activity** - the most common, e.g. a battle, a meeting or a wedding
* **Acquisition** - mapping a change of property
* **Move** - movement of artifacts or persons
* **Production** - creation of artifacts

.. include:: navigation.rst

Form fields
-----------
* :doc:`/form/name`
* :doc:`type`
* :doc:`/form/date`
* :doc:`/form/description`
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

Move
****
* **From** - a :doc:`place` as a start point
* **To** - a :doc:`place` as a destination point
* :doc:`artifact` - to select artifacts that were moved
* :doc:`Person <actor>` - to select persons that were moved

Acquisition
***********
* **Given Place** - to select which :doc:`places <place>` changed ownership.

To add **recipients** and **donors** go to the **Actor** tab, add actors and
select as activity:

* **acquired title through** for **recipients**
* **surrendered title through** for **donors**

Production
**********
* :doc:`artifact` - to select artifacts that were produced

The creators can be added via the **Actor** tab and selecting the **performed**
activity while linking them.
