Export
======

.. toctree::

Available for admins and managers

Export SQL
----------

* Be aware, especially when sharing, that **user data**, e.g. email addresses,
  are included in the database backups
* SQL dumps are saved in the **files/sql/export** folder
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


Export RDF/NT
-------------

* RDF/NT dumps are saved in the **files/rdf/export** folder
* A warning will appear if the directory isn't writable
* File names begin with date and time e.g. 2018-08-23_1533_export.nt
* Existing backups are shown in a list and can be downloaded or deleted
* Only N-Triples (NT) are available, because of its efficiency


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

A dedicated export is available to generate data suitable for ingestion into
`ARCHE <https://arche.acdh.oeaw.ac.at/>`_, the ACDH repository system.
This feature is intended for administrative use only.

See also:

* `ARCHE Deposition Process <https://arche.acdh.oeaw.ac.at/browser/deposition-process>`_
* `ARCHE Metadata Schema <https://acdh-oeaw.github.io/arche-schema/>`_

* Only available for **admin users**
* Generates a **ZIP** archive ready to be transferred to ARCHE
* Output includes metadata, files, RDF and SQL dumps, and debug information
  in an ARCHE-compatible structure
* The process may take **significant time** and consume **large disk space**
* The ZIP file is saved in the ``files/arche/export`` directory

.. note::

   This export is **not** listed among the standard user exports and is only
   available to administrators due to performance and data sensitivity concerns.

Tabs
****

* **Info**
  Displays the data entered in ``production.py``.
  Provides a button to check ARCHE files.
  Only files associated with ``caseStudyIds`` (if any are defined) and not
  matching ``excludeLicenseIds`` are checked.
  More information on the file checker can be found in
  :doc:`/admin/data_integrity_checks`.

* **Export**
  Shows the exported files.
  Allows administrators to start and manage the ARCHE export.

Configuration
*************

To make use of the ARCHE export functionality, specific metadata must be
provided in the ``production.py`` settings file using the
``ARCHE_METADATA`` dictionary.

Here is an example configuration:

.. code-block:: python

    ARCHE_METADATA = {
        'projectAcronym': 'oa_collection',
        'topCollection': 'OpenAtlas collection',
        'description': 'Collection description',
        'language': 'en',
        'depositor': [
            'Jane Doe',
            'https://orcid.org/0000-0000-0000-0000',
            'https://isni.org/isni/0000000121032683',
            'https://d-nb.info/gnd/123456789'
        ],
        'acceptedDate': "2024-01-01",
        'submissionDate': "2024-01-01",
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
        'editor': ['Jane Doe'],
        'contact': ['Jane Doe'],
        'owner': ['https://d-nb.info/gnd/123456789'],
        'rightsHolder': ['https://d-nb.info/gnd/123456789'],
        'licensor': ['https://d-nb.info/gnd/123456789'],
        'principalInvestigator': [
            'Researcher A',
            'Researcher B',
            'https://orcid.org/0000-0000-0000-1111'
        ],
        'relatedDiscipline': [
            'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003',
            'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/602001'
        ],
        'subject': ['Archaeology', 'Cultural Heritage'],
        'licenseSummary': 'CC BY 4.0',
        'datasetLicense': 'https://creativecommons.org/licenses/by/4.0/',
        'lifeCycleStatus':
            'https://vocabs.acdh.oeaw.ac.at/archelifecyclestatus/completed',
        'url': '',
        'caseStudyIds': [
            1234, 4567
        ],
        'excludeLicenseIds': [
            8901
        ],
        'excludeReferenceSystems': [
            'Internal catalogue', 'Inventory numbers'
        ]
    }

Description of fields
*********************

.. note::

   For all fields that refer to people (e.g., ``depositor``, ``curator``,
   ``hasMetadataCreator``), you can use either a **persistent identifier**
   (preferably `ORCID <https://orcid.org/>`_, but also
   `GND <https://www.dnb.de/EN/gnd>`_, `ISNI <https://isni.org/>`_,
   `VIAF <https://viaf.org/>`_, or `Wikidata <https://www.wikidata.org/>`_)
   or a **plain name**. Use persistent identifiers whenever possible for
   better interoperability.

* ``projectAcronym`` *(optional)*: Short lowercase project slug used for
  URIs, ZIP filename, ``<slug>_database.sql``, ``<slug>_rdf.ttl``, and
  ``metadata/<slug>_metadata.ttl`` (falls back to ``topCollection``)
* ``topCollection``: Human-readable title of the ARCHE top-level collection
* ``description`` *(optional)*: Description of the top-level collection
* ``language``: Language code or ACDH language URI (e.g. ``'en'``)
* ``depositor``: List of persons/organisations responsible for the deposit
* ``acceptedDate``: ISO date string of when the data was accepted for deposit
* ``submissionDate`` *(optional)*: ISO date string of submission
* ``hasMetadataCreator``: List of people responsible for the ARCHE metadata
* ``curator``: List of ARCHE curators
* ``editor`` *(optional)*: List of collection editors
* ``contact`` *(optional)*: List of contact persons or organisations
* ``owner`` *(optional)*: List of resource owners
* ``rightsHolder`` *(optional)*: Default rights holders for collections/dumps
* ``licensor`` *(optional)*: Default licensors for collections/dumps
* ``principalInvestigator``: List of principal investigators for this project
* ``relatedDiscipline``: URLs to vocabularies defining the
  `related disciplines <https://vocabs.acdh.oeaw.ac.at/oefos/en/>`_
* ``subject`` *(optional)*: List of subject keywords for the top collection
* ``licenseSummary`` *(optional)*: License summary for collections
* ``datasetLicense`` *(optional)*: License URI for SQL and RDF dump files
* ``lifeCycleStatus`` *(optional)*: ACDH life-cycle status URI
* ``url`` *(optional)*: External project URL for the top collection
* ``caseStudyIds`` *(optional)*: Restrict exported files to those linked
  with specific case study IDs. Non-case-study IDs are ignored and reported in
  ``debug/problematic_files.md``.
* ``excludeLicenseIds`` *(optional)*: List of license type IDs whose files
  should be excluded from the ARCHE export and ARCHE file checker.
* ``excludeReferenceSystems`` *(optional)*: List of reference system
  labels to be excluded from the export

.. note::

   If ``caseStudyIds``, ``excludeLicenseIds``, or ``excludeReferenceSystems``
   are empty, all files, licenses, and reference systems are considered.
