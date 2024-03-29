Reference
=========

.. toctree::

CIDOC documentation: :cidoc_entity:`E31 Document<e31-document>`

* **Bibliography** - e.g. book, inbook or article
* **Edition** - e.g. charter editions or chronicle edition
* **External Reference** - e.g. URLs of websites or DOIs

.. include:: navigation.rst

Form fields
-----------
* :doc:`/ui/name` - or an **URL** field in case of an external references
* :doc:`type`
* :doc:`/ui/description`

Citation example
----------------
At :doc:`/admin/content` an example citation can be defined which will be displayed under the
form at insert/update of an edition or a bibliography.

Can be linked via tabs to
-------------------------
* :doc:`source`
* :doc:`event`
* :doc:`actor`
* :doc:`place`
* :doc:`file`

When linking a **Bibliography** or **Edition** a **page** can be defined.

When linking an **External Reference** a **link text** can be specified which be shown on the
info page of referenced entities. In case  no link text was provided the URL will be shown instead.
