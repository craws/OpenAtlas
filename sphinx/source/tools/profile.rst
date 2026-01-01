Profile
=======

.. toctree::

When logged in, you can access your **profile** at the right top of the page.
Here you can edit personal information and adapt the user interface to your
preferences.

Change password
---------------
To **Change password** enter the current password and a new one twice.

General
-------
* **Name** - optional, provide your full name to make it easier for other users
  to identify you
* **Email** - providing an email address is important in case you have to reset
  your password
* **Show email** - uncheck to hide your email for other users
  (except admins and managers)
* **Newsletter** - check to receive newsletters including an unsubscribe link

Modules
-------
Here you can adjust shown interface elements to your preferences. You still see
unselected elements such as hours, minutes and seconds in a form, when data
was already entered in those fields.

* **Map Overlay** - needed to see overlays on the :doc:`/tools/map` as
  well as insert new overlays and edit them
* **Time** - show time fields in forms, see :doc:`/ui/date`

.. _display:

Display
-------
* **Language** - select your preferred language for the user interface
* **Table rows** - amount of rows that are shown
* **Show aliases in tables** - show aliases of actors and places in tables and
  make them searchable
* **Show created and modified information** - show when/by whom an entry was
  created/updated
* **Show import information** - show project and identifier for entities
  that were imported from another project
* **Show CIDOC class** - show the corresponding CIDOC class at entity view
* **Default map zoom** - define the lowest zoom level to include all
  features in a :doc:`/tools/map` view
* **Max map zoom** - adjust how far you can zoom into a :doc:`/tools/map`.

Presentation site
-----------------
URLs regarding a presentation site can be set/overridden by users. This
can be useful e.g. in case multiple projects are sharing an instance but use
different presentation sites for their data.

* **Website URL** - address of the presentation site, e.g.
  https://frontend-demo.openatlas.eu/. A link to the website will be displayed
  at the backend's overview page
* **Resolver URL** - if entity details can be viewed by using the id at
  the end of an URL, a resolver URL can be specified. Example: with the
  resolver URL https://example.net/entities/ a link for the presentation site
  view of an entity would be shown in the backend and would look like this:
  https://example.net/entities/1234
