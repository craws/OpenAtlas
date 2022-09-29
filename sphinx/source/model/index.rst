Model
=====

.. toctree::
   :maxdepth: 1

   cidoc_crm
   openatlas_shortcuts
   references
   link_checker

**Data Model**

While the model uses `CIDOC CRM <https://www.cidoc-crm.org/>`_ as
ontology, it can be used without prior knowledge of data models, ontologies,
etc. The software automatically maps information to the model. As the
definitions of the CIDOC Conceptual Refernece Model was imported into the
system, its
`classes <https://demo.openatlas.eu/overview/model/cidoc_class_index>`_
and `properties <https://demo.openatlas.eu/overview/model/property>`_ can be
browsed directly in OpenAtlas (see also :doc:`here<cidoc_crm>`).
Furthermore, it is possible to verify link-conformity between entities via the
`link-checker <https://demo.openatlas.eu/overview/model>`_ (for more
information click here :doc:`here<link_checker>`).

During the development much emphasis was put on the fact that users do not have
to concern themselves with the model or its ontology. Nevertheless, it is
possible to display the CIDOC classes used in the user interface and thus gain
insight into how the data is mapped.

Pressing the **Model** button on the start page leads to a
graphical presentation of the model (see below), a
:doc:`link checking tool<link_checker>` and links to the classes and
properties.

.. image:: openatlas_schema.png
.. image:: openatlas_schema2.png

Furthermore, it is possible to active **Show CIDOC classes** in the user
interface. This will displays the CIDOC class of an entity in the detail view
of a data base entry.
To do so click the gear symbol and choose :doc:`profile</tools/profile>`. Go
to **Display**, press the **Edit** button and choose **Show CIDOC classes**.

While we try to only use CIDOC CRM classes and properties where possible
(instead of introducing own classes or using extensions), some shortcuts are
used to increase performance and to keep the code base maintainable.
For more information, see :doc:`OpenAtlas shortcuts<openatlas_shortcuts>`.

While OpenAtlas uses the CIDOC CRM within the application, a finer grained
model is needed to deal with any contextual differences needed for the user
interface. Therefore, e.g.
:cidoc_entity:`E33 - Lingustic Object<e33-linguistic-object>` can be a source
or a source translation with different forms in different context.
An overview of internal mapping and CIDOC CRM classes can be found here
`here <https://github.com/craws/OpenAtlas/tree/main/install/crm>`_
