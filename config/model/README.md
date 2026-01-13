# Model configuration

Within the OpenAtlas source code configuration files, which determine model
relations, display, forms and the like, can be found in **config/model**.
The main motivation for this approach is to speed up development and make
it easier to understand the system.

Changes can be made to test different setups, but we strongly advice against
implementing changes for productive environments because:

* There may be conflicts with future OpenAtlas versions, as this approach is
relatively new and will be subject to changes.
* Currently, there are no check or validation functions for the configuration
* Even if changes appear to work, they might cause unwanted side effects in
the application, API or presentation sites.

A better approach would be to test needed changes and then tell us about it.
In case we implement suggested changes, it would mitigate the issues mentioned
above.

# Functionality

Changes in the config files allow you to:

* Add, change, or remove entity classes and their relations
* Change display details like labels and the order of shown items, e.g. tabs

# Limitations

* It is not possible to add new classes via the config alone, as this requires
database adaptations. * Non-CIDOC-conformant relations can be defined in the
file, but they will fail because of additional user-interface checks.

# File structure

* **class_groups.py** - configuration for grouping classes, e.g. person and
group will be displayed together in "actor" sections at overviews
* **model.py** - used for class instantiation
* **classes** folder - detailed configuration of individual OpenAtlas classes

# **Class configuration structure**

Description of the structure for classes used in the classes directory.

* **label** - optional (default = class name)
* **attributes**
  * **values**: name, alias, dates, location, description
  * **options**: label, required, annotated (only for description)
* **relations** - the order affects display of entity views and forms
  * **label** - optional (default = relation name)
  * **classes** - a list of related OpenAtlas classes
  * **property** - the CIDOC property used to link classes
  * **inverse** - link direction (default = False)
  * **required** - if link is required (default = False)
  * **multiple** - if multiple connections are possible (default = False)
  * **mode**
    * **direct** - editable at the entity form
    * **tab** - editable via tabs (default)
  * **add_dynamic** - determines if types can be added dynamically
    (default = False)
  * **type** - special case to add a type to the link, e.g. involvement
  * **additional_fields** - special cases to add link information
    * **dates**
    * **description**
    * **page** - like description, used for references
  * **tooltip** - shown in entity form if mode is direct
  * **tab** - display options if shown via tabs
    * **columns** - columns shown for related entities, optional
      (default = standard columns)
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
    * **person_place** - show event places at an actor view
    * **place_person** - show involved actors of events at a place view
  * **additional_information** - labels can be set optionally
    * **file_size** - used for files
    * **file_extension** - used for files
    * **type_information** - show additional information for types, e.g. the id
      for imports and if selectable
  * **network_color** - color of entities in the backend network visualisation
* **extra**
  * **reference_system** - possibility to configure to add external reference
    links
