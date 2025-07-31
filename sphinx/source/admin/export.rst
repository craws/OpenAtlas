Export
======

.. toctree::

Available for admins and managers

Export SQL
----------

* Be aware, especially when sharing, that **user data**, e.g. email addresses,
  are included in the database backups
* SQL dumps are saved in the **files/export** folder
* A warning will appear if the directory isn't writable
* File names begin with date and time e.g. 2018-08-23_1533_export.sql
* Existing backups are shown in a list and can be downloaded or deleted

Export SQL
**********
A SQL dump will be created with **pg_dump** in a plain text format. The
resulting file can be used to fill an existing empty database, such as

.. code-block::

   psql openatlas < export.sql

Export database dump
********************

A SQL dump will be created with **pg_dump** in a custom archiving format (-Fc).
In this format **pg_restore** can be used to restore the database regardless
of used operating system and if line breaks are used or not

.. code-block::

   pg_restore -d openatlas -1 export.dump


Export CSV
----------
When the **Export CSV** button is clicked, a **ZIP** file containing several
**CSV** files is downloaded. The ZIP file contains:

* All entities divided by their OpenAtlas class
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The **ZIP** file's name starts with the current date and time, for
example 2022-10-04_1610-export.zip. This process can take some time.

Export JSON
-----------
When the **Export JSON** button is clicked, a **JSON** file is downloaded.
This file contains the following keys:

* Entities
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The file name starts with the current date and time, for example
2022-10-04_1610-export.json. This process can take some time.

Export XML
----------
When the **Export XML** button is clicked, an **XML** file is
downloaded. This file contains the following tags:

* Entities
* Links
* Properties
* Hierarchy of properties
* Classes
* Hierarchy of classes
* Geometries

The file name starts with the current date and time, for example
2022-10-04_1610-export.xml. This process can take some time.

Export ARCHE
------------

A dedicated export is available to generate data suitable for ingestion into `ARCHE <https://arche.acdh.oeaw.ac.at/>`_, the ACDH repository system. This feature is intended for administrative use only.

* Only available for **admin users**
* Generates a **ZIP** archive ready to be transfered to ARCHE
* Output includes metadata, files, RDF and SQL dumps, and debug information in ARCHE-compatible structure
* The process may take **significant time** and consume **large disk space**
* ZIP file is saved in the ``files/export`` directory

.. note::

   This export is **not** listed among the standard user exports and is only available to administrators due to performance and data sensitivity concerns.

Configuration
*************

To make use of the ARCHE export functionality, specific metadata must be provided in the ``production.py`` settings file using the ``ARCHE_METADATA`` dictionary.

Here is an example configuration:

.. code-block:: python

    ARCHE_METADATA = {
        'topCollection': 'OpenAtlas collection',
        'language': 'en',
        'depositor': [
            'Jane Doe',
            'https://orcid.org/0000-0000-0000-0000',
            'https://isni.org/isni/0000000121032683',
            'https://d-nb.info/gnd/123456789'
        ],
        'acceptedDate': "2024-01-01",
        'hasMetadataCreator': [
            'https://orcid.org/0000-0000-0000-1111',
            'https://orcid.org/0000-0000-0000-0000',
            'https://isni.org/isni/0000000121032683',
            'Jane Doe'
        ],
        'curator': [
            'https://orcid.org/0000-0000-0000-1111',
            'https://d-nb.info/gnd/123456789',
            'Jane Doe'
        ],
        'principalInvestigator': [
            'Researcher A',
            'Researcher B',
            'https://orcid.org/0000-0000-0000-1111'
        ],
        'relatedDiscipline': [
            'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003',
            'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/602001'
        ],
        'typeIds': [
            1234, 4567, 87656, 3252, 234
        ],
        'exclude_reference_systems': [
            'Internal catalogue', 'Inventory numbers'
        ]
    }

**Description of fields:**

.. note::

   For all fields that refer to people (e.g., ``depositor``, ``curator``, ``hasMetadataCreator``), you can use either a **persistent identifier** (preferably `ORCID <https://orcid.org/>`_, but also `GND <https://www.dnb.de/EN/gnd>`_ or `ISNI <https://isni.org/>`_) or a **plain name**. Use persistent identifiers whenever possible for better interoperability.

* ``topCollection``: ARCHE top-level collection identifier
* ``language``: Language code of the metadata (e.g. ``'en'``)
* ``depositor``: List of persons responsible for the deposit
* ``acceptedDate``: ISO date string of when the data was accepted for deposit
* ``hasMetadataCreator``: List of metadata creators
* ``curator``: List of collection curators
* ``principalInvestigator``: List of principal investigators
* ``relatedDiscipline``: URLs to vocabularies defining the `related disciplines <https://vocabs.acdh.oeaw.ac.at/oefos/en/>`_
* ``typeIds`` *(optional)*: Restrict exported files to those linked with specific type IDs
* ``exclude_reference_systems`` *(optional)*: List of reference system labels to be excluded from the export

.. note::

   If ``typeIds`` or ``exclude_reference_systems`` are empty, all files and reference systems are considered.
