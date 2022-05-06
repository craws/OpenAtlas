Move events
===========

.. toctree::

Various move events can be mapped via OpenAtlas, including journeys and the
sending and receiving of letters.

Create a new move event - general instruction
---------------------------------------------

As move events are a subgroup of :doc:`events</entity/event>`, click
**Event** in the menu to create a new entry. This will bring you to the
event overview page where you can find the **+Move** button.
By clicking it a form will open in which you can add the following
information:

* A descriptive **name** for the move event; as in other forms, a name
  is required to save information
* A fitting **type** for the move event; if you can not find one in the
  list, it might be possible for you to add new types - depending on
  your :doc:`user group</admin/user>` (please see this
  :doc:`tutorial<types>` for more information)
* you can add one or more **sub events**. Please keep in mind: Sub events
  cannot be added in a temporal order and are used to represent events that
  occur simultaneously. Examples are a music festival with parallel concerts
  or a war with overlapping battles at different locations. To represent a
  temporal sequence, use **preceding event** (for a short
  introduction see the :doc:`journey` tutorial). You can
  select the event from a list of already entered events. If the event you are
  looking for cannot be found in this list, please add it via **Event** in the
  menu and then link it
* you can add one or more **preceding events**, for more information see
  above or the :doc:`journey` tutorial
* via **from** you can add a location from where the move event started,
  think the starting point of a journey or the place a letter was send from.
  You can choose a location from a list of already added locations. If the
  place  you are looking for is not in this list yet, please add it via
  **Place** menu and then link it
* via **to**, you can add the end location of the move event. For more
  information check **from** (above in this tutorial)
* if an **artifact** was moved by the event, e.g. a letter that was sent, you
  can choose the artifact from a list of already entered artifacts. If the
  artifact is not entered into the database yet, use **Artifact** in the
  menu to create an entry and link it here
* if a **person** was move by the event, choose the person from a list
  of already entered actors. If the actor is not entered into the database
  already, use the **Actor** tab in the menu to create an entry and link it
  here. **Please note**, only people who did not participate in a move event of
  their own free will should be linked here. Think of an exchange or transfer
  of prisoners, the expulsion of individuals, or relic translations and
  the transport of dead people. Travel does not fall into this category. The
  participants of a journey or another (voluntarily) undertaken move event are
  linked in a different way. For more information on this, see the tutorial on
  :doc:`journey`. **Please also note** that only individuals can be
  linked here, not groups. A move of a group cannot be mapped via CIDOC CRM
  at the moment and is therefore not possible here.
* it is possible to link the move event by using external references (find
  more information :doc:`here</entity/reference_system>`)
* enter a start and end **date** of the move event
* additionally you can enter a **description** of the event as free text

By clicking the **Insert** or **Insert and continue** button you can save
the entered data.
After saving the information, you can link sources, actors (for
participants of a **voluntary** move event!), references, files and notes
via the respective buttons on the landing page of your new entry.

For more information on move events including an artifact, please see the
example on :doc:`letters`. On how to enter a journey, please refer
to the :doc:`journey` tutorial.
