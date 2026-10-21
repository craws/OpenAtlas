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
   * - ``oa``
     - `OpenAtlas Extension <https://openatlas.eu/ontology/#>`_
     - High-performance shortcuts for frequent property chains.

The JSON-LD Context (``/api/1/context.json``)
---------------------------------------------
To make API responses clean and readable for human developers while preserving
full semantic compliance for machines, OpenAtlas uses a JSON-LD 1.1 ``@context``.

The context resolves intuitive attribute names to their canonical ontology URIs:

.. code-block:: json

   {
     "@context": {
       "@version": 1.1,
       "crm": "http://www.cidoc-crm.org/cidoc-crm/",
       "geo": "http://www.opengis.net/ont/geosparql#",
       "Place": "crm:E53_Place",
       "Person": "crm:E21_Person",
       "has_geometry": {"@id": "geo:hasGeometry", "@type": "@id"},
       "as_wkt": {"@id": "geo:asWKT", "@type": "geo:wktLiteral"},
       "took_place_at": {"@id": "crm:P7_took_place_at", "@type": "@id"},
       "carried_out_by": {"@id": "crm:P14_carried_out_by", "@type": "@id"}
     }
   }

The complete context definition can be retrieved at ``GET /api/1/context.json``.

OpenAtlas Extension Ontology & Shortcuts (``/api/1/ontology``)
--------------------------------------------------------------
In historical and archaeological research, certain relationship patterns recur
frequently. Constructing multi-node event chains for every simple link creates
unnecessary complexity and performance overhead.

To solve this, OpenAtlas defines formal **shortcuts** in its extension ontology.
Each shortcut is backed by an `OWL property chain axiom <https://www.w3.org/TR/owl2-primer/#Property_Chains>`_,
ensuring that standard RDF reasoners can automatically unfold the shortcut into
full CIDOC CRM paths:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - OpenAtlas Shortcut
     - Semantics
     - CIDOC CRM Path Resolution
   * - ``oa:has_relationship_to``
     - Actor relates to Actor (OA7)
     - ``E39 Actor`` -> ``P11i participated in`` -> ``E5 Event`` -> ``P11 had participant`` -> ``E39 Actor``
   * - ``oa:begins_in``
     - Item origin location (OA8)
     - ``E77 Item`` -> ``P92i brought into existence by`` -> ``E63 Beginning`` -> ``P7 took place at`` -> ``E53 Place``
   * - ``oa:ends_in``
     - Item demise location (OA9)
     - ``E77 Item`` -> ``P93i taken out of existence by`` -> ``E64 End of Existence`` -> ``P7 took place at`` -> ``E53 Place``

The machine-readable OWL ontology graph can be queried at ``GET /api/1/ontology``
in Turtle, RDF/XML, JSON-LD, or N-Triples.

Dual LOD Profiles: OpenAtlas Graph vs. Linked Art
-------------------------------------------------
OpenAtlas v1 offers two distinct Linked Open Data profiles, alongside W3C SKOS
thesaurus exports, to suit different integration requirements:

.. _openatlas-crm-endpoints:

1. Full OpenAtlas CRM Graph (``/api/1/entity/...``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Endpoints**:
  * ``GET /api/1/entity/{uuid}`` (or ``.../entity/{uuid}.{ext}``)
  * ``GET /api/1/entities/{entity_class}``
  * ``GET /api/1/export/dump``
* **Audience**: Semantic Web applications, archaeological graph databases, and RDF triple stores.
* **Status**: **Fully supported in v1 Beta**.
* **Characteristics**: Represents the complete richness of the OpenAtlas data
  model, combining CIDOC CRM, CRMarchaeo (e.g. ``A6_Feature``,
  ``A8_Stratigraphic_Unit``), GeoSPARQL (``geo:asWKT``), and formal OpenAtlas
  shortcuts (``oa:has_relationship_to``, ``oa:begins_in``, ``oa:ends_in``).

.. _linked-art-endpoints:

2. Strict Linked Art Profile (``/api/1/linked-art/...``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Endpoints**:
  * ``GET /api/1/linked-art/entity/{uuid}`` (or ``.../entity/{uuid}.{ext}``)
  * ``GET /api/1/linked-art/entities/{entity_class}``
  * ``GET /api/1/linked-art/export/dump``
* **Audience**: GLAM institutions (Galleries, Libraries, Archives, Museums),
  cultural heritage aggregators, and Linked Open Data consumers.
* **Status**: **Fully supported in v1 Beta**.
* **Characteristics**: Adheres strictly to the `Linked Art profile <https://linked.art/>`_
  (JSON schemas with ``additionalProperties: false``). Responses strictly conform
  to Linked Art classes (such as ``HumanMadeObject``, ``Place``, ``Actor``, ``Activity``),
  providing full entity details, classified types, timespans, citations, and related links.

3. Controlled Vocabularies & SKOS (``/api/1/vocabulary/...``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Endpoints**:
  * ``GET /api/1/vocabulary/{id}/skos``
  * ``GET /api/1/vocabulary/{id}/skos.{ext}``
* **Audience**: Terminology managers, thesaurus hubs (e.g. SKOSMOS), and SPARQL endpoints.
* **Status**: **Fully supported in v1 Beta**.
* **Characteristics**: The root type is structured as a ``skos:ConceptScheme``,
  with all child nodes linked hierarchically via ``skos:broader`` and ``skos:narrower``.
  Supports standard formats (Turtle, RDF/XML, JSON-LD, N-Triples).

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
