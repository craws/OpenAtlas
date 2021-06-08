Archaeological data
===================

.. toctree::

The steps mentioned below describe how to enter archaeological data into OpenAtlas.
The following elements are involved in the procedure:

* :doc:`/entity/place`: the archaeological site itself (Level 1)
* :doc:`/entity/feature`: a subunit of the place, e.g. graves, buildings, and pits. A place can consist of multiple subunits (Level 2)
* :doc:`/entity/stratigraphic_unit`: a subunit of the feature, e.g. burial. A feature can consist of multiple subunits (Level 3)
* Find (see :doc:`/entity/artifact`): an archaeological find, e.g. coin or knife (Level 4)
* :doc:`/entity/human_remains`: subunits of a burial, e.g. bones and teeth that carry anthropological information (Level 4)
* :doc:`/entity/type`: used for classification, can be extended by users
* :doc:`/entity/reference`: citation, e.g. book or article written a bout the site or any of the subunits
* :doc:`/entity/file`: an image or other file concerning the site or any of its subunits

.. image:: /entity/sub_unit.jpg

Adding a new place
------------------
In order to store new archaeological information in the database, the first necessary step is to create a new
:doc:`/entity/place`. In the OpenAtlas database a place is a physical thing that has a certain position and or extend in
space that can be connected to various other information (temporal, spatial, events, sources etc.).

* Click on :doc:`/entity/place` in the :doc:`/ui/menu` and create a new entry by using the **+ Place** button
* State the site's name
* Select an appropriate :doc:`/entity/type` from the list, e.g. Burial Site or Settlement
* Use the magnifier button on the map to add the site to the map as well as a GeoNames reference if desired
* Add further information, e.g. evidence, an alias, a date or a description if available
* Press **Insert** to save the entry
* To add a citation click the **Reference tab**
* If you want to add an image e.g. a plot or photo of the site use the **File tab**

Adding a feature to the site
----------------------------
Next, a :doc:`/entity/feature` connected to the :doc:`/entity/place` will be created. This feature can be a grave of a grave yard, a building of a settlement, etc.

* Click on the **Feature Tab** and create a new entry by using the **+ Feature** button
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list
* Add further information, e.g. dimensions or a description
* Press **Insert and add stratigraphic unit** to save the entry and go on with the workflow

If you want to link the created feature to a different citation or add an image you can use **Insert** and add those
information or go back later and do it then. In this case you would have to click the **Stratigraphic unit Tab** and the
**+ Stratigraphic unit** button to go on with the workflow.

Adding a stratigraphic unit to the feature
------------------------------------------
Every :doc:`/entity/feature` consists of one or more :doc:`/entity/stratigraphic_unit`. For a grave this would be
the burial or a burial and the backfilling.

* By clicking Insert and add stratigraphic unit in the before mentioned step, you can directly enter a stratigraphic unit connected to the created feature
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, e.g. burial or interface
* Add additional information on the stratigraphic unit if available
* Press **Insert and add find** or **Insert an add human remains** to go on with the workflow

Adding a find to the stratigraphic unit
---------------------------------------
The following steps add a find (see :doc:`/entity/artifact`) to the before created :doc:`/entity/stratigraphic_unit`. You can now add grave goods to a burial or
finds to a certain layer of the feature.

* By clicking Insert and add find in the before mentioned step, you can directly connect a find to the newly created stratigraphic unit
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, e.g. pottery or wire ring
* Add additional information if available
* Press **Insert** to save the entry
* Add a file if desired by using the **File** tab

You can also enter a find by going to the stratigraphic unit you want to link the find to. Click the **Find tab** and
**+ Find** afterwards.

Adding human remains to the stratigraphic unit
----------------------------------------------
Anthropological data can be entered into OpenAtlas by adding :doc:`/entity/human_remains`. You can do so by connecting a
certain bone to a :doc:`/entity/stratigraphic_unit` and add all the relevant information, e.g. pathological changes,
measurements, discoloration, or additional information. Please note that information on the biological sex, gender,
and age of an individual can be entered in the stratigraphic unit entry mask.

* By clicking Insert and add human remains in the before mentioned creation of a stratigraphic unit, you can directly connect human remains to it
* Choose a descriptive name
* Select an appropriate :doc:`/entity/type` from the list, e.g. femur or canine
* Add additional information if available
* Press **Insert** to save the entry
* Add a file if desired by using the **File** tab

You can also enter :doc:`/entity/human_remains` by going to the stratigraphic unit you want to link the information to. Click the
**Human remains tab** and **+ Human remains button** afterwards.