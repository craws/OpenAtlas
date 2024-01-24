Image annotation
================

.. toctree::

The image annotation feature allows for marking areas on an image and adding
a text and/or link it to an entity. E.g. a person on a group picture or an
artifact at an excavation site image.

Prerequisite for image annotation is an enabled and configured
:doc:`/admin/iiif` server.

Usage
-----

At a :doc:`/entity/file` detail view click on the **Enable IIIF view** button
below the image if it wasn't converted already.

Once the image was converted you can click on the **Annotate** link below the
image and the annotation view will open in a new tab.

In the image annotation view you can see the image in an IIIF viewer and a form
for new annotations and a list of already entered annotations with links to
edit or delete them.

**Form fields**

* **IIIF image view** - here you can use the rectangle draw button on the left
  side to mark an area.
* **Annotation** - you can enter a description here
* **Entity** - you can link an entity here

Be aware that the **Entity** selection only offers entities that are already
linked to the file. This is to guarantee that the entity is also linked via
the model (which the image annotation is not part of).
