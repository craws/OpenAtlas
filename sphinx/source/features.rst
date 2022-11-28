Features
========

Model
-----

* The OpenAtlas :doc:`/model/index` is based on the international standard of
  `CIDOC CRM <https://www.cidoc-crm.org/>`_
* :doc:`Types </entity/type>` can be used to adapt for specific research topics
* **Linked Open Data (LOD)** with `SKOS <https://www.w3.org/TR/skos-primer/>`_
  based precision via :doc:`Reference Systems </entity/reference_system>`
* Solutions to deal with :doc:`spatial </tools/map>` and
  :doc:`temporal </ui/date>` uncertainty
* Detailed mapping for
  :doc:`archaeological finds </examples/archaeological_data>`
* :doc:`Data integrity check</admin/data_integrity_checks>` functions
* :doc:`Model link checker<model/link_checker>` to confirm CIDOC CRM validity

Geolocating
-----------

Places with known location can be entered into an interactive
:doc:`/tools/map` based on
`Leaflet <https://leafletjs.com/>`_, which features different view layers,
allows for zooming, fullscreen mode, clustering, searching and much more.
`PostGIS <https://postgis.net/>`_ is used for creating and manipulating spatial
data. Therefore, it is possible to enter location as needed as multiple points,
lines, areas and shapes.

User interface
--------------

* File upload
* Interactive map
* Search and Filters
* Bookmarks and notes
* Internationalization
* User manual
* Network visualization

Due to the integration of `D3.js <https://d3js.org/>`_ it is possible to
visualize data as a network graph in 2D and 3D.

An English user manual corresponding to the current software version is provided in the application itself. Throughout the application are context specific links to the manual but there are also manual entries about step-by-step examples, troubleshoot instructions and more. Feel free to take a look at the user manual of the demo version.

Multiple languages for the user interface are implemented with `gettext <https://www.gnu.org/software/gettext/>`_. At the moment English and German are available. Easy extension to other languages is possible, when translations available.

To allow quick navigation, even in a big data set, full-text search is possible. Additionally, a refined advanced search can be used to filter the results (e.g. only actors or a search in descriptions). Tables and tree views, that can have many entries, have a full-text filter for convenience. The map provides a search field for a GeoNames search.

Files can be uploaded and linked with entities. It is possible to link one file to multiple entities (e.g. a group picture showing different actors) and the other way round. Files are available to download in the original size. In the admin interface the upload file size limit and allowed extensions can be configured.

Newsletter. This feature enables managers and admins to send newsletters. An editable receiver list with users who have opted in is shown. Newsletters will contain an unsubscribe link.

Bookmarks and notes are user specific and can be used to e.g. mark entries which need further editing. Already bookmarked entities and notes are shown on the start page after login.

User management
---------------

* Users and groups can be used to grant different access levels
* Newsletter
* Password reset

Data exchange
-------------

API
***

An application programming interface (API) for easier exchange with other
information system was implemented. The output is based on
`JSON-LD <https://json-ld.org/spec/latest/json-ld/>`_ syntax and
`GeoJSON <https://tools.ietf.org/html/rfc7946>`_.
`Linked Places <https://github.com/LinkedPasts/linked-places>`_
was used as standard.

Export
******

A CSV export for single tables and an SQL export (pg_dump) are implemented in
the admin interface.

Import
******

CSV lists can be imported, e.g. a list of places (name, description, dates and
point coordinates).

Anthropological Analyses
------------------------

Anthropological analysis tools allow to enter data that derived from analyses
on human remains. A tool to do sex estimation based on the method given by
Ferembach et al. 1979 was implemented already.
