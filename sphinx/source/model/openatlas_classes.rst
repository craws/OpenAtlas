OpenAtlas classes
=================

.. toctree::

These special classes are used within the software to further refine
`CIDOC CRM <https://www.cidoc-crm.org/>`_ classes for the user interface.

All OpenAtlas classes can be mapped directly to the corresponding CIDOC CRM
classes. For all available classes and properties of CIDOC CRM (version 7.1.1)
`see here <https://cidoc-crm.org/Version/version-7.1.1>`_.

Example:
The CIDOC class :cidoc_entity:`E18 - Physical Thing<e18-physical-thing>`
"comprises all persistent physical items with a relatively stable form,
human-made or natural" (for more information see
:cidoc_entity:`CIDOC CRM<e18-physical-thing>` documentation).
In OpenAtlas E18 is used to represent :doc:`place </entity/place>`,
:doc:`stratigraphic unit </entity/stratigraphic_unit>`, and
:doc:`feature </entity/feature>`, which are all physical things according to
`CIDOC CRM <https://www.cidoc-crm.org/>`_.
To differentiate between those different entities, the corresponding OpenAtlas
classes were created. While :doc:`place </entity/place>`,
:doc:`stratigraphic unit </entity/stratigraphic_unit>`, and
:doc:`feature </entity/feature>` are all considered E18 and mapped to this
CIDOC CRM class in the background of the application, the user interface
displays the OpenAtlas class name for user's convenience and to avoid
confusion.

The same is true for bibliography, edition, external reference and file,
which are all considered to be :cidoc_entity:`E31 - Documents<E31-Document>` in
CIDOC CRM or the OpenAtlas classes source and source translation which
correspond to the CIDOC class
:cidoc_entity:`E33 - Linguistic object<E33-Linguistic-Object>`.

An overview of all OpenAtlas classes used and how they correspond to CIDOC CRM
classes can be found
`here <https://demo.openatlas.eu/overview/model/openatlas_class_index>`_.
