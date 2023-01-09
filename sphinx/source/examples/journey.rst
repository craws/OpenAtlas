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
**Please note**, that that only individuals entered as person can be linked
to a move event later on. This is **not possible** for groups, as a move of
one or more groups can not be mapped with the current version of CIDOC CRM.

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
* Fill out the form, for more information see the :doc:`move event tutorial<move_event>`.
* **Please note**: do not link a person in this form if the journey was taken
  willingly.
  Link here only people who have not traveled of their own free will - think,
  for example, of a prisoner transport or the translation of relics. To see
  how to link (voluntary) travelers correctly, see below.
* **Please also note**: Use **preceding event** to document multiple
  parts of a trip. Unlike **sub events**, these can be put in chronological
  order. Sub events are there to capture events that happen at the same time
  (for more information see :doc:`move event tutorial<move_event>`).
* Click the **Insert** button to save the data or **Insert and continue**
  button to save and start to enter another move event

Link actors to the journey
--------------------------
To link actors (who have made a journey of their own free will) to the created
entry click on the blue **Actor** tab on the landing page of the respective
move event.

* Here, the Link button can be used to link people already entered into the
  database. The following information can be entered via the form:

    * at type you can define the role of the actor in the journey; if
      there is no suitable entry in the list, a new type can be created
      depending on the user's authorization, see the :doc:`types
      tutorial<types>`.
    * the actor can be changed afterwards via the **Change** button
    * the form of participation can be determined
    * in addition, dates and a free text description are possible

* via **+person** or **+group** new actors can be created and then linked to
  the move event
