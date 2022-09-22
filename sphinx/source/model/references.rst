References
==========

.. toctree::

References
----------

OpenAtlas uses :cidoc_property:`P67<P67-refers-to>` ("refers to") in order to
link various entities to references.
References can be:

* Documents (:cidoc_entity:`E31<E31-Document>`) such as files, bibliographic
  entities or references like URLs, DOIs, etc.
* Linguistic Objects (:cidoc_entity:`E33<E33-Linguistic-Object>`) such as the
  content of a medieval charter)

In order to record which part of the document contains the respective reference
a delimiter respectively a certain value to determine the position in the
reference, is stored along with the link between the entities. This can be page
numbers of a book, chapters, figure numbers etc.

.. image:: references.png

::

   E31(Document) - P67(refers to) - E21(Person) at delimiter: "Folio 7v"

Example:
[Book of Kells (:cidoc_entity:`E31 Document<E31-Document>`)] refers to
(:cidoc_property:`P67<P67-refers-to>`) [Saint Mary
(:cidoc_entity:`21 Person<E21-Person>`)] at delimiter: "Folio 7v"

Each reference document is more or less unique and can refer to multiple
entities. The distinction is defined by the delimiter value. If the document as
a whole refers to the entity, no delimiter is necessary.

Reference Systems
-----------------

Referencers systems include sources such as vocabularies, gazetteers, etc.
They are considered authority documents
(:cidoc_entity:`E32<EE32-Authority-Document>`).

Users can define a reference system respectively authority document by defining
a name, class, and description.

Example:

* Name: `GeoNames<https://geonames.org/>`
* Class: :cidoc_entity:`E32<E32-Authority-Document>`
* Description: GeoNames - a geographical database - contains geographical
  information on all countries and the dataset includes over eleven million
  place names that are available for download free of charge.

OpenAtlas distinguishes between:

* Functional web resources, implemented via an API, etc.
* Non-digital respectively non-web-functional resources such as printed
  encyclopedia, card catalogs, inventory records, etc.

The link between an entity and the Authority Document is stored in the
model.link table in the following way:

* domain_id: ID of the Authority Document
* property_code: P67
* range_id: ID of the entity
* description: delimiter (alphanumeric)

This combination of :cidoc_entity:`E32<EE32-Authority-Document>` and delimiter
could furthermore be resolved as :cidoc_entity:`E31 Document<E31-Document>` as
it is a unique reference documenting the entity while the E32 alone is the
container for all possible references from this authority document.

.. image:: reference_system.png

::

   E21(Person) - P67i(is referred to by) - E31(Document) - P71(is listed in) E32(Authority Document)

Example:
[Terry Prattchet (:cidoc_entity:`21 Person<E21-Person>`)] is referred to by
(:cidoc_property:`P67i<P67-refers-to>`)
[`Q46248<https://www.wikidata.org/wiki/Q46248>`
(:cidoc_entity:`E31 Document<E31-Document>`)] is listed in
(:cidoc_property:`P71i<P71-lists>`)[`WikiData<https://www.wikidata.org/wiki/>`
(:cidoc_entity:`E32<EE32-Authority-Document>`)]


References and Files
--------------------

Various entities can be connected to files. This is mapped as:

:cidoc_entity:`E31<E31-Document>` (Document = file) - refers to
(:cidoc_property:`P67<P67-refers-to>`) - :cidoc_entity:`E1<E1-CRM-Entity>`

Files can refer to any of the "top level" entities and can
(but need not necessarily) be images. Files are stored with a certain
system type (i.e. file). If the file is an image, this is most probably a
depiction of the entity.

A file can also have a further reference - e.g. the source where the file comes
from. This can be a bibliographical reference to the publication
where a file (e.g. a scanned image) is extracted from. In this case there is a
link between a document :cidoc_entity:`E31<E31-Document>` with a type
"Bibliography" (or sub type) via :cidoc_property:`P67<P67-refers-to>` to
another document :cidoc_entity:`E31<E31-Document>` with a system type "file".
In this case the file is not the depiction of the reference but the reference
is the origin of the file. This is mostly needed to document the copyright
resp. right holder or source of the file.
