Journey
=======

.. toctree::

A journey can be tracked in OpenAtlas as a series of move events as
described in the following steps. For more information on move events in
general see this :doc:`tutorial<move_event>`.
On move events concerning artifacts, have a look at the
:doc:`letter tutorial<letters>`.

The following steps describe how to enter a journey as special case of a **move
events**. To create a new move event the following elements are involved in the
procedure:

* :doc:`/entity/actor`: The person/persons that moved/went on a journey
* :doc:`/entity/event`: The **Move** of a letter or person from one place to
  another
* :doc:`/entity/place`: Start or end point of the move event
* :doc:`/entity/type`: Used for classification, list of types can be extended
  by users

Adding actors
-------------
If not all :doc:`actors</entity/actor>` involved in the journey were
entered into the database already, add them via a click on the respective
tab in the :doc:`menu</ui/menu>`. Here, click the **+ Person** button to get to
the form. As for all other forms, at least a name is required to save the data.

Adding locations
----------------
If not all :doc:`locations</entity/place>` involved in the journey were already
entered into the database, add them via a click on the respective tab in the
:doc:`menu</ui/menu>`. Here, click the **+ Place** button to get to
the form. As for all other forms, at least a name is required to save the data.

Creating the move event
-----------------------
The following steps will create a move event:

* Click on the **Event** tab in the menu then use the **+ Move** button
* Fill out the form, for more information see the
  :doc:`move event tutorial<move_event>`.
* Link one or more persons that went on the trip
* **Please also note**: Use **preceding event** to document multiple
  parts of a trip. Unlike **sub events**, these can be put in chronological
  order. Use **sub events** to capture events that happen at the same time
  (for more information see :doc:`move event tutorial<move_event>`).
* Click the **Insert** button to save the data or **Insert and continue**
  button to save and start to enter another move event

Link actors to the journey
--------------------------
Already entered persons (and artifacts) can be added at the event form which
creates a **moved by** relation to the event. Unfortunately this is not
possible for groups in the current version of CIDOC CRM.

Alternatively, actors (persons and groups) can be added via the actor tab where
it is also possible to create new actor entities via the **+ Person** and
**+ Group** button. In this case a more general **participated at** relation
will be created between actors and events. It is also possible to add additional
information:

* Via type you can define the role of an actor in a journey; if
  there is no suitable type in the list, a new one can be created
  depending on the user's OpenAtlas status. For more see the
  :doc:`types tutorial<types>`.
* The actor can be changed afterwards via the **Change** button
* In addition, dates for a participation (in case they differ from the
  event) and a free text description can be added
