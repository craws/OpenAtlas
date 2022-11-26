Features
========

Model
-----

CIDOC CRM
*********

The web interface provides tools to enter and manipulate data which will be
saved in a `CIDOC CRM <https://www.cidoc-crm.org/>`_ compatible model to a
`PostgreSQL <https://www.postgresql.org/>`_ database. A main focus of OpenAtlas
is to design a web interface that allows users not to focus on the underlying
data model but to enter data in a convenient and easy way. Therefore, the
CIDOC CRM specification was imported into the system. It can be browsed and is
used to verify link conformity between entities. Additionally, link
combinations can be tested manually e.g. when planning model extensions.

System, Custom and Value Types
******************************

Due to this feature, the model and user interface forms can be adapted for
specific research interests. Already provided system types can be extended.
Additionally, it is possible to add new types e.g. "hair color" for persons.
These type hierarchies can be configured to allow single or multiple choices.
A type can be used for multiple entities e.g. a hierarchy like "importance"
for places, actors and groups. Furthermore, value types can be created to add
numeric values e.g. weight or material composition of a find.

Linked data
***********

Entries can be linked to external reference systems using
`SKOS <https://www.w3.org/TR/skos-primer/>`_ based precision.
`GeoNames <https://www.geonames.org/>`_ and
`Wikidata <https://www.wikidata.org/>`_ are already included in
the default application using their APIs and more can be added. Also linking
generic references, e.g. providing a URL for an actor to a Wikipedia entry is
possible.

Spatial and Temporal Fuzziness
******************************

In many cases the spatial or temporal position respectively extent of an entity
is not known precisely. Therefore, OpenAtlas allows defining time-spans
(earliest/latest begin and earliest/latest end) or areas in which the temporal
respectively spatial extent can be located with a 100% certainty.

Archaeological Subunits
***********************

These allow detailed mapping of archaeological finds, e.g. in a cemetery. They
are used in a strict hierarchy: Place -> Feature (e.g. a grave) ->
Stratigraphic Unit (e.g. a coffin or skeleton) ->
Find (e.g. grave goods) and Human Remains
(e.g. for anthropological information on the burial).

Data integrity check functions
**********************************

Because data integrity is important for the quality of research data, we
implemented functions to check possible inconsistencies including checks for
orphaned data, date inconsistency, duplicates, similar names, invalid links,
unused types and more.

Geolocating
-----------

Places with known location can be entered into an interactive map based on
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
