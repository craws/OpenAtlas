Cookbook
========

This cookbook is designed for researchers, archaeologists, historians, and
students who want to work with OpenAtlas data without having a background in
software development.

Each recipe provides step-by-step instructions, practical use cases, and
ready-to-use examples.

.. contents:: Table of Recipes
   :local:
   :depth: 1

---

Recipe 1: Exploring Data Without Code (Interactive Swagger UI)
--------------------------------------------------------------
You do not need terminal commands or programming languages to inspect data.
OpenAtlas includes an interactive web interface.

1. Open your browser and navigate to:
   ``https://<your-instance>/api/1/docs/swagger``
2. If your OpenAtlas instance is protected, click the green **Authorize** button
   at the top right, enter ``Bearer <your-token>``, and click **Authorize**.
3. Browse the categories (e.g. **lod**, **vocabulary**, **files**).
4. Click on any endpoint to expand it (for example, ``GET /api/1/entities/{entity_class}``).
5. Click **Try it out** on the right side.
6. Enter parameters in the form fields (e.g. ``entity_class: place``, ``limit: 10``).
7. Click **Execute**.
8. View the live response body, response headers, and the equivalent ``curl``
   command generated for you.

---

Recipe 2: Finding Places & Mapping Them in QGIS
-----------------------------------------------
OpenAtlas places include geographic coordinates formatted according to the OGC
GeoSPARQL standard as Well-Known Text (WKT).

Querying Places
^^^^^^^^^^^^^^^
To retrieve up to 100 places:

.. code-block:: text

   GET https://<your-instance>/api/1/entities/place?limit=100&page=1

In the response, each place contains an ``as_wkt`` geometry string, for example:

.. code-block:: json

   {
     "id": "https://demo.openatlas.eu/api/1/entity/913322f4-a3cf-2e90-bfd1-cecc8e523b56",
     "type": "Place",
     "label": "Vienna",
     "has_geometry": {
       "type": "Geometry",
       "as_wkt": "POINT(16.372477 48.208354)"
     }
   }

Importing into QGIS
^^^^^^^^^^^^^^^^^^^
1. **Option A (Python Console in QGIS)**:
   Open QGIS, press :kbd:`Ctrl+Alt+P` to open the Python console, and run:

   .. code-block:: python

      import json, requests
      from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsProject

      url = "https://demo.openatlas.eu/api/1/entities/place?limit=100"
      res = requests.get(url, headers={"Authorization": "Bearer YOUR_TOKEN"}).json()

      layer = QgsVectorLayer("Point?crs=epsg:4326&field=id:string&field=name:string", "OpenAtlas Places", "memory")
      pr = layer.dataProvider()

      for item in res.get("orderedItems", []):
          geom_wkt = item.get("has_geometry", {}).get("as_wkt")
          if geom_wkt:
              feat = QgsFeature()
              feat.setGeometry(QgsGeometry.fromWkt(geom_wkt))
              feat.setAttributes([str(item.get("id")), str(item.get("label"))])
              pr.addFeature(feat)

      layer.updateExtents()
      QgsProject.instance().addMapLayer(layer)

2. **Option B (CSV Export)**:
   Convert the JSON response to a CSV file containing an ``as_wkt`` column and a
   name column, then use QGIS **Layer** -> **Add Layer** -> **Add Delimited Text Layer**,
   selecting **Well Known Text (WKT)** geometry.

---

Recipe 3: Filtering Historical Dates (Including BC / BCE)
---------------------------------------------------------
Historical research requires temporal flexibility. OpenAtlas handles precise
dates, month ranges, whole years, and negative years for Before Christ (BC / BCE).

.. note::
   There is no year 0 in historical chronology. 1 BC is represented as ``-1``,
   followed immediately by 1 AD (``1``).

Practical Examples
^^^^^^^^^^^^^^^^^^
* **Events between 1200 and 1500 AD**:

  .. code-block:: text

     GET /api/1/entities/activity?startDate=1200&endDate=1500

* **Artifacts from the 5th Century BC (500 BC to 401 BC)**:

  .. code-block:: text

     GET /api/1/entities/artifact?startDate=-500&endDate=-401

* **Combining Search, Date Ranges, and Sorting**:

  .. code-block:: text

     GET /api/1/entities/place?search=Castle&startDate=1000&endDate=1300&sortBy=start_date&sort=asc

---

Recipe 4: Cleaning & Enriching Data with OpenRefine
---------------------------------------------------
`OpenRefine <https://openrefine.org/>`_ is a powerful, free tool for working
with messy data, cleaning it, and reconciling it with external authorities (like
Wikidata or GND).

Importing Directly from OpenAtlas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Launch OpenRefine in your browser.
2. Select **Create Project** -> **Web Addresses (URLs)**.
3. Enter your OpenAtlas API URL:
   ``https://<your-instance>/api/1/entities/place?limit=100&page=1``
   *(If protected, pass the token as a header or save the JSON file locally first).*
4. Click **Next**.
5. In the preview window, OpenRefine will detect the JSON structure. Click on the
   ``orderedItems`` array to select the entity records.
6. Click **Create Project**.
7. You now have a clean tabular spreadsheet of your OpenAtlas entities. You can
   use OpenRefine's **Reconcile** feature to match your place names against
   Wikidata, Getty AAT, or GeoNames.

---

Recipe 5: Exporting Typologies to SKOSMOS
-----------------------------------------
If your institution hosts a terminology hub or thesaurus viewer (such as
`SKOSMOS <https://skosmos.org/>`_), you can export any OpenAtlas type hierarchy
directly as a W3C SKOS ConceptScheme.

1. In OpenAtlas, note the numeric ID of the root type (e.g. ``42``).
2. Download the SKOS Turtle export via:

   .. code-block:: bash

      curl "https://demo.openatlas.eu/api/1/vocabulary/42/skos.ttl" -o vocabulary.ttl

3. The generated file contains a complete ``skos:ConceptScheme`` with all child
   nodes linked via ``skos:broader`` and ``skos:narrower``.
4. Load ``vocabulary.ttl`` directly into your Jena Fuseki or Sesame SPARQL backend
   configured for SKOSMOS.

---

Recipe 6: Working with Images & IIIF Viewers (Mirador)
------------------------------------------------------
OpenAtlas supports the `International Image Interoperability Framework (IIIF) <https://iiif.io/>`_.

Displaying Thumbnails in Web Pages or Markdown
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Every publicly licensed image in OpenAtlas has a fast thumbnail endpoint:

.. code-block:: text

   https://<your-instance>/api/1/files/<file-id>/thumbnail

You can embed this URL directly in HTML (``<img src="...">``) or markdown.

Loading Manifests in Mirador or Universal Viewer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Retrieve the IIIF v3 Manifest URL:

   .. code-block:: text

      https://<your-instance>/api/1/iiif/<file-id>/manifest/3

2. Open any web-based IIIF viewer (such as the `Mirador Demo <https://projectmirador.org/embed.html>`_).
3. Paste the manifest URL into the viewer's "Add Resource" dialog to explore
   high-resolution zoom, panning, and polygon annotations.

---

Recipe 7: Ready-to-Use Scripts for Excel / CSV Export
-----------------------------------------------------
If you need to load OpenAtlas data into Excel, R, or Pandas, copy and paste the
following short scripts:

Python (Downloads Entities to Excel / CSV)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Requires ``requests`` and ``pandas`` (install via ``pip install requests pandas openpyxl``):

.. code-block:: python

   import pandas as pd
   import requests

   BASE_URL = "https://demo.openatlas.eu/api/1"
   HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}

   # 1. Fetch entities
   response = requests.get(f"{BASE_URL}/entities/person?limit=100", headers=HEADERS)
   data = response.json()

   # 2. Convert to DataFrame
   items = data.get("orderedItems", [])
   rows = [{"id": item["id"], "name": item["label"]} for item in items]
   df = pd.DataFrame(rows)

   # 3. Save as Excel and CSV
   df.to_excel("openatlas_persons.xlsx", index=False)
   df.to_csv("openatlas_persons.csv", index=False)
   print(f"Successfully saved {len(df)} records!")

R (Downloads Entities to a Data Frame)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: r

   library(httr)
   library(jsonlite)

   url <- "https://demo.openatlas.eu/api/1/entities/person?limit=100"
   res <- GET(url, add_headers(Authorization = "Bearer YOUR_TOKEN"))
   data <- fromJSON(content(res, as = "text", encoding = "UTF-8"))

   df <- data.frame(
     id = data$orderedItems$id,
     name = data$orderedItems$label
   )

   write.csv(df, "openatlas_persons.csv", row.names = FALSE)
   print(paste("Saved", nrow(df), "persons to openatlas_persons.csv"))
