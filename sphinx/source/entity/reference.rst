Reference
=========

.. toctree::

CIDOC documentation: :cidoc_entity:`E31 Document<e31-document>`

* **Bibliography** - add book, inbook, or article
* **Edition** - e.g. charter editions or chronicle edition
* **External Reference** - such as URLs of websites or DOIs

.. include:: navigation.rst

Form fields
-----------
* :doc:`/ui/name` - or an **URL** field in case of an external references
* :doc:`type`
* :doc:`/ui/description`

Citation example
----------------
Via :doc:`/admin/content` an example citation can be defined which will be
displayed under the form during the insert/update of an edition or a
bibliography.

Can be linked via tabs to
-------------------------
* :doc:`source`
* :doc:`event`
* :doc:`actor`
* :doc:`place`
* :doc:`file`

While linking a **Bibliography** or **Edition** a **page** can be defined.

While linking an **External Reference** a **link text** can be specified which
be shown on the info page of referenced entities. In case no link text is
provided the URL will be shown instead.
