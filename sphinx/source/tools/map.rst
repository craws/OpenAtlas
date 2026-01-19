Map
===

.. toctree::

The interactive map (based on `Leaflet <https://leafletjs.com/>`_) is a tool
to present and enter a place's location.
`PostGIS <https://postgis.net/>`_ is used for creating and manipulating
spatial data.

Navigation
----------
* Zoom in/out of the map by using your mousewheel or the **+**/**-**
  buttons in the upper left corner
* Drag the content with the mouse (left click and hold)
* Change the basemap by using layer button in the upper right corner
* Switch to full screen with the rectangle in the upper left corner

Search
------
Press the magnifying glass icon on the left side to search for
a places. The search filters data on
`GeoNames <https://www.geonames.org/>`_ and provides a list of places with
the same name. Choosing the desired places allows to import the geonames ID
and/or the coordinates of said place into the OpenAtlas place form (see below).

WKT import
----------

.. |edit| image:: edit.png

With the |edit| icon WKT text can be imported.
Clicking this button will open a new popup where a WKT geometry can be entered.
If the geometry is valid, the **draw geometry** button will be enabled. By
clicking this button the geometry will be drawn on the map and the respective
geometry popup will open to enter *title* and *description* for this geometry.

Possible WKT geometries with examples are:

* POINT(30 10)
* LINESTRING(30 10, 10 30, 40 40)
* POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))


Adding new geometries
---------------------
When in insert or update mode of a place you have the following options
(more than one can be used):

* Set a marker/point at the position where the physical thing is located
* Draw a line connected to a physical object's spatial characteristics, e.g.
  the course of a road or the bed of a river
* Draw the shape of a physical thing if the precise extend is known
* Draw an area in which the physical thing is located with 100% certainty

GeoNames
--------
The *GeoNames ID* field can either be entered manually or imported
from the map's search result

**Exact match** should be used if there is a high degree of confidence that
the concepts can be used interchangeably. By default it is a
**close match**, which means that the concepts are sufficiently similar
that they can be used interchangeably in some information retrieval
applications. Please refer to `SKOS <https://www.w3.org/TR/skos-reference/>`_
for further information.

Map Overlay
-----------
Added overlays for places will be visible on the map by default and can be
toggled with the map layer button at the upper right corner.

To insert new overlays (only available for editors or above) go to the view
of a specific place. After adding an image file in the file tab you can click
**link** in the overlay column to enter coordinates (Easting and Northing) for:

* top left corner
* top right corner
* bottom left corner

of the image to position it on the map.
The coordinates have to be stated in **WGS84** decimal degrees (EPSG 4326).
