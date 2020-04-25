Event
=====

.. toctree::

Available event classes based on `CIDOC CRM <http://www.cidoc-crm.org/>`_:

* **Activity** - the most common, e.g. a battle, a meeting or a wedding
* **Acquisition** - this is a special case where a change of property can be mapped, see below
* **Move** - this event is for objects or person who moved

On the index page you can see already entered events.

* Click **+ Event** to enter a new one.
* Click on the **name** of an entry in the list to access the detail view.
* To edit an object, click on the **Edit** button in the detail view.

Form fields:

* :doc:`../form/name`
* :doc:`../form/type`
* :doc:`../form/date`
* :doc:`../form/description`
* **Location** - a :doc:`place` where the event occurred
* **Sub event of** - events can be part of another event, e.g. a battle as a sub event of a war.

**Acquisition** has an additional field:

* **Given Place** - to select which :doc:`places <place>` changed ownership.

To add **recipients** and **donors** go to the **Actor** tab, add actors and select as activity:

* **acquired title through** for **recipients**
* **surrendered title through** for **donors**

**Move** has additional fields:

* **From** - a :doc:`place` as a start point
* **To** - a :doc:`place` as a destination point
* :doc:`object` - to select objects that were moved
* :doc:`Person <actor>` - to select persons that were moved
