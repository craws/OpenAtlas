Places
======

.. toctree::

Below, you can find out how to enter new places and how to use the map.

Create a new place
------------------

To start entering a new :doc:`Place</entity/place>` click the **Place**
button in the :doc:`menu</ui/menu>`. Then use the **+ Place** button to get
to the respective form. The following information can be entered:

* Choose a descriptive :doc:`/ui/name`; as in all other forms, a name is
  required to save data
* If a place has several designations or is also known by other names, note
  them under :doc:`/ui/alias`. Please keep in mind: Place names in other
  languages can be covered by using **Geonames** as a
  :doc:`/entity/reference_system`
* Select a fitting :doc:`/entity/type` from the list. If none can be found,
  you can add new types (depending on your user group). You can find more
  information on types and how to add new ones :doc:`here<types>`
* Add an **administrative unit** or **historical place** and/or link the
  place to an :doc:`/entity/reference_system` (see a tutorial
  :doc:`here<reference_systems>`)
* You can also add a :doc:`/ui/date` and a free text :doc:`/ui/description`

How to use the map
******************

The :doc:`/tools/map` has multiple functionalities:

* You can zoom in and out by using the **+** and **-** button or make the
  map full screen
* Use the magnifying glass to search for places. Type a place name in the
  search field, press enter and choose the correct place from the list. The
  map will zoom to the chosen location and a pop-up will be shown.
  You can choose from the following options:

  * **Import ID** will import the related Geonames ID into your form
  * **Import Coordinates** will import the related coordinates and show a
    marker on the map
  * **Import ID and Coordinates**

* The map on which the visualization is based can be changed by hovering
  over the layer button. "Landscape", "Street Map" or "Satellite" views are
  available. In addition, various settings for the maps can be made, e.g.
  whether clusters or markers are to be displayed
* The map can also be used to set your own markers for locations. Four
  different modes are available for this:

  * **Centerpoint**: Sets a point at the position a physical thing is
    located at
  * **Linestring**: A line can be drawn to show the location of e.g. a
    border, a street, or an old river bed. Double-click on the last drawn
    point to end the drawing mode
  * **Shape** (rectangular symbol): You can use the this to draw any shape
    that represents the location - use this if the exact location of a
    physical thing is known such as the outline of a certain building with
    or the exact shape of a grave in a georeferenced burial ground plot. To
    close the polygon click on the first drawn point; **please note**:
    drawing doughnut shapes with holes is not possible.
  * **Area**: You can use the polygon to mark an area where the
    physical thing is/was located, but whose exact location is unknown.
    **Please note**: Select the area big enough to be 100% sure that
    the object is/was located in it. To close the polygon click on the first
    drawn point; **please note**: drawing doughnut shapes with holes is not
    possible.
  * After the marker/polygon has been drawn/set, further information can be
    entered into the pop-up, such as a name or a description as free text.
    This is optional but useful in case you draw multiple geometries for one
    entry. In addition, data about the polygon and coordinates can be
    copied from the corresponding field of the pop-up window
  * By clicking on the drawn shape or marker, these can be edited and/or
    deleted
  * All the entered information is saved when pressing the **Insert** button

Reference Systems - GeoNames
****************************
You can also link your data to GeoNames without using the map. To do so,
add the respective GeoNames identifier in the dedicated field and choose if
it is an exact match or close match. **Please note**: As for all references
systems, information can not be saved without stating which kind of match
it is.

By clicking the **Insert** or **Insert and continue** button you can save
the information
