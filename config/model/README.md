This is a draft

# About

In **config/model** are the configuration files which are responsible for
display, forms and similar. The main motivation for this approach is to speed
up development and make it easier to understand the software.

Changes can be made to test different setups, but we strongly advice against
implementing changes for productive environments for following reasons:

* There maybe conflicts with future OpenAtlas updates, espescially because
this approach is relatively new and will be subject to changes.
* Currently, there are no checks or validation functions (which might change)
* Even if the changes don't break the application, they might cause unwanted
side effects in the application, API, presentation sites or similar.

A much better approach would be to test needed changes and then tell us about
it. In case we decide to implement suggested changes, it would mitigate the
dangers mentioned above.

# Structure

* **class_groups.py** - configuration for grouping classes, e.g. person and group will
be displayed together in "actor" sections at overviews
* **model.py** - used for class instantiation
* **classes** folder - detailed configuration of individual OpenAtlas classes

# Functionality

With changes in the config files it is possible to:
* Add, change or remove relations between classes, e.g. make some required
* Determine modes of linking, e.g. if relations are edited directly at an
entity form or via tabs
* Change display details like labels and the order of shown items, e.g. tabs

# Limitations

* It is not possible to add new classes via the config alone. This would also
require database adaptions.
* Although it is possible to define non CIDOC conform relations they will fail
because of additional checks in the user interface.
