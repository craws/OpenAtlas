ARCHE
=====

.. toctree::

**Be aware** this feature is experimental and only usable for a specific dataset.

`ARCHE <https://arche.acdh.oeaw.ac.at/>`_ (A Resource Centre for the HumanitiEs) is a service aimed at offering stable and persistent hosting as well as dissemination of digital research data and resources.

In order to import data from ARCHE to OpenAtlas changes to instance/production.py are needed (ask your administrator for further details):

.. code-block::
   :caption: instance/production.py

   ARCHE = {
    'id': 0,                                                  # Top collection ID (acdh:TopCollection)
    'collection_ids': [0],                                    # Sub collections ID containing metadata.json files (acdh:Collection)
    'base_url': 'https://arche-curation.acdh-dev.oeaw.ac.at/',      # Base URL to get data from
    'thumbnail_url': 'https://arche-thumbnails.acdh.oeaw.ac.at/'    # URL of ARCHE thumbnail service
    }}

The ARCHE button is displayed in the Admin/Data menu only if above data is provided.
Click on the ARCHE button to get to the overview section.

Overview
--------

Data provided in the production.py is displayed. If user belongs to the **manager** user group, a button called **Fetch** is displayed. Click **Fetch** to fetch data from ARCHE.


Fetch
-----

Data fetched from ARCHE are listed in a :doc:`/ui/table`.
Only data (based on the :doc:`/entity/artifact`), which was not imported is shown.

Click on **Import ARCHE data** to import data.

Data used from ARCHE
--------------------

All data is gathered from [IMAGE_NAME]_metadata.json:

.. code-block::

    'image_id': image_id (ARCHE)
    'image_link': image_url (ARCHE)
    'image_link_thumbnail': thumbnail_url (ARCHE)
    'creator': EXIF:Artist
    'latitude': EXIF:GPSLatitude
    'longitude': EXIF:GPSLongitude
    'description': XMP:Description
    'name': IPTC:ObjectName
    'license': EXIF:Copyright
    'date': EXIF:CreateDate

Automatically created entities
------------------------------

All necessary new types, persons etc. will be automatically created during the import process.

:doc:`/entity/type`
^^^^^^^^^^^^^^^^^^^

* Custom hierarchy **Relevance** for Persons (E21)
* **Involvement** for creation and production event
* Additional **License** types -> EXIF:Copyright

:doc:`/entity/reference_system`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New :doc:`/entity/reference_system` named **ARCHE** is created with data provided by instance/production.py

:doc:`/entity/index`
^^^^^^^^^^^^^^^^^^^^

* :doc:`/entity/artifact` (E22): Graffito, name (IPTC:ObjectName), description (XMP:Description), linked (P67) to **ARCHE** :doc:`/entity/reference_system` (E32)
* Location (E53): Location of Graffito, linked (P53) to :doc:`/entity/artifact` (EXIF:GPSLatitude, EXIF:GPSLongitude)
* Production :doc:`/entity/event` (E12): Date (EXIF:CreateDate) linked (P11) to :doc:`/entity/actor` and linked (P108) to :doc:`/entity/artifact`
* Creation :doc:`/entity/event` (E65): Date (EXIF:CreateDate) linked (P14) to :doc:`/entity/actor` **Person** (EXIF:Artist) and linked (P92) to :doc:`/entity/file`
* :doc:`/entity/file` (E31): linked (P2) to **License** :doc:`/entity/type` (EXIF:Copyright), linked (P67) to :doc:`/entity/artifact`
* :doc:`/entity/actor` **Person** (E21): name (EXIF:Artist, etc.), linked (P2) to :doc:`/entity/type` **Relevance**

.. image:: ARCHE_import_OpenAtlas.jpg
    :width: 400px