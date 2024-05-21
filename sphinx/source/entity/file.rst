File
====

.. toctree::

CIDOC documentation: :cidoc_entity:`E31 Document<e31-document>`

The first tab **Files** shows an overview of used disk space and a **List**
button to show all files.

.. include:: /entity/navigation.rst

If entities are linked to displayable files the first one is shown in the info
tab but can be changed to another one in the files tab of the entity.

Files can be uploaded by editors if they don't exceed the upload size limit and
have an allowed extension. Both criteria are displayed at the upload form. It
is possible to upload multiple files in one go. They can either be selected in
the file field or drag and dropped into the specified area.

Form fields
-----------
* **File** - here you can chose a file from your computer
* :doc:`/ui/name` - if empty it will be prefilled after the file selection with
  the filename
* **License** - which works like a :doc:`type`, it is a good practice to define
  one
* :doc:`/ui/description`

Form fields important for public sharing
----------------------------------------
Beside the license other information is important in case it is planned to
share files with the public, e.g. at a presentation site or a public archive.
More information is available at :ref:`public_sharing_label`

* **Public sharing allowed** - indicates if public sharing is allowed
* **Creator** - the creator of the file, e.g. the designer of a logo
* **License holder** - if not the same as creator

Can be linked via tabs to
-------------------------
* :doc:`/entity/source`
* :doc:`/entity/event`
* :doc:`/entity/actor`
* :doc:`/entity/place`
* :doc:`/entity/reference`

Settings
--------
* **Maximum file size in MB** - this limits also the total size of multiple
  file upload
* **Profile image width in pixel** - related to the layout of info tabs
* **Allowed file extensions**

Images that can be displayed in the browser are defined through their
extensions and can be changed in the configuration file
(e.g. instance/production.py) default is:

.. code-block:: python

   DISPLAY_FILE_EXT = ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']

Logo
----
You can chose a custom logo. The file has to be uploaded before and has to have
a display file extension. The displayed logo has a max-height of 120 px. If you
selected a larger one the browser will try to scale it.

Image preview
-------------
If image processing is enabled (default=on, configurable by admins) and user
have **Show icons in tables** in their :doc:`/tools/profile` activated, small
images of files are shown in tables.

Please be aware with many files and large tables this can impact performance.

How to make files available for the public
------------------------------------------
In case it is planned to share files with the public, e.g. at a presentation
site or a public archive, several criteria have to be met.

Criteria checked by the software
********************************
* The file must exist
* A license has to be specified
* It has to be marked with **public sharing allowed**

In case these criteria aren't met, a file won't be:
* Shared via the :doc:`/technical/api`
* Won't show up on presentation sites developed by the OpenAtlas team
* Won't be included in case the long time archiving
system `ARCHE <https://arche.acdh.oeaw.ac.at/>`_ is used

Criteria checked by managers and users
**************************************
* The linked license is the correct one and allows public sharing
* Other license specific criteria, e.g. specifying the creator, are met

There are many licenses with many different criteria, e.g. a
CC-BY 4.0 license requires the attribution to the creator. Because it is not
possible to check these automatically, it is the responsibility of
the project management to ensure that all necessary requirements
are met and to indicated it via setting the **public sharing allowed** flag.

Be aware that licenses can be linked to an external reference (e.g. an URL)
which might be informative for other users or viewers.
