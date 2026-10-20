Overview
========

Welcome to the OpenAtlas API documentation. OpenAtlas provides programmatic
access to archaeological, historical, and geospatial data stored in an
OpenAtlas instance.

Whether you want to build a public presentation website, connect analytical
tools, perform research queries, or integrate with Linked Open Data (LOD)
networks, the OpenAtlas API provides human- and machine-readable data across
multiple standard formats.

Overview & Philosophy
---------------------
The OpenAtlas API combines two complementary paradigms:

1. **RESTful Web Services**: Easy-to-use, predictable URLs delivering JSON
   and GeoJSON for developers, web applications, and desktop GIS tools.
2. **Linked Open Data (LOD)**: Rich, graph-based RDF representations using
   the `CIDOC Conceptual Reference Model (CIDOC CRM) <https://www.cidoc-crm.org/>`_,
   the international `Linked Art <https://linked.art/>`_ profile, and W3C
   `SKOS <https://www.w3.org/2004/02/skos/>`_ for controlled vocabularies.

Versioning
----------
OpenAtlas follows sequenced semantic versioning. The API currently supports
two major generations:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Version
     - Status
     - Description
   * - **0.4**
     - **Stable**
     - The proven RESTful API (Flask-RESTful). Provides endpoints for
       entities, types, GeoJSON, and LPF. Documented in :doc:`/api/api_04`.
   * - **1.0**
     - **Beta**
     - The next-generation API based on OpenAPI 3.1 and Pydantic. Features
       native Linked Open Data graphs, Linked Art profiles, SKOS thesauri,
       IIIF Presentation API v2/v3, and high-performance streaming dumps.

Interactive Documentation UIs
-----------------------------
For API v1, OpenAtlas provides three interactive browser interfaces that let
you explore, inspect, and test all 31 endpoints directly without writing a
single line of code:

.. grid:: 1 3 3 3
   :gutter: 2

   .. grid-item-card:: Swagger UI
      :link: /api/1/docs/swagger
      :link-type: url

      Interactive testing sandbox. Try out endpoints, enter parameters,
      authorize with a token, and execute live requests.

   .. grid-item-card:: ReDoc
      :link: /api/1/docs/redoc
      :link-type: url

      Clean, publication-ready three-panel documentation focusing on
      schemas, types, and response models.

   .. grid-item-card:: Scalar
      :link: /api/1/docs/scalar
      :link-type: url

      Modern, responsive API client interface with instant code snippets
      in various programming languages.

Machine-Readable OpenAPI Specification
--------------------------------------
The complete OpenAPI 3.1 specification for API v1 is dynamically generated at:

* **URL**: ``/api/1/docs/openapi.json`` (or ``https://<your-instance>/api/1/docs/openapi.json``)

Guide Contents
--------------
* :doc:`getting_started` - Access modes, JWT Bearer tokens, and first requests.
* :doc:`lod` - Semantic Web concepts, CIDOC CRM, CRMarchaeo, Linked Art, and SKOS.
* :doc:`cookbook` - Step-by-step practical recipes for non-programmers (QGIS, OpenRefine, dates, IIIF, Python/R).
* :doc:`reference` - Complete index of all 36 endpoints, parameters, and error codes.
* :doc:`api_04` - Documentation for the current stable API v0.4.
