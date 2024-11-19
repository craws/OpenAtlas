Letters
=======

.. toctree::

The following step by step instruction describes how to enter a letter
exchange event.
The following elements are involved in the procedure:

* :doc:`/entity/artifact`: The physical presentation of the letter
* :doc:`/entity/source`: The content of the letter
* :doc:`/entity/event`: The **Move** of the letter from one place to another
* :doc:`/entity/place`: Start or end point of the letter exchange
* :doc:`/entity/actor`: Sender/recipient of the letter
* :doc:`/entity/type`: Used for classification, can be extended by users

Adding an artifact
------------------
The created artifact is the physical presentation of the letter. So the
begin of the date field would be the creation of the letter, etc.

* Click on :doc:`/entity/artifact` in the :doc:`/ui/menu` and create a new
  entry by using the **+ Artifact** button
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, such as letter
* Add further information e.g. a date or description
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
* Add more information as desired
* Press **Insert** to save the entry

**Please note**: It is important to link the artifact to the source in this way
to reflect that it is the source written on the letter.
If you would link it using the tab **Artifact** it means the source refers to
the artifact instead.

Adding the move event
---------------------
Now you can create a move event to track the sending of the letter from
one location to the other:

* After saving the source, you can see the linked artifact with its name in the
  source view. Click on it
* In the artifact view click on the **Event** tab in the menu and create a new
  move with the **+ Move** button
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, e.g. letter exchange
* With *from* and *to* you can choose the start and end location of the
  move
* The respective artifact should already be selected
* If available, enter the dates for the letter exchange
* Press **Insert** to save the entry

Adding sender and recipient
---------------------------
Now you can link one actor at by using the following steps:

* Open the created event by clicking on it in the event tab of the move
* Click on the **Actor** tab
* Either link an already exiting person from the list with **Link** or
  create a new one by using the **+ Person** button
* When entering the involvement information, choose the actor and add the
  respective type (sender/recipient)
* Press **Insert** to save the entry
