Map
===

.. toctree::

The interactive map (based on `Leaflet <https://leafletjs.com/>`_) is a tool
to present and enter the location of places. `PostGIS <https://postgis.net/>`_
is used for creating and manipulating spatial data.

Navigation
----------
* You can zoom in/out with the mousewheel or the **+**/**-** buttons in the
  upper left corner.
* You can drag the content with the mouse (left click and hold)
* Change the basemap at the layer button in the upper right corner.
* Switch to full screen with the rectangle in the upper left.

Search
------
With the magnifying glass icon in the upper left you can search for (current)
places at `GeoNames <https://www.geonames.org/>`_.

WKT import
----------

.. |edit| image:: edit.png

With the |edit| icon a WKT text can be imported.
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
When in insert or update mode of a place you have following options available
(can be combined):

* Set a marker/point at the position where the physical thing is located.
* Draw a line connected to a physical objects spatial characteristics, e.g.
  the course of a road.
* Draw the shape of a physical thing if the precise extend is known.
* Draw the area in which the physical thing is located. E.g. if its precise
  shape is not known but known to be within a certain area.

GeoNames
--------
The *GeoNames ID* field can either be manually entered or imported from a map
search result.

The checkbox **exact match** can be used if there is a high
degree of confidence that the concepts can be used interchangeably. By default
it is a **close match**, which means that the concepts are sufficiently similar
that they can be used interchangeably in some information retrieval
applications. Please refer to `SKOS <https://www.w3.org/TR/skos-reference/>`_
for further information.

Map Overlay
-----------
If you have the module map overlay activated in your :doc:`profile`, added
overlays for places will be visible on the map by default and can be toggled
at map layer button at the upper right corner.

To insert new overlays (only available for editors and admins) go to the view
of a specific place. After adding an image file in the file tab you can click
**link** in the overlay column to enter coordinates (Easting and Northing) for:

* top left corner
* top right corner
* bottom left corner

of the image to position it on the map.
The coordinates need to be in **WGS84** decimal degrees (EPSG 4326).
