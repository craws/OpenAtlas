Type
====

.. toctree::

CIDOC documentation: :cidoc_entity:`E55 Type<e55-type>`

Types are used to add information or group entities. They are hierarchical and
can be accessed and edited via the **Types** :doc:`/ui/menu` item. With this
feature the user interface can be adapted for specific research interests.

* Types can be added dynamically in forms (for users with editor status or
  higher) with basic information like name, description and super type
* The root type description is shown in forms as a mouse over text at
  the **i** icon
* **Untyped entities** can be checked via type overview
* **Multiple linked entities** can be checked at type overview, useful if
  a type should be switched to single choice
* Types (except value types) can be **Set unselectable** via the
  corresponding button in a type view. If selected only the type's
  sub-categories can be selected in a form. Set unselectable can only be
  selected if the type is not already used for entities. You need editor
  permission or higher to make this change
* A more detailed description on how to enter new types can be found
  :doc:`here</examples/types>`

Standard types
--------------
Some standard types are pre-installed in every OpenAtlas instance. These types

* Cannot be deleted or renamed (but subtypes of them can)
* Are single select only
* Appear in forms with a **Type** label
* Are displayed in entity tables

Custom types
------------
Custom types can be created, deleted and renamed. The default installation
comes with one example custom type **Sex** which is used for actors. Custom
types

* Can be single or multiple choices
* Can be used for multiple classes, for example the type "case study" and its
  sub-types can be used in forms for places, actors, and events

If you want to change an existing **multiple type to single** but the
multiple checkbox is greyed out and not selectable, the multiple option is
used for at least one entity already. Check entries in type overview at
**multiple linked entities** and make changes if necessary.

Value types
-----------
Value types can be created, deleted, and renamed. They are used to add
values in form of decimals to an entity. The default installation
comes with an example value type **Dimensions** with the sub-types
**Height** and **Weight** which are used in the form for artifacts. Value
types

* Can be used for multiple classes
* Values can be entered as decimals in forms
* A unit such as centimetre, gram, or percentage can be specified


Form fields
-----------
* :doc:`/ui/name`
* :doc:`/ui/description`
* :doc:`reference_system`
* :doc:`/ui/date`
* A super (type) if it is a sub-type of another type

Can be linked via tabs to
-------------------------
* :doc:`reference`
* :doc:`file`

Making types required
---------------------
It is possible to make certain types required. To make a type required, go
to type overview. Mark it as required in the display on the right. You have
to have manager or higher status to do this.

Please keep in mind that not all users can add new types when making a type
required. This might lead to situations where a user is unable to choose a
fitting type for an entity and might therefore reduce data quality.

Existing entries that were entered before a typ was set to required and have
no set values for this specific type can not be updated anymore afterwards.
