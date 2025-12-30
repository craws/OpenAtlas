# Model configuration
In **config/model** are the configuration files which are responsible for
model relations, display, forms and similar. The main motivation for this
approach is to speed up development and make it easier to understand the
system.

Changes can be made to test different setups, but we strongly advice against
implementing changes for productive environments for following reasons:

* There will be conflicts with future OpenAtlas updates, especially because
this approach is relatively new and will be subject to changes.
* Currently, there are no checks or validation functions
* Even if the changes don't break the application, they might cause unwanted
side effects in the application, API, presentation sites or similar.

A much better approach would be to test needed changes and then tell us about
it. In case we decide to implement suggested changes, it would mitigate the
dangers mentioned above.

# Functionality
With changes in the config files it is possible to:
* Add, change or remove relations between classes, e.g. make some required
* Determine modes of linking, e.g. if relations are edited directly at an
entity form or via tabs
* Change display details like labels and the order of shown items, e.g. tabs

# Limitations
* It is not possible to add new classes via the config alone. This would also
require database adaptions.
* Although it is possible to define none CIDOC conform relations they will fail
because of additional checks in the user interface.

# File structure
* **class_groups.py** - configuration for grouping classes, e.g. person and
group will be displayed together in "actor" sections at overviews
* **model.py** - used for class instantiation
* **classes** folder - detailed configuration of individual OpenAtlas classes

# Class configuration structure
Description of the structure for classes used in the classes directory.
* **label** - optional (default = class name)
* **attributes**
  * **values**: name, alias, dates, location, description
  * **options**: label, required, annotated (only for description)
* **relations** - the order affects display of entity views and forms
  * **label** - optional (default = relation name)
  * **classes** - a list of related classes
  * **property** - the property used to link them
  * **inverse** - link direction (default = False)
  * **required** - if possible to remove (default = False)
  * **multiple** - if multiple connections are possible (default = False)
  * **mode**
    * **direct** - editable at the entity form
    * **tab** - editable via tabs (default)
  * **add_dynamic** - if types can be added dynamically (default = False)
  * **type** - special case to add a type to the link, e.g. involvement
  * **additional_fields** - special cases to add link information
    * **dates**
    * **description**
    * **page** - like description, used for references
  * **tooltip** - shown in entity form if mode is direct
  * **tab** - display options if shown via tabs
    * **columns** - columns shown for related entities,
      optional (default = standard columns)
    * **buttons**
      * **link** - link to existing entities
      * **insert** - insert a new entity and link automatically
    * **tooltip** - shown at tab headers
* **display**
  * **buttons**
    * **copy** - provide a copy function
    * **network** - provide display of an ego network
    * **move** - to (bulk) change the type of entities (only at type view)
    * **download** - for files
    * **selectable** - toggle if selectable (only at type view)
    * **stratigraphic_tools** - only used at stratigraphic units
  * **form_buttons**
    * **insert_and_continue** - continue with another entry
    * **insert_continue_sub** - continue with entering a place sub
    * **insert_continue_human_remains** - continue with entering human remains
  * **additional_tabs**
    * **note** - possibility to add notes
    * **person_place** - special function to show event places at an actor
    * **place_person** - special function to show actors of event at a place
  * **additional_information** - labels can be set optionally
    * **file_size** - used for files
    * **file_extension** - used for files
    * **type_information** - show additional infor for types, e.g. the id for
      imports and if selectable
  * **network_color** - color of entities in the backend network visualisation
* **extra**
  * **reference_system** - possibility to configure to add external reference
    links
