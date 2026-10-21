API v1 (Beta)
=============

This section provides a quick-reference index of all 36 endpoints available in
OpenAtlas API v1, organized by feature area.

.. tip::
   To test any endpoint interactively in your browser with real parameters, visit
   the :doc:`interactive Swagger UI </api/index>`.

Endpoint Summary Table
----------------------

System & Root Endpoints
^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/``
     - API root index with schema and documentation links.
   * - ``GET``
     - ``/api/1/system/info``
     - Frontend configuration (map settings, IIIF status, language).
   * - ``GET``
     - ``/api/1/system/count/entities``
     - Instance counts per class (optionally filtered by case study).
   * - ``GET``
     - ``/api/1/system/classes``
     - System classes, CIDOC mapping, groups, and UI icons.
   * - ``GET``
     - ``/api/1/system/crm-properties``
     - Active CIDOC CRM properties, domains, ranges, and i18n labels.

Project Metadata
^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/case-studies``
     - Hierarchical list of all project case studies.
   * - ``GET``
     - ``/api/1/case-studies/{id}``
     - Detail information for a single case study and sub-case studies.
   * - ``GET``
     - ``/api/1/agents``
     - List of registered rights holders, authors, and creators.
   * - ``GET``
     - ``/api/1/agents/{id}``
     - Detailed information for an agent or rights holder.

Controlled Vocabularies & SKOS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/vocabulary``
     - Flat list of all OpenAtlas types with counts and references.
   * - ``GET``
     - ``/api/1/vocabulary/{id}``
     - Single type item with parent/sub hierarchy and images.
   * - ``GET``
     - ``/api/1/vocabulary/{id}/skos``
     - W3C SKOS ConceptScheme hierarchy (content negotiated).
   * - ``GET``
     - ``/api/1/vocabulary/{id}/skos.{ext}``
     - SKOS export driven by format extension (``.ttl``, ``.xml``, ``.json``, ``.nt``).
   * - ``GET``
     - ``/api/1/vocabulary/tree``
     - Hierarchical tree organized by categories (standard, custom, place, etc.).
   * - ``GET``
     - ``/api/1/vocabulary/tree/{openatlas_class}``
     - Hierarchical tree filtered by an OpenAtlas system class.
   * - ``GET``
     - ``/api/1/vocabulary/standard/{openatlas_class}``
     - Standard types tree formatted for UI components and case study filters.

Linked Open Data (LOD)
^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/entity/{uuid}``
     - Single entity formatted as CIDOC CRM LOD graph (JSON-LD default).
   * - ``GET``
     - ``/api/1/entity/{uuid}.{ext}``
     - Single entity with explicit format extension (``.ttl``, ``.xml``, ``.json``, ``.nt``).
   * - ``GET``
     - ``/api/1/entities/{entity_class}``
     - Paginated collection (ActivityStreams ``OrderedCollectionPage``) with search and filters.
   * - ``GET``
     - ``/api/1/context.json``
     - Complete OpenAtlas JSON-LD 1.1 ``@context``.
   * - ``GET``
     - ``/api/1/ontology``
     - OpenAtlas Extension OWL Ontology graph (defining shortcuts).
   * - ``GET``
     - ``/api/1/ontology.{ext}``
     - OpenAtlas Extension OWL Ontology graph with explicit format extension.
   * - ``GET``
     - ``/api/1/export/dump``
     - Keyset-streaming full LOD export in N-Triples format (authenticated).

Strict Linked Art Profile
^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/linked-art/entity/{uuid}``
     - Single entity conforming to the international Linked Art JSON-LD schema.
   * - ``GET``
     - ``/api/1/linked-art/entity/{uuid}.{ext}``
     - Single Linked Art entity with explicit format extension.
   * - ``GET``
     - ``/api/1/linked-art/entities/{entity_class}``
     - Paginated collection conforming to the Linked Art profile.
   * - ``GET``
     - ``/api/1/linked-art/export/dump``
     - Keyset-streaming Linked Art dump in JSON Lines (``.jsonl``) or N-Triples (``.nt``).

Digital Assets & Files
^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/files/{id}/display``
     - Serves the original image file or redirects (302) to IIIF image URL.
   * - ``GET``
     - ``/api/1/files/{id}/thumbnail``
     - Serves the pre-scaled thumbnail image or redirects (302) to IIIF thumbnail.
   * - ``GET``
     - ``/api/1/files/public``
     - Paginated overview of all publicly shareable, licensed files.
   * - ``GET``
     - ``/api/1/files/entity/{id}``
     - Paginated overview of public files linked to a specific entity.

IIIF Presentation API
^^^^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Method
     - Endpoint
     - Description
   * - ``GET``
     - ``/api/1/iiif/{id}/manifest/{version}``
     - IIIF Manifest (version ``2`` or ``3``).
   * - ``GET``
     - ``/api/1/iiif/{id}/canvas/{version}``
     - IIIF Canvas for a specific file and version.
   * - ``GET``
     - ``/api/1/iiif/{id}/image/{version}``
     - IIIF Image resource annotation.
   * - ``GET``
     - ``/api/1/iiif/{id}/annotation-list/{version}``
     - IIIF Annotation List (v2) or Annotation Page (v3).
   * - ``GET``
     - ``/api/1/iiif/{id}/annotation/{version}``
     - Specific IIIF spatial polygon or point annotation.

Query Parameters for Collections
--------------------------------
The collection endpoints (``/api/1/entities/{entity_class}`` and
``/api/1/linked-art/entities/{entity_class}``) support the following query
parameters:

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Default
     - Description
   * - ``page``
     - Integer
     - ``1``
     - Page number (1-indexed).
   * - ``limit``
     - Integer
     - ``50``
     - Number of items per page (maximum ``100``).
   * - ``search``
     - String
     - ``None``
     - Case-insensitive substring match on the entity label/name.
   * - ``startDate``
     - String
     - ``None``
     - Beginning of time span (e.g. ``1200``, ``1200-05``, ``1200-05-15``, or negative ``-400`` for BC).
   * - ``endDate``
     - String
     - ``None``
     - End of time span (e.g. ``1500``, ``1500-12-31``, or negative ``-100`` for BC).
   * - ``typeId``
     - Int / UUID
     - ``None``
     - Filter entities assigned to this type ID or type UUID.
   * - ``caseStudy``
     - Int / UUID
     - ``None``
     - Filter entities belonging to this case study.
   * - ``sortBy``
     - String
     - ``name``
     - Field to sort by: ``name``, ``startDate``, or ``endDate``.
   * - ``sort``
     - String
     - ``asc``
     - Sort order: ``asc`` (ascending) or ``desc`` (descending).

Standard Error Response Format
------------------------------
When an error occurs, the API returns a structured JSON payload with HTTP status
codes:

.. code-block:: json

   {
     "title": "Entity does not exist",
     "message": "The requested entity could not be found in the database.",
     "details": {
       "provided_id": "913322f4-a3cf-2e90-bfd1-cecc8e523b56",
       "hint": "Check if the UUID or ID is correct and the entity has not been deleted."
     },
     "status": 404,
     "url": "https://demo.openatlas.eu/api/1/linked-art/entity/913322f4-a3cf-2e90-bfd1-cecc8e523b56",
     "timestamp": "2026-10-16T10:00:00.000000Z"
   }

HTTP Status Codes
^^^^^^^^^^^^^^^^^
* ``200 OK``: Successful request.
* ``302 Found``: Temporary redirect (e.g. redirecting image requests to the high-performance IIIF server).
* ``400 Bad Request``: Invalid parameters or formatting errors.
* ``401 Unauthorized``: Authentication is required but was not provided.
* ``403 Forbidden``: The provided token does not have permission to access the resource.
* ``404 Not Found``: The requested entity, file, or endpoint does not exist.
* ``422 Unprocessable Entity``: Validation failure on query or path parameters (e.g. invalid date, negative limit, or NUL character in search).
* ``500 Internal Server Error``: Unexpected database or server error.
