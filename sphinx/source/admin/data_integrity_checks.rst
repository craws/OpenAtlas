Data integrity checks
=====================

.. toctree::

OpenAtlas puts great emphasis on the data quality. Even if the
responsibility for the quality of the information entered ultimately lies
with the individual projects, avoidance of inconsistent on a technical level
are important during the development of the application. It is therefore not
possible e.g. to enter the start date of an event after the end date of the
same event

Nevertheless mistakes happen, not only on the application level but also
when importing data from other projects or deleting files outside of the
application, etc. Therefore, functions to check possible inconsistencies were
implemented and are described in detail below.

Orphans
-------

Orphans
*******
Here unlinked data are shown. These so called orphans could be artifacts
from imports or results of bugs and can be deleted. If orphans seem to appear
regularly (without data imports or known bugs) please report this issue to the
OpenAtlas team e.g. via the
`OpenAtlas redmine <https://redmine.openatlas.eu/>`_.


Entities without links
**********************
Entries shown have no relation to other entities. Of course that can be
part of the normal data set, but should be check if correct. An unlinked
entity could be artifacts of an import or were not linked by accident.

Type
****
The types listed here were created but have no sub types or associated data.
They might have been pre-installed before teams have started entering
information or were created and then never used.

Missing files
*************
File entities without a corresponding file are listed here. This is (most
likely) caused by the deletion of files from the dataset.

Orphaned files
**************
Files without a corresponding file entity are listed here.

Orphaned IIIF files
*******************
IIIF files without a corresponding entity are listed here.

Orphaned annotations
********************
Annotations that are linked to an entity, but file and entity themselves are
not linked are listed here. There are three options to proceed:

* *Relink entity*: Adds a link between file and entity
* *Remove entity*: Removes the entity from the annotation
* *Delete annotation*: Deletes the whole annotation

Orphaned subunits
*****************
Subunits without a link to the level above, e.g. a feature
with no connection to a place.

Circular dependencies
*********************
It can be checked if an entity is linked to itself. This could happen, for
example, if a person has been entered as is married to themself or a type
has itself as super. It shouldn't be possible to create circular
dependencies within the application but nevertheless it's useful to
check the database as this can happen through data imports or bugs. If you
find circular dependencies in your dataset regularly with a previous report
or known bugs, please report the issue e.g. via the
`OpenAtlas redmine <https://redmine.openatlas.eu/>`_.

Dates
-----
In this view various results of invalid or inconsistent dates are shown.

Invalid dates
*************
In this tab invalid date combinations are shown, for example dates of begins
That are later than end dates. These issues should be fixed, otherwise the user
interface won't allow to update these entities.

Invalid link dates
******************
Similar to "invalid dates", invalid link dates should be fixed as soon as
possible.

Invalid involvement dates
*************************
Incompatible dates for involvements are shown. Example: A person participated
in an event for longer than the event lasted.

Invalid preceding dates
***********************
Here, incompatible dates for chained events are listed. Example: A
preceding event starts after the succeeding event.

Invalid sub dates
*****************
This tab shows incompatible dates for hierarchical events. Example: A
sub event begins before the super event began.

Check links
-----------
Here, every link will be checked for its CIDOC validity. Depending on the
amount of data this can take some time. While data entered by using the
OpenAtlas user interface should always be CIDOC conform, imported
data should be check after import. If invalid links are
found the problem should be resolved in the original data source.

Check link duplicates
---------------------
Two tests are combined:

The first test checks for duplicate links that are identically. These links
can be afterwards by clicking the *Delete link duplicates* button.

In case the first test found no duplicate links the dataset will be checked
for entities that were connected to a single use type multiple times.
Example: A place has been linked to types castle and city. Only one of the
types will be displayed in the user interface, the other one would be
deleted automatically if the entry is updated by anyone.
You are then given the option to have a look at the links and to remove the
wrong ones by clicking the **Remove** link next to the entries in the
last column.

By using the OpenAtlas interface link duplicates should be avoided
automatically but can happen due to data import or bugs. If this is a
reoccuring issue for your dataset, please report e.g. via the
`OpenAtlas redmine <https://redmine.openatlas.eu/>`_.

Check similar names
-------------------
This test will search for similar entity names. Depending on selection
and data volume this might take some time. The following options are given:

* **Classes** - select the class you want to search for similar names
* **Ratio** - select how similar the names should be, 100 is the default and
  means 100% identical

The function uses the `fuzzywuzzy <https://pypi.org/project/fuzzywuzzy/>`_
package which uses the
`Levenshtein Distance <https://en.wikipedia.org/wiki/Levenshtein_distance>`_.

Check files
-----------

In this section, all files are checked for completeness and consistency.
Further information about file entities can be found in the manual under
:doc:`entity/file`.

Missing information
*******************
* **No creator**: Files without a creator entered.
* **No license holder**: Files without a license holder entered.
* **Not public**: Files that are not publicly accessible.
* **No license**: Files where no license was assigned.

File integrity
**************
* **Missing files**: A file entity was created but has no associated file.
* **Duplicated files**: Lists all files that share the same SHA value.
  In such cases, the files themselves are duplicates, but their metadata
  entries differ.
