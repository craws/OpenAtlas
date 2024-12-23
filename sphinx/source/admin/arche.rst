ARCHE
=====

.. toctree::

`ARCHE <https://arche.acdh.oeaw.ac.at/>`_ (A Resource Centre for the
HumanitiEs) is a service aimed at offering stable and persistent hosting as
well as dissemination of digital research data and resources.

In order to import data from ARCHE to OpenAtlas, changes to
instance/production.py are needed (ask your OpenAtlas administrator for
further details):

.. code-block::
   :caption: instance/production.py

   ARCHE = {
    'id': 0,    # Top collection of the project (acdh:TopCollection)
    'url': 'https://arche-curation.acdh-dev.oeaw.ac.at/',  # Base URL to get
    data from
    }}

The **ARCHE** button is displayed in the Admin/Data menu only if the
changes mentioned above are made.
Click on the **ARCHE** button to get to the overview section.

Overview
--------

Data provided in the production.py is displayed. If user is part of
the **manager** user group, the **Fetch** button is displayed. Click
**Fetch** to fetch data from ARCHE.


Fetch
-----

Data fetched from ARCHE are listed in a :doc:`/ui/table`.
Only data (based on the :doc:`/entity/artifact`) that was not imported is
shown.

Click on **Import ARCHE data** to import data.

Data from ARCHE
---------------

All metadata is gathered from the EXIF endpoint of the first image in the
"2_JPGs" collection. Additionally, the corresponding .png from
"4_Orthophotos" is taken as reference file.

Automatically created entities
------------------------------

All necessary new types, persons etc. will be automatically created or added
during the import process.

.. image:: ARCHE_import_OpenAtlas.jpg
    :width: 700px

:doc:`/entity/type`
^^^^^^^^^^^^^^^^^^^
- Custom hierarchy **Relevance** for :doc:`/entity/actor` (:cidoc_entity:`E21 Person<e21-person>`)
- **Involvement** for :cidoc_entity:`E65 Creation<e65-creation>` and p:cidoc_entity:`E12 Production<e12-production>` event
- Additional **License** :doc:`/entity/type` -> EXIF:Copyright

:doc:`/entity/reference_system`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New :doc:`/entity/reference_system` named **ARCHE** is created with data
provided by instance/production.py

:doc:`/entity/index`
^^^^^^^^^^^^^^^^^^^^
- :doc:`/entity/artifact` (:cidoc_entity:`E22 Human-Made Object<e22-human-made-object>`): Graffito, name (IPTC:ObjectName), description (XMP:Description), linked (:cidoc_property:`P67<p67-refers-to>`) to **ARCHE** :doc:`/entity/reference_system` (:cidoc_entity:`E32<e32-Authority-Document>`)
- :cidoc_entity:`E53 Place<e53-place>`: Location of Graffito, linked (:cidoc_property:`P53<p53-has-former-or-current-location>`) to :doc:`/entity/artifact` (EXIF:GPSLatitude, EXIF:GPSLongitude)
- :doc:`/entity/event` (:cidoc_entity:`E12 Production<e12-production>`): Date (EXIF:CreateDate) linked (:cidoc_property:`P11<p11-had-participant>`) to :doc:`/entity/actor` (:cidoc_entity:`E21 Person<e21-person>`) and linked (:cidoc_property:`P108<p108-has-produced>`) to :doc:`/entity/artifact`
- :doc:`/entity/event` (:cidoc_entity:`E65 Creation<e65-creation>`): Date (EXIF:CreateDate) linked (:cidoc_property:`P14<p14-carried-out-by>`) to :doc:`/entity/actor` (:cidoc_entity:`E21 Person<e21-person>`) and linked (:cidoc_property:`P92<p92-brought-into-existence>`) to :doc:`/entity/file`
- :doc:`/entity/file` (:cidoc_entity:`E31 Document<e31-document>`): linked (:cidoc_property:`P2<p2-has-type>`) to **License** :doc:`/entity/type` (EXIF:Copyright), linked (:cidoc_property:`P67<p67-refers-to>`) to :doc:`/entity/artifact`
- :doc:`/entity/actor` (:cidoc_entity:`E21 Person<e21-person>`): name (EXIF:Artist, etc.), linked (:cidoc_property:`P2<p2-has-type>`) to :doc:`/entity/type` **Relevance**

