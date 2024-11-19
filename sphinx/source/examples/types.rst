Types
=====

.. toctree::

:doc:`Types</entity/type>` are used to add information to all entities.
They are organized hierarchically into trees and specific for each project.
Furthermore, types help to show information in an organized way on a
presentation site. So use types instead of free text wherever possible.
There are different kind of types: A distinction is made between different
groups of types:

* Standard types - These are the types displayed as "Type" in each form.
  They are used to specify each entity. They are single select only and can
  not be renamed or deleted (the subtypes can); some standard types are
  pre-installed
* Custom types - These types help to customize each instance of OpenAtlas;
  they can be created, edited, renamed, and deleted by each project to cover
  as much information on their data as possible; only few types come
  pre-installed as examples
* Value types - These are used to add numerical information such as
  measurements

Different user groups have different permissions regarding the creation and
modification of types. Further information can be found in the manual entry
regarding :doc:`/entity/type`. Please note that the possibility to add and edit
types depends on the user group, see :doc:`/admin/user`.

An overview of the types already created can be accessed by clicking the Types
menu item. Furthermore, new types can be created here if necessary.

.. image:: type_1.png
    :width: 400px

Create a new type tree
----------------------
To create a new custom type or value type tree press the +Type button.
Please fill out the form:

* Choose a descriptive **name** for the new type
* Decide if the type is single or multiple select (only available for custom
  types)
* Choose to which classes the new type will be added, e.g.
  :doc:`/entity/artifact` or :doc:`/entity/place`; the typ will only be
  shown in the related form
* You can also enter text into the **description** field which will be
  displayed when you mouse-over the information button next to the type’s
  name in forms.

By pressing **insert** you can create a new type tree.

To edit an already existing type tree, go to the type you want to edit,
click on its name and push the edit button next to the name.

.. image:: type_2.png
    :width: 400px

You can edit the type’s name, chosen classes and description. Please note that
changing multiple to single choice is not always possible. For more
information see :doc:`/entity/type`.

Add a type to an existing type tree
-----------------------------------

Types can be added dynamically in forms (with at least editor permission) with
basic information like name, description and super type.

A more detailed way to create a new type in an already existing standard,
custom, or value type tree, is to find that type tree in the overview and
click on it.

.. image:: type_3.png
    :width: 400px

You can then add the following information:

* Choose a descriptive name
* Choose a super if applicable, e.g. choose “Blue” as super when you are adding
  “Light blue” to the tree
* You can add external references and dates as well as a description; the
  description will be displayed when you mouse-over the information button next
  to the type’s name in the data entry form

By pressing insert you can create a new type tree.

To edit an already existing type, click on that type. Find the edit button in
the overview and change information after clicking that button.
