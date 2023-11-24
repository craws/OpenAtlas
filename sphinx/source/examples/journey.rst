Journey
=======

.. toctree::

The following steps describe how to enter a journey as move event. For more
information on move events in general see this :doc:`tutorial<move_event>`.
On move events concerning artifacts, have a look at the
:doc:`letter tutorial<letters>`.

These steps describe how to enter a journey as special case of a **move
event**. To create a new move event following elements are involved in the
procedure:

* :doc:`/entity/actor`: the person/persons that went on a journey
* :doc:`/entity/event`: the **Move** of the letter from one place to another
* :doc:`/entity/place`: start or end point of the journey
* :doc:`/entity/type`: used for classification, can be extended by users

Adding actors
-------------
If not all :doc:`actors</entity/actor>` involved in the journey were
entered into the database already, add them via a click on the respective
tab in the :doc:`menu</ui/menu>`. Here, click the **+ Person** button to get to
the form. As for all other forms, a name is required to save the data.

Adding locations
----------------
If not all :doc:`locations</entity/place>` involved in the journey were
entered into the database already, add them via a click on the respective
tab in the :doc:`menu</ui/menu>`. Here, click the **+ Place** button to get to
the form. As for all other forms, a name is required to save the data.

Creating the move event
-----------------------
The following steps will create a move event:

* Click on the **Event** tab in the menu then use the **+ Move** button
* Fill out the form, for more information see the
  :doc:`move event tutorial<move_event>`.
* Link persons in this form who made the journey
* **Please also note**: Use **preceding event** to document multiple
  parts of a trip. Unlike **sub events**, these can be put in chronological
  order. Sub events are there to capture events that happen at the same time
  (for more information see :doc:`move event tutorial<move_event>`).
* Click the **Insert** button to save the data or **Insert and continue**
  button to save and start to enter another move event

Link actors to the journey
--------------------------
Already entered persons (and artifacts) can be added at the event form which
creates a **moved by** relation to the event. Unfortunately this is not
possible for groups in the current version of CIDOC CRM.

Alternatively, actors (persons and groups) can be added via the actor tab where
it is also possible to create new ones via the **+ Person** and **+ Group**
button. In this case a more general **participated at** relation will be used
between actors and event. It is also possible to add additional information:

* At type you can define the role of the actor in the journey; if
  there is no suitable entry in the list, a new type can be created
  depending on the user's authorization, see the :doc:`types
  tutorial<types>`.
* The actor can be changed afterwards via the **Change** button
* The form of participation can be determined
* In addition, dates for the participation (in case they differ from the
  event) and a free text description are possible
