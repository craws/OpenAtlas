References Systems
==================

.. toctree::

To create **Linked Open Data** (LOD) it is possible to connect entered
information with a :doc:`/entity/reference_system`. Online available
**controlled vocabularies** and **gazetteers** are particularly suitable for
this. But it is also possible to link your own data with analog resources,
such as card catalogs or inventory data from museums.

`Wikidata <https://www.wikidata.org/>`_  and `GeoNames <https://www.geonames
.org/>`_ are available in OpenAtlas by default but other applications can be
added by the users. To see which reference systems are already available on
your OpenAtlas instance, click the **Reference system** button on the start
page.

**Please note**: As for types, different user groups have different
permissions regarding the creation and modification of external
reference systems. To add or edit an external reference you have to have the
role of admin or manager. Further information can be found in the manual entry
regarding :doc:`/entity/reference_system` and under :doc:`/admin/user`.

Create a new reference system
-----------------------------

To create a new reference system click the **Reference System** button on
the starting page of your OpenAtlas instance. You will then see a list with
already added external references.
If you user group has permission to create additional external references a
**+ Reference system** button is displayed. Click it to get into the form.
Here you can add the following information:

* **Name**: Choose a descriptive name; as for other forms, a name is
  required to save data.
* **Website URL**: State the vocabulary's/gazetteer's URL, e.g.
  https://www.wikidata.org for Wikidata
* **Resolver URL**: Put in an URL that brings you to the respective entry
  when combined with an ID e.g. https://www.wikidata.org/wiki/ - see for
  example https://www.wikidata.org/wiki/Q3044 where Q3044 is an ID (the link
  will bring you directly to Charlemagne's entry in Wikidata)
* **Example ID**: An example ID can be specified, which is then used as an
  example in the corresponding input field of the different forms; for
  Wikidata this could be *Q3044* (for Charlemagne), for Geonames
  for example *2761369* (for Vienna (AT))
* **External reference match**: Here you can state a default precision (exact
  match or close match) that will be shown in the respective form; if you
  set a default reference match, the other(s) can be chosen from a drop down
  list if necessary, if no external reference match is set, it will be left
  blank and exact or close match can be chosen from a drop down list.
  Close match and exact match are
  `SKOS <https://www.w3.org/TR/skos-primer/>`_ based definitions of confidence

  * choose **Close match** if your entry and the entity in the vocabulary
    are sufficiently similar and can be used interchangeably in some
    information retrieval application (think a D-shaped belt buckle is a
    close match to a belt buckle (Wikidata ID Q3180027) or the historic
    Vienna is a close match to today's Vienna as it is included in Geonames)
  * choose **Exact match** if there is a high degree of confidence that the
    entered data and the vocabulary's entity are interchangeable (think
    Charlemagne - the King of Franks, King of Lombards who became Holy Roman
    Emperor in 800 AD is an exact match to Q3044 in Wikidata or the Venus of
    Willendorf in the Natural History Museum Vienna is an exact match to the
    entity Q131397 (Venus of Willendorf) in Wikidata)

* **Classes**: Select in which forms the new external reference should
  be displayed. This can appear in one or more forms
* **Description**: you can add a description as free text if desired

Save the information to the database by clicking the **Insert** button.

**Please keep in mind**: When information is entered into a reference system
field in a form, the data in this form can only be saved if an external
reference match is also specified.
