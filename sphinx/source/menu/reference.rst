Reference
=========

.. toctree::

Available reference classes based on `CIDOC CRM <http://www.cidoc-crm.org/>`_:

* **Bibliography** - e.g. book, inbook or article
* **Edition** - e.g. charter editions or chronicle edition
* **External Reference** - e.g. URLs of websites or DOIs

.. include:: navigation.rst

Form fields
-----------
* :doc:`/form/name` - or an **URL** field in case of an external references
* :doc:`/form/type`
* :doc:`/form/description`

Can be linked via tabs to
-------------------------
* :doc:`source`
* :doc:`event`
* :doc:`actor`
* :doc:`place`
* :doc:`/tools/file`

When linking a **Bibliography** or **Edition** a **page** can be defined.

When linking an **External Reference** a **link text** can be specified which be shown on the
info page of referenced entities. In case  no link text was provided the URL will be shown instead.
