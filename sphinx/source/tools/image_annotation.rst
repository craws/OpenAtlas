Image annotation
================

.. toctree::

The image annotation feature allows for marking areas on an image and adding
a text and/or link to an entity. In that way a person in a group picture
or an artifact on an excavation photo can be linked to the entity in OpenAtlas.

Prerequisite for image annotation is an enabled and configured
:doc:`/admin/iiif` server.

Usage
-----

In a :doc:`/entity/file`'s detail view, click the **Enable IIIF view** button
below the image, if it is not converted already.
Once the image is converted click the **Annotate** link below the
image and the annotation view will open in a new tab.

In the image annotation view you can see the image in an IIIF viewer as
well as a form for new annotations including a list of already saved
annotations. Links to edit or delete previous annotations are als porvided.

**Form fields**

* **IIIF image view** - click the button on the left to draw a rectangle
  to mark the desired area.
* **Annotation** - enter a description
* **Entity** - link to an entity

Be aware that the **Entity** selection only offers entities that are already
linked to the file. This guarantees that each selectable entity is also
linked to the file via the model. Immage annotation does not create new
model links in the background!
