Linked Open Data
================

This guide explains how OpenAtlas handles **Linked Open Data (LOD)** in Version 1,
which ontologies are employed, and how research data is structured and serialized.

Why Linked Open Data?
---------------------
Research data in archaeology, history, and the humanities is inherently
heterogeneous and interconnected. OpenAtlas uses Linked Open Data to fulfill the
`FAIR data principles <https://www.go-fair.org/fair-principles/>`_
(Findable, Accessible, Interoperable, Reusable).

By assigning persistent URIs and expressing relationships through formal
ontologies, data stored in OpenAtlas can be integrated with international
vocabularies (such as Getty AAT or Wikidata) and aggregated across disciplinary
boundaries.

Core Ontologies in OpenAtlas v1
-------------------------------
OpenAtlas maps database records to internationally recognized domain ontologies:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Prefix
     - Vocabulary / Ontology
     - Typical Usage
   * - ``crm``
     - `CIDOC CRM v7.1 <https://www.cidoc-crm.org/>`_
     - Core entities: Places (E53), Persons (E21), Groups (E74), Objects (E22), Activities (E7).
   * - ``archaeo``
     - `CRMarchaeo <https://www.cidoc-crm.org/crmarchaeo/>`_
     - Archaeological excavation data: Features (A6) and Stratigraphic Units (A8).
   * - ``geo``
     - `OGC GeoSPARQL <https://www.ogc.org/standard/geosparql/>`_
     - Geometries (``geo:Geometry``) and Well-Known Text (``geo:asWKT``).
   * - ``skos``
     - `W3C SKOS <https://www.w3.org/2004/02/skos/>`_
     - Controlled vocabularies, concept schemes, broader/narrower hierarchies.
   * - ``la``
     - `Linked Art <https://linked.art/>`_
     - Strict application profile of CIDOC CRM for cultural heritage data.

LOD Profiles in Version 1 (Beta)
--------------------------------
OpenAtlas v1 provides two Linked Open Data interfaces, along with W3C SKOS
thesaurus exports:

1. Strict Linked Art Profile (``/api/1/linked-art/...``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Endpoints**:
  * ``GET /api/1/linked-art/entity/{uuid}`` (or ``.../entity/{uuid}.{ext}``)
  * ``GET /api/1/linked-art/entities/{entity_class}``
* **Audience**: GLAM institutions (Galleries, Libraries, Archives, Museums),
  cultural heritage aggregators, and Linked Open Data consumers.
* **Status**: **Fully supported in v1 Beta** (Recommended).
* **Characteristics**: Adheres strictly to the `Linked Art profile <https://linked.art/>`_
  (JSON schemas with ``additionalProperties: false``). Responses strictly conform
  to Linked Art classes (such as ``HumanMadeObject``, ``Place``, ``Actor``, ``Activity``),
  providing full entity details, classified types, timespans, citations, and related links.

2. Controlled Vocabularies & SKOS (``/api/1/vocabulary/...``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Endpoints**:
  * ``GET /api/1/vocabulary/{id}/skos``
  * ``GET /api/1/vocabulary/{id}/skos.{ext}``
* **Audience**: Terminology managers, thesaurus hubs (e.g. SKOSMOS), and SPARQL endpoints.
* **Status**: **Fully supported in v1 Beta**.
* **Characteristics**: The root type is structured as a ``skos:ConceptScheme``,
  with all child nodes linked hierarchically via ``skos:broader`` and ``skos:narrower``.
  Supports standard formats (Turtle, RDF/XML, JSON-LD, N-Triples).

3. OpenAtlas Native CRM Graph (``/api/1/entity/...``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Endpoints**:
  * ``GET /api/1/entity/{uuid}`` (or ``.../entity/{uuid}.{ext}``)
  * ``GET /api/1/entities/{entity_class}``
* **Status**: **In Development / Experimental (Alpha Stub)**.
* **Characteristics**: Provides a preliminary, lightweight stub interface returning
  the entity URI, class type, and label. A comprehensive, deep CIDOC CRM graph
  serializer with formal property-chain shortcuts is currently under active
  development and will be introduced in an upcoming release.
* **Recommendation**: For production semantic integration in Version 1 Beta,
  please use the :ref:`Linked Art endpoints <linked-art-endpoints>`.

Format Selection & Content Negotiation
--------------------------------------
All Linked Open Data endpoints support HTTP Content Negotiation via the
``Accept`` header, as well as explicit URL extensions:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Format
     - HTTP Header (``Accept``)
     - URL Extension
   * - **JSON-LD** (Default)
     - ``application/ld+json``
     - ``.json``
   * - **Turtle**
     - ``text/turtle``
     - ``.ttl``
   * - **RDF/XML**
     - ``application/rdf+xml``
     - ``.xml``
   * - **N-Triples**
     - ``application/n-triples``
     - ``.nt``

*Example*: Fetching an entity in Turtle format using content negotiation:

.. code-block:: bash

   curl -H "Accept: text/turtle" https://demo.openatlas.eu/api/1/linked-art/entity/913322f4-a3cf-2e90-bfd1-cecc8e523b56

Or by appending ``.ttl`` directly to the URL:

.. code-block:: bash

   curl https://demo.openatlas.eu/api/1/linked-art/entity/913322f4-a3cf-2e90-bfd1-cecc8e523b56.ttl
