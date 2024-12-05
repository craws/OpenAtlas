OpenAtlas classes
=================

.. toctree::

These special classes are used within the software to further refine
`CIDOC CRM <https://www.cidoc-crm.org/>`_ classes for the user interface.
While OpenAtlas uses the CIDOC CRM within the application, a finer grained
model is needed to deal with contextual differences in the user
interface. Therefore,
:cidoc_entity:`E33 - Lingustic Object<e33-linguistic-object>` is used as class
for sources as well as source translations with different user interface forms.
An overview of the internal mapping and CIDOC CRM classes can be found
`here <https://github.com/craws/OpenAtlas/tree/main/install/crm>`_.

All of these so called OpenAtlas classes can be mapped directly to the
corresponding CIDOC CRM class. For all available classes and properties of
CIDOC CRM (version 7.1.2) see
`the CIDOC CRM documentation <https://cidoc-crm.org/Version/version-7.1.2>`_.

Example:
:cidoc_entity:`E18 - Physical Thing<e18-physical-thing>` "comprises all
persistent physical items with a relatively stable form, human-made or
natural" (for more information see
:cidoc_entity:`CIDOC CRM<e18-physical-thing>` documentation).
In OpenAtlas E18 is used to represent :doc:`place </entity/place>`,
:doc:`stratigraphic unit </entity/stratigraphic_unit>`, and
:doc:`feature </entity/feature>`, which are all considered physical things
according to `CIDOC CRM <https://www.cidoc-crm.org/>`_.
To differentiate between those different entities, the corresponding OpenAtlas
classes were created. While :doc:`place </entity/place>`,
:doc:`stratigraphic unit </entity/stratigraphic_unit>`, and
:doc:`feature </entity/feature>` are all considered E18 and mapped to this
CIDOC CRM class in the background of the application, the user interface
displays the OpenAtlas class name and a corresponding, entity-specific form
for user's convenience and to avoid confusion.

The same is true for bibliography, edition, external reference and file,
which are all considered to be :cidoc_entity:`E31 - Documents<E31-Document>` in
CIDOC CRM or the OpenAtlas classes source and source translation which
correspond to the CIDOC class
:cidoc_entity:`E33 - Linguistic object<E33-Linguistic-Object>`.

An overview of all OpenAtlas classes used and how they correspond to CIDOC CRM
classes can be found at the
`demo <https://demo.openatlas.eu/overview/model/openatlas_class_index>`_.
