Type
====

.. toctree::

CIDOC documentation: :cidoc_entity:`E55 Type<e55-type>`

Types are used to add information or group entities. They are hierarchical and
can be accessed and edited via the **Types** :doc:`/ui/menu` item. With this
feature the user interface can be adapted for specific research interests.

* Types can be added dynamically in forms (with at least editor permission)
  with basic information like name, description and super type
* The root type description is shown in forms as a mouse over text at
  the **i** icon
* **Untyped entities** can be checked at the type overview
* **Multiple linked entities** can be checked at the type overview, useful if
  switching to single
* Types (except value types) can be **Set unselectable**, e.g. to enter
  sub categories, via the corresponding button at a type view. But only if not
  already used by entities and at least editor permissions are needed.
* A more detailed description on how to enter new types can be found
  :doc:`here</examples/types>`

Standard types
--------------
Standard types are already present in the default installation with a few
examples.

* Cannot be deleted or renamed (but subtypes of them can)
* Are single select only
* In forms they appear with a **Type** label
* Are displayed in entity tables

Custom types
------------
Custom types can be created, deleted and renamed. The default installation
comes with one example custom type **Sex** which is used for actor.

* Can be set to allow single or multiple choices
* Can be used for multiple classes, e.g. a hierarchy "case study" for places,
  actors and events

If you want to change an existing **multiple type to single** but the
multiple checkbox is greyed out and not selectable it means that at least one
entity already used multiple. You can check these entries at the type overview
at **multiple linked entities**.

Value types
-----------
Value types can be created, deleted and renamed. The default installation comes
with an example value type **Dimensions** with the sub types **Height** and
**Weight** which are used in the form for artifacts.

* Can be used for multiple classes
* Values can be entered as decimals in forms

Form fields
-----------
* :doc:`/ui/name`
* :doc:`/ui/description`
* :doc:`reference_system`
* :doc:`/ui/date`
* A super (type) if it is a sub type of another type

Making types required
---------------------
It is possible making specifying of types required. This can be done at the
type overview in the right information display of the respective type by users
who have at least manager permissions.

Be careful with making types required, especially when there are users who
aren't permitted to create new ones. It may put them in an awkward situation at
data entry and, as a result, may even reduce the data quality.

Also keep in mind, that existing entries which haven't set this type, will than
not be possible to update, without setting the required type.
