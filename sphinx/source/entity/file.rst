File
====

.. toctree::

CIDOC documentation: :cidoc_entity:`E31 Document<e31-document>`

The first tab **Files** shows an overview of used disk space and a **List**
button to show all files.

.. include:: /entity/navigation.rst

If entities are linked to displayable files the first linked file is shown in
the info tab. If another image should be displayed it can be changed in the
files tab of each entity.

Files can be uploaded by editors if they don't exceed the upload size limit and
have one of the allowed extensions. Both criteria are displayed in the
upload form. It is possible to upload multiple files in one go. They can
either be selected via the file field or by drag and drop.

Form fields
-----------
* **File** - choose a file from your computer
* :doc:`/ui/name` - a name is required; if field is left empty, it will be
  filled with the file name after file selection
* **License** - files such as images can only be shown on a presentation
  site and archived if a license is defined; furthermore it is just good
  practice to define licence
* :doc:`/ui/description`

Form fields important for public sharing
----------------------------------------
Beside the license other information is important in case it is planned to
share files with the public, e.g. at a presentation site or a public archive.
More information is available at :ref:`public_sharing_label`

* **Public sharing allowed** - indicates if public sharing is allowed
* **Creator** - the creator of the file, e.g. the designer of a logo
* **License holder** - mention if different from creator

Can be linked via tabs to
-------------------------
* :doc:`/entity/source`
* :doc:`/entity/event`
* :doc:`/entity/actor`
* :doc:`/entity/place`
* :doc:`/entity/reference`

Settings
--------
File settings can be accessed via the Files menu item. Not all users can
change the settings; Options provided are:

* **Maximum file size in MB** limits the maximum file size; also limits the
  total size when multiple files are uploaded together
* **Profile image width in pixel** - related to the layout of info tabs
* **Allowed file extensions** - e.g. pdf, jpg, jpeg, svg

Images that can be displayed in the browser are defined through their
extensions and can be changed in the configuration file
(e.g. instance/production.py) default is:

.. code-block:: python

   DISPLAY_FILE_EXT = ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']

Logo
----
You can chose a custom logo. To do so chose an already uploaded file with a
displayable file extension. The displayed logo has a max-height of 120 px.
If you have selected a larger image your browser will try to scale it.

Image preview
-------------
If image processing is enabled (default=on, configurable by admins) small
images of files are shown in tables.

How to make files available for the public
------------------------------------------
In case files are supposed to be shared with the public, e.g. on a presentation
site or a public archive, several criteria have to be met.

Criteria checked by the software
********************************
* The file must exist
* A license has to be specified
* **Public sharing allowed** has to be marked

In case these criteria aren't met, a file won't be:

* Shared via the :doc:`/technical/api`
* Won't show up on presentation sites developed by the OpenAtlas team
* Won't be included in long time archiving
  if `ARCHE <https://arche.acdh.oeaw.ac.at/>`_ is used

Criteria checked by managers and users
**************************************
* The linked license is correct and allows public sharing
* Other license specific criteria, e.g. specifying the creator, are met

A automatic check for those specifics is not possible as there are many
licenses with numerous different criteria. Therefore it is the
responsibility of the project management to ensure that all necessary
requirements are met. To indicate this use the **public sharing
allowed** flag.

**Used licenses should linked to an external reference (e.g. an URL) were
possible as it is informative for other users and viewers.**
