Letters
=======

.. toctree::

The following steps describe how to enter a letter exchange event.
The following elements are involved in the procedure:

* :doc:`/entity/artifact`: the physical presentation of the letter
* :doc:`/entity/source`: the content of the letter
* :doc:`/entity/event`: the **Move** of the letter from one place to another
* :doc:`/entity/place`: Start or end point of the letter exchange
* :doc:`/entity/actor`: Sender/recipient of the letter
* :doc:`/entity/type`: used for classification, can be extended by users

Adding an artifact
------------------
The created artifact is the physical presentation of the letter and the
following data concerns the object e.g. the begin date would be the creation of
the letter, the description can be used to record e.g. the material of
the object.

* Click on :doc:`/entity/artifact` in the :doc:`/ui/menu` and create a new
  entry by using the **+ Artifact** button
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, e.g. letter
* Add further information as date or description if available
* Press **Insert** to save the entry

Adding a source
---------------
With :doc:`/entity/source` you can record the content of said letter. For
example, if there are copies of the letter, they all have the same text
(= source).

* Click on :doc:`/entity/source` in the menu and create a new entry by using
  the **+ Source** button
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list
* Click on **Artifact** and choose the before created letter from the list
* Press **Insert** to save the entry

It is important to link the artifact to the source in this way to reflect that
it is the source written on the letter.
If you would link it using the tab **Artifact** it means the source refers to
the artifact instead.

Adding the move event
---------------------
This creates an entry concerning the movement of the letter.

* After saving the source, you can see the linked artifact with its name in the
  source view and click on it
* In the artifact view click on the **Event** tab in the menu and create a new
  move with the **+ Move** button
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, e.g. letter exchange
* With *from* and *to* you can choose the starting and ending location of the
  move
* The respective artifact should already be preset
* If available, enter the dates for the letter exchange
* Press **Insert** to save the entry

Adding sender and recipient
---------------------------
Now you can link one actor at a time to the move event by the following steps.

* Open the created event by clicking on it in the event tab of the move
* Click on the **Actor** tab
* Either link an already entered person with **Link** or create a new one with
  **+ Person** button
* When entering the involvement information, choose the actor and add the
  respective type (sender/recipient)
* Press **Insert** to save the entry
