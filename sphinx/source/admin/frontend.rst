Frontend
========

.. toctree::

Many projects have a presentation site (frontend) to make the project
results accessible to a wider audience. If a running
version of a presentation site exists already, the following values can be
configured via Admin to create links the backend:

* **Website URL** - address of the presentation site, e.g.
  https://frontend-demo.openatlas.eu/. A link to the website will be displayed
  at the backend's overview page
* **Resolver URL** - if entity details can be viewed by using the id at
  the end of an URL, a resolver URL can be specified. Example: with the
  resolver URL https://example.net/entities/ a link for the presentation site
  view of an entity would be shown in the backend and would look like this:
  https://example.net/entities/1234

Linking the presentation page via resolver URL to the backend allows you to
view entries and their changes in this frontend as well.
