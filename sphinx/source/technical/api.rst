API
***

.. toctree::

Introduction
============

This page provides an overview of the OpenAtlas Application Programming
Interface (`API <https://en.wikipedia.org/wiki/API>`_). The API is
`RESTlike <https://restfulapi.net/rest-architectural-constraints/>`_
to provide easy access to the data.

* To try out the API first hand, visit https://demo.openatlas.eu/swagger
* For developers a complete
  `Swagger documentation <https://app.swaggerhub.com/apis/ctot-nondef/OpenAtlas/>`_
  is provided.

Quick Start Guide
=================
The API can be accessed via the OpenAtlas user interface or through URL GET
requests.

1. UI access
------------
Each detail view of an entity provide two buttons (JSON and RDF) where the
formats, in which the entity should be exported, can be selected. If the
buttons are not visible, please change the **Show API links**
at the :ref:`display` tab in your :doc:`/tools/profile`.

Through the UI, only a single entity can be accessed.

.. figure:: api_ui_json.jpg
   :align: center

   Possible JSON API formats

.. figure:: api_ui_rdf.jpg
   :align: center

   Possible RDF API formats

2. URL / GET access
-------------------
The most common way to communicate with the OpenAtlas API is through GET
request, either manually from the local browser or with other applications
following a specific URL schema:

.. code-block::

    {domain}/api/{api version}/{endpoint}?{parameter}&{parameter}

**Example URL**
    https://demo.openatlas.eu/api/0.3/entity/5117
**Domain**
    Location of the OpenAtlas instance from which information should be
    retrieved; e.g. https://demo-openatlas.eu/ for the demo version.
**API Version**
    Input without version number leads to the current stable version
    (`https://demo.openatlas.eu/api/entity/5117 <https://demo.openatlas.eu/api/entity/5117>`_).
    If another version of the API is to be used, the version number can be
    specified (demo.openatlas.eu/api/**0.3**/entity/5117). A version overview
    can be found under point Versioning_.
**Endpoints**
    Specific data can be queried by attaching an endpoint
    (demo.openatlas.eu/api/0.3/**entity**/5117). The information is provided
    in a human - and machine-readable form. Further information under
    Endpoints_.
**Required path values**
    Must be included to create a valid URL. Different endpoints require
    different values (demo.openatlas.eu/api/0.3/entity/**5117**. **5117** is
    an ID as required by the entity endpoint) - all required values are state
    in **{** **}** at the Endpoints_ definition.
**Parameters**
    Used to structure additional information for a given URL. They are added
    to the end of an URL after the "?" symbol
    (demo.openatlas.eu/api/0.3/entity/5117**?**download=true). All available
    Parameters can be found under Parameters_. For more general information
    see this
    `article <https://www.botify.com/learn/basics/what-are-url-parameters#:~:text=URL%20parameters%20(also%20known%20as,by%20the%20'%26'%20symbol.>`_.

Versioning
==========
.. list-table::
   :header-rows: 1
   :widths: 20 20 20

   * - stable
     - unstable
     - deprecated
   * - :ref:`0.3<version_0_3>`
     - :ref:`0.1<version_0_1>`, :ref:`0.2<version_0_2>`
     - :ref:`1.0<version_1_0>`

The OpenAtlas API follows the notion of
`sequenced based versioning <https://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
and reflects the significance: **major.minor.fix** e.g. **3.11.1**. Only the
**major** number is used for the URL path. **Minor** and **fix** are used for
documentation reasons only with the exception of versions 0.1, 0.2 and 0.3.
A **stable** version of the API will be available at all times. In addition,
**previous** versions will still be usable but tagged as **deprecated**. A
warning will be posted in the
`roadmap <https://redmine.openatlas.eu/projects/uni/roadmap>`_ and
`release notes <https://redmine.openatlas.eu/projects/uni/news>`_ before
these versions will be discontinued. **Unstable** versions are currently
developed, so breaking changes may occur at any time without prior notice.

Endpoints
=========

Through different endpoints, data can be retrieved from OpenAtlas. Each version
has a own set of endpoints, be sure to use the right one.

.. toctree::
   :maxdepth: 1

   Version 0.3 (stable, current) <api_version_03>
   api_version_02
   api_version_01
   Version 1.0 (whitepaper) <api_version_1>

The requested information is provided in Linked Places format
`Linked Places format (LPF) <https://github.com/LinkedPasts/linked-places-format>`_. Alternatively,
`GeoJSON <https://datatracker.ietf.org/doc/html/rfc7946>`_, `Linked Open Usable Data <https://linked.art/>`_
or RDFs, derived from the `LPF <https://github.com/LinkedPasts/linked-places-format>`_ data, can be accessed.

Parameters
==========

With parameters the result of the requested endpoint can be manipulated
(filtered, searched, sorted, etc.). Each endpoint provide another set of
parameters which can be used. So please consult the `Endpoints`_ listing for
more details.

Parameters are added to the end of an URL after the "**?**" symbol
(e.g. demo.openatlas.eu/api/0.3/entity/5117**?download=true**) and are
connected with the "**&**" sign.
For more general information on this topic see this
`article <https://www.botify.com/learn/basics/what-are-url-parameters#:~:text=URL%20parameters%20(also%20known%20as,by%20the%20'%26'%20symbol.>`_.

At the moment only the :ref:`stable version 0.3<version_0_3>` of the API can
be provided by an detailed parameter list.


.. toctree::
   :maxdepth: 1

   api_parameters_03

Error handling
==============
OpenAtlas uses conventional HTTP response codes to indicate the success or
failure of an API request. Codes in the 2xx range indicate a successful request
while those in the 4xx range signal an error - providing the information was
not possible. Codes in the 5xx range indicate a server error.
If any issues occur when using the OpenAtlas API, a case-specific error message
is provided in JSON format, describing the error in more detail.

Example:

.. code-block::

  {
       "title": "entity does not exist",
       "message": "Requested entity does not exist. Try another ID",
       "url": "https://demo.openatlas.eu/api/entity/9999/,
       "timestamp": "Tue, 19 Jul 2022 13:59:13 GMT",
       "status": 404
   }

If an invalid endpoint parameter value e.g. ?sort=kfs instead of ?sort=desc is
entered, Flask catches this via its own
`Flask-RESTful <https://flask-restful.readthedocs.io/en/latest/>`_ extension.
An error message is provided by its own error handler
`error handler <https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling>`_

Proxy
=====

If the server is behind a proxy, there are some issues with the RDF export of entities.
To provide the OpenAtlas API with a proxy server, add following line to **instance/production.py**

.. code-block:: python

    API_PROXY = 'http://proxy.example:8899'

Authentication guide
====================
No authentication is needed to use the OpenAtlas API.
