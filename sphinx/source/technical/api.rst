API
***

.. toctree::

Introduction
============

This page provides an overview of the OpenAtlas API. An (`API <https://en
.wikipedia.org/wiki/API>`_) allows easy and controlled access to the data
stored in an OpenAtlas instance from external sources, such as presentation
sites or analytical tools. The information provided is readable for human and
machines alike. By using the API data can be queried in several different ways.

The development of the OpenAtlas API follows the
`RESTful <https://restfulapi.net/rest-architectural-constraints/>`_ constraints.

Testing the API is possible via: https://demo.openatlas.eu/swagger.
Using it with the data from a specific OpenAtlas instance is possible by
visiting <your-domain.eu>/swagger. Be aware
that the :doc:`/admin/api` has to be set to public in the admin setting
section of the instance.

Quick Start Guide
=================
The API can be accessed via the OpenAtlas user interface or through an URL GET
requests.

1. UI access
------------
Each detail view of an entity provides two buttons (JSON and RDF). Via those
buttons the format, in which the entity will be exported, can be selected.
If the buttons are not visible, please change the **Show API links**
in the :ref:`display` tab of your :doc:`/tools/profile` in the settings.

By using the UI in this way, only a single entity can be accessed.

.. figure:: api_ui_json.jpg
   :align: center

   Possible JSON API formats

.. figure:: api_ui_rdf.jpg
   :align: center

   Possible RDF API formats


2. URL / GET access
-------------------
The most common way to communicate with the OpenAtlas API is through GET
request. This can be done either manually from the local browser or with other
applications following a specific URL schema:

.. code-block::

    {domain}/api/{api version}/{endpoint}?{parameter}&{parameter}

**Example URL**
    https://demo.openatlas.eu/api/0.3/entity/5117
**Domain**
    Location of the OpenAtlas instance from which information should be
    retrieved, e.g. https://demo-openatlas.eu/ for the demo version
**API Version**
    Input without a version number leads to the current stable version
    (`https://demo.openatlas.eu/api/entity/5117 <https://demo.openatlas.eu/api/entity/5117>`_).
    If another version of the API is to be used, the version number can be
    specified (e.g. demo.openatlas.eu/api/**0.4**/entity/5117). A version
    overview can be found under Versioning_.
**Endpoints**
    Specific data can be queried by attaching an endpoint
    (e.g. demo.openatlas.eu/api/0.4/**entity**/5117). The information is
    provided in a human - and machine-readable form. For further information
    see Endpoints_.
**Required path values**
    Must be included to create a valid URL. Different endpoints require
    different values (e.g. demo.openatlas.eu/api/0.4/entity/**5117**.
    **5117** is an ID as required by the entity endpoint) - all required
    values are state in **{** **}** at the Endpoints_ definition.
**Parameters**
    Used to structure additional information for a given URL. They are added
    to the end of an URL after the "?" symbol
    (e.g. demo.openatlas.eu/api/0.4/entity/5117**?**download=true). All
    available Parameters can be found under Parameters_. For more general
    information see this
    `article <https://www.botify.com/learn/basics/what-are-url-parameters#:~:text=URL%20parameters%20(also%20known%20as,by%20the%20'%26'%20symbol.>`_.

Versioning
==========
.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - stable
     - deprecated
     - unstable
     - unavailable
   * - `0.4 <https://demo.openatlas.eu/swagger/>`_
     - None
     - 1.0
     - 0.3, 0.2, 0.1

The OpenAtlas API follows the notion of
`sequenced based versioning <https://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
and reflects the significance: **major.minor.fix** e.g. **3.11.1**. Only the
**major** number is used for the URL path. **Minor** and **fix** are used for
documentation reasons only with the exception of versions 0.1, 0.2, 0.3 and 0.4.
A **stable** version of the API will be available at all times. In addition,
**previous** versions will still be usable but tagged as **deprecated**. A
warning will be posted in the
`roadmap <https://redmine.openatlas.eu/projects/uni/roadmap>`_ and
`release notes <https://redmine.openatlas.eu/projects/uni/news>`_ before
a versions is discontinued. **Unstable** versions are currently
still under development, so breaking changes may occur at any time without
prior notice.

Endpoints
=========

Through different endpoints, data can be retrieved from OpenAtlas. Each version
has an own set of endpoints, make sure to use the correct one.

The current version 0.4 endpoint descriptions are available at:

* `Current OpenAPI specification <https://demo.openatlas.eu/swagger/>`_ for
  the OpenAtlas demo version
* `Local OpenAPI specification </swagger>`_: this link is only available if
  called from an OpenAtlas instance

The requested information is provided in the
`Linked Places format (LPF) <https://github.com/LinkedPasts/linked-places-format>`_.
Alternatively,
`GeoJSON <https://datatracker.ietf.org/doc/html/rfc7946>`_, `Linked Open Usable Data <https://linked.art/>`_
or RDFs, derived from `Linked Open Usable Data <https://linked.art/>`_
data, can be accessed.

Parameters
==========

By using parameters the result of the requested endpoint can be manipulated
(filtered, searched, sorted, etc.). Each endpoint provides another set of
parameters which can be used. Consult the `Endpoints`_ list for more details.

Parameters are added to the end of an URL after the "**?**" symbol
(e.g. demo.openatlas.eu/api/0.4/entity/5117**?download=true**) and are
connected with the "**&**" sign.
For more general information on this, see this
`article <https://www.botify.com/learn/basics/what-are-url-parameters#:~:text=URL%20parameters%20(also%20known%20as,by%20the%20'%26'%20symbol.>`_.

* `Current OpenAPI parameters <https://demo.openatlas.eu/swagger/>`_ at the
  OpenAtlas demo version
* `Local OpenAPI parameters </swagger>`_: this link is only available if
  called from an OpenAtlas instance

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
`Flask-RESTful <https://flask-restful.readthedocs.io/en/latest/>`_ extension
and displays an error message provided by its own
`error handler <https://flask-restful.readthedocs.io/en/latest/reqparse.html#error-handling>`_

Proxy
=====

If the server is behind a proxy, issues with the RDF export of entities can
occur. To provide the OpenAtlas API with a proxy server, add the following
line to **instance/production.py**

.. code-block:: python

    PROXIES = {
        'http': 'http://someurl.org:8080',
        'https': 'http://someurl.org:8080'}

Authentication guide
====================
No authentication is needed to use the OpenAtlas API.
