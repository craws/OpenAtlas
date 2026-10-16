Getting Started
===============

This guide explains how to connect to the OpenAtlas API, configure access
permissions, obtain an API token, and make your first requests.

Access Modes
------------
By default, the OpenAtlas API is **protected** to prevent unauthorized access
to non-public research data. However, administrators can configure public
access in the application settings:

1. Log in as an Administrator.
2. Navigate to **Admin** -> **Settings** -> **API** (:doc:`/admin/api`).
3. Toggle **Public** to *On* or *Off*:

   * **Public (Off)**: The API requires authentication via Web Session, JWT
     Bearer Token, or an IP address on the whitelist.
   * **Public (On)**: The API can be read publicly without credentials. Only
     files marked with an open license and set to publicly shareable will be
     accessible.

Authentication Methods
----------------------

1. Web Browser Session
^^^^^^^^^^^^^^^^^^^^^^
If you are logged into the OpenAtlas user interface, your browser session cookie
is automatically shared with the API. You can visit any API URL directly in your
browser without providing additional credentials.

2. API Token (JWT Bearer Token)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For scripts, analytical tools, external websites, or third-party platforms,
access is authenticated using JSON Web Tokens (JWT).

.. note::
   Only OpenAtlas Administrators can generate API tokens.

**Generating a Token**:

1. Open **Admin** -> **Settings** -> **API** (:doc:`/admin/api`).
2. In the **API token (JWT)** panel, select **Generate**.
3. Choose the target **User** whose permissions the token will inherit.
4. Set an **Expiration** time in days (or ``0`` for no expiration).
5. Give the token a memorable **Token name** (e.g. ``QGIS-Project-2026``).
6. Click **Generate**. Copy the token string immediately — it is displayed
   only once!

**Using the Token in HTTP Headers**:
Include the token in the ``Authorization`` header of every request:

.. code-block:: text

   Authorization: Bearer <your-jwt-token>

3. IP Whitelist
^^^^^^^^^^^^^^^
If an external server needs access from a static IP address, an administrator
can add that IP to the ``ALLOWED_IPS`` list in ``instance/production.py``.

Your First Request: System Information
--------------------------------------
The endpoint ``/api/1/system/info`` returns global configuration parameters
such as map defaults, enabled modules, and available image sizes.

Browser / Swagger UI
^^^^^^^^^^^^^^^^^^^^
1. Open the interactive Swagger UI at ``/api/1/docs/swagger``.
2. Click the green **Authorize** button at the top right.
3. In the dialog, enter your token in the format: ``Bearer <your-token>``.
4. Click **Authorize**, then **Close**.
5. Scroll to **system** -> ``GET /api/1/system/info``, click **Try it out**,
   and click **Execute**.

Terminal (cURL)
^^^^^^^^^^^^^^^
.. code-block:: bash

   curl -X GET "https://demo.openatlas.eu/api/1/system/info" \
        -H "Authorization: Bearer YOUR_TOKEN_HERE" \
        -H "Accept: application/json"

Python
^^^^^^
.. code-block:: python

   import requests

   BASE_URL = "https://demo.openatlas.eu/api/1"
   headers = {"Authorization": "Bearer YOUR_TOKEN_HERE"}

   response = requests.get(f"{BASE_URL}/system/info", headers=headers)
   data = response.json()

   print(f"Site Name: {data['siteName']}")
   print(f"Default Language: {data['defaultLanguage']}")

R
^
.. code-block:: r

   library(httr)

   url <- "https://demo.openatlas.eu/api/1/system/info"
   res <- GET(url, add_headers(Authorization = "Bearer YOUR_TOKEN_HERE"))
   data <- content(res, as = "parsed")

   print(data$siteName)
