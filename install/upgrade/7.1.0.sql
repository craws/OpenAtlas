-- Upgrade 7.0.x to 7.1.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.1.0' WHERE name = 'database_version';

-- Fixing possible inconsistencies for source translation type
UPDATE web.hierarchy SET name = 'Source translation', category = 'standard' WHERE name IN ('Source Translation', 'Source translation');
UPDATE model.entity SET name = 'Source translation' WHERE name = 'Source Translation';

-- Deletes possible wrong links created because of bug #1634
DELETE FROM model.link WHERE id in (
    SELECT l.id FROM model.link l
    JOIN model.entity d ON l.domain_id = d.id AND d.openatlas_class_name = 'type'
    JOIN model.entity r ON l.range_id = r.id AND r.openatlas_class_name = 'type'
    WHERE l.property_code = 'P2'
);

-- Remove created, modified fields in model tables
ALTER TABLE model.cidoc_class DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
ALTER TABLE model.cidoc_class_inheritance DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
ALTER TABLE model.cidoc_class_i18n DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
ALTER TABLE model.property DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
ALTER TABLE model.property_inheritance DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
ALTER TABLE model.property_i18n DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
ALTER TABLE model.openatlas_class DROP COLUMN IF EXISTS created, DROP COLUMN IF EXISTS modified;
DROP TRIGGER IF EXISTS update_modified ON model.cidoc_class;
DROP TRIGGER IF EXISTS update_modified ON model.cidoc_class_inheritance;
DROP TRIGGER IF EXISTS update_modified ON model.cidoc_class_i18n;
DROP TRIGGER IF EXISTS update_modified ON model.property;
DROP TRIGGER IF EXISTS update_modified ON model.property_inheritance;
DROP TRIGGER IF EXISTS update_modified ON model.property_i18n;
DROP TRIGGER IF EXISTS update_modified ON model.openatlas_class;

--------------------------------------
-- #1506: Update CIDOC CRM to 7.1.1 --
--------------------------------------

-- Change sub/super event links
UPDATE model.link SET property_code = 'P9' WHERE property_code = 'P117';

-- Join appellation
UPDATE model.entity SET (cidoc_class_code, openatlas_class_name) = ('E41', 'appellation') WHERE cidoc_class_code = 'E82';
UPDATE model.link SET property_code = 'P1' WHERE property_code = 'P131';
DELETE FROM model.openatlas_class WHERE cidoc_class_code = 'E82';

-- Drop foreign keys of model tables (recreated below after CIDOC update)
ALTER TABLE model.entity DROP CONSTRAINT IF EXISTS entity_class_code_fkey;
ALTER TABLE model.entity DROP CONSTRAINT IF EXISTS entity_openatlas_class_name_fkey;
ALTER TABLE model.link DROP CONSTRAINT IF EXISTS link_property_code_fkey;
ALTER TABLE model.cidoc_class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_super_code_fkey;
ALTER TABLE model.cidoc_class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_sub_code_fkey;
ALTER TABLE model.cidoc_class_i18n DROP CONSTRAINT IF EXISTS class_i18n_class_code_fkey;
ALTER TABLE model.property DROP CONSTRAINT IF EXISTS property_domain_class_code_fkey;
ALTER TABLE model.property DROP CONSTRAINT IF EXISTS property_range_class_code_fkey;
ALTER TABLE model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_super_code_fkey;
ALTER TABLE model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_sub_code_fkey;
ALTER TABLE model.property_i18n DROP CONSTRAINT IF EXISTS property_i18n_property_code_fkey;
ALTER TABLE model.openatlas_class DROP CONSTRAINT IF EXISTS openatlas_class_cidoc_class_code_fkey;
ALTER TABLE web.reference_system_openatlas_class DROP CONSTRAINT IF EXISTS reference_system_openatlas_class_openatlas_class_name_fkey;

-- Remove former CIDOC
TRUNCATE model.cidoc_class_inheritance, model.cidoc_class_i18n, model.cidoc_class, model.property_inheritance, model.property_i18n, model.property RESTART IDENTITY;

-- Enter new CIDOC
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (1, 'E15', 'Identifier Assignment', 'This class comprises activities that result in the allocation of an identifier to an instance of E1 CRM Entity. Instances of E15 Identifier Assignment may include the creation of the identifier from multiple constituents, which themselves may be instances of E41 Appellation. The syntax and kinds of constituents to be used may be declared in a rule constituting an instance of E29 Design or Procedure.
Examples of such identifiers include Find Numbers, Inventory Numbers, uniform titles in the sense of librarianship and Digital Object Identifiers (DOI). Documenting the act of identifier assignment and deassignment is especially useful when objects change custody or the identification system of an organization is changed. In order to keep track of the identity of things in such cases, it is important to document by whom, when and for what purpose an identifier is assigned to an item.
The fact that an identifier is a preferred one for an organisation can be expressed by using the property E1 CRM Entity. P48 has preferred identifier (is preferred identifier of): E42 Identifier. It can better be expressed in a context independent form by assigning a suitable E55 Type, such as “preferred identifier assignment”, to the respective instance of E15 Identifier Assignment via the P2 has type property.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (2, 'E12', 'Production', 'This class comprises activities that are designed to, and succeed in, creating one or more new items.
It specializes the notion of modification into production. The decision as to whether or not an object is regarded as new is context sensitive. Normally, items are considered “new” if there is no obvious overall similarity between them and the consumed items and material used in their production. In other cases, an item is considered “new” because it becomes relevant to documentation by a modification. For example, the scribbling of a name on a potsherd may make it a voting token. The original potsherd may not be worth documenting, in contrast to the inscribed one.
This entity can be collective: the printing of a thousand books, for example, would normally be considered a single event.
An event should also be documented using an instance of E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities and matter is preserved, but identity is not.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (3, 'E39', 'Actor', 'This class comprises people, either individually or in groups, who have the potential to perform intentional actions of kinds for which someone may be held responsible.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (4, 'E7', 'Activity', 'This class comprises actions intentionally carried out by instances of E39 Actor that result in changes of state in the cultural, social, or physical systems documented.
This notion includes complex, composite and long-lasting actions such as the building of a settlement or a war, as well as simple, short-lived actions such as the opening of a door.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (5, 'E33', 'Linguistic Object', 'This class comprises identifiable expressions in natural language or languages.
Instances of E33 Linguistic Object can be expressed in many ways: e.g., as written texts, recorded speech or sign language. However, the CIDOC CRM treats instances of E33 Linguistic Object independently from the medium or method by which they are expressed. Expressions in formal languages, such as computer code or mathematical formulae, are not treated as instances of E33 Linguistic Object by the CIDOC CRM. These should be modelled as instances of E73 Information Object.
In general, an instance of E33 Linguistic Object may also contain non-linguistic information, often of artistic or aesthetic value. Only in cases in which the content of an instance of E33 Linguistic Object can completely be expressed by a series of binary-encoded symbols, its content may be documented within a respective knowledge base by the property P190 has symbolic content: E62 String. Otherwise, it should be understood as an identifiable digital resource only available independently from the respective knowledge base.
In other cases, such as pages of an illuminated manuscript or recordings containing speech in a language supported by a writing system, the linguistic part of the content of an instance of E33 Linguistic Object may be documented within a respective knowledge base in a note by P3 has note: E62 String. Otherwise, it may be described using the property P165 incorporates (is incorporated in): E73 Information Object as a different object with its own identity.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (6, 'E66', 'Formation', 'This class comprises events that result in the formation of a formal or informal E74 Group of people, such as a club, society, association, corporation or nation.
E66 Formation does not include the arbitrary aggregation of people who do not act as a collective.
The formation of an instance of E74 Group does not require that the group is populated with members at the time of formation. In order to express the joining of members at the time of formation, the respective activity should be simultaneously an instance of both E66 Formation and E85 Joining.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (7, 'E57', 'Material', 'This class is a specialization of E55 Type and comprises the concepts of materials.
Instances of E57 Material may denote properties of matter before its use, during its use, and as incorporated in an object, such as ultramarine powder, tempera paste, reinforced concrete. Discrete pieces of raw-materials kept in museums, such as bricks, sheets of fabric, pieces of metal, should be modelled individually in the same way as other objects. Discrete used or processed pieces, such as the stones from Nefer Titi''s temple, should be modelled as parts (cf. P46 is composed of (forms part of): E18 Physical Thing).
This type is used categorically in the model without reference to instances of it, i.e., the Model does not foresee the description of instances of instances of E57 Material, e.g.: “instances of gold”.
It is recommended that internationally or nationally agreed codes and terminology are used.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (14, 'E6', 'Destruction', 'This class comprises events that destroy one or more instances of E18 Physical Thing such that they lose their identity as the subjects of documentation.
Some destruction events are intentional, while others are independent of human activity. Intentional destruction may be documented by classifying the event as both an instance of E6 Destruction and of E7 Activity.
The decision to document an object as destroyed, transformed or modified is context sensitive:
1. If the matter remaining from the destruction is not documented, the event is modelled solely as an instance of E6 Destruction.
2. An event should also be documented as an instance of E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the original. In this case, the new items have separate identities. Matter is preserved, but identity is not.
3. When the initial identity of the changed instance of E18 Physical Thing is preserved, the event should be documented as an instance of E11 Modification.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (15, 'E20', 'Biological Object', 'This class comprises individual items of a material nature, which live, have lived or are natural products of or from living organisms.
Artificial objects that incorporate biological elements, such as Victorian butterfly frames, can be documented as both instances of E20 Biological Object and E22 Human-Made Object.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (8, 'E52', 'Time-Span', 'This class comprises abstract temporal extents, in the sense of Galilean physics, having a beginning, an end and a duration.
Instances of E52 Time-Span have no semantic connotations about phenomena happening within the temporal extent they represent. They do not convey any meaning other than a positioning on the “time-line” of chronology. The actual extent of an instance of E52 Time-Span can be approximated by properties of E52 Time-Span giving inner and outer bounds in the form of dates (instances of E61 Time Primitive). Comparing knowledge about time-spans is fundamental for chronological reasoning.
Some instances of E52 Time-Span may be defined as the actual, in principle observable, temporal extent of instances of E2 Temporal Entity via the property P4 has time-span (is time-span of): E52 Time-Span. They constitute phenomenal time-spans as defined in CRMgeo (Doerr &amp; Hiebel 2013). Since our knowledge of history is imperfect and physical phenomena are fuzzy in nature, the extent of phenomenal time-spans can only be described in approximation. An extreme case of approximation, might, for example, define an instance of E52 Time-Span having unknown beginning, end and duration. It may, nevertheless, be associated with other descriptions by which we can infer knowledge about it, such as in relative chronologies.
Some instances of E52 may be defined precisely as representing a declaration of a temporal extent, as, for instance, done in a business contract. They constitute declarative time-spans as defined in CRMgeo (Doerr &amp; Hiebel 2013) and can be described via the property E61 Time Primitive P170 defines time (time is defined by): E52 Time-Span.
When used as a common E52 Time-Span for two events, it will nevertheless describe them as being simultaneous, even if nothing else is known.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (9, 'E55', 'Type', 'This class comprises concepts denoted by terms from thesauri and controlled vocabularies used to characterize and classify instances of CIDOC CRM classes. Instances of E55 Type represent concepts in contrast to instances of E41 Appellation which are used to name instances of CIDOC CRM classes.
E55 Type is the CIDOC CRM’s interface to domain specific ontologies and thesauri. These can be represented in the CIDOC CRM as subclasses of E55 Type, forming hierarchies of terms, i.e., instances of E55 Type linked via P127 has broader term (has narrower term): E55 Type. Such hierarchies may be extended with additional properties.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (10, 'E3', 'Condition State', 'This class comprises the states of objects characterised by a certain condition over a time-span.
An instance of this class describes the prevailing physical condition of any material object or feature during a specific instance of E52 Time Span. In general, the time-span for which a certain condition can be asserted may be shorter than the real time-span, for which this condition held.
The nature of that condition can be described using P2 has type. For example, the instance of E3 Condition State “condition of the SS Great Britain between 22 September 1846 and 27 August 1847” can be characterized as an instance “wrecked” of E55 Type.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (11, 'E21', 'Person', 'This class comprises real persons who live or are assumed to have lived.
Legendary figures that may have existed, such as Ulysses and King Arthur, fall into this class if the documentation refers to them as historical figures. In cases where doubt exists as to whether several persons are in fact identical, multiple instances can be created and linked to indicate their relationship. The CIDOC CRM does not propose a specific form to support reasoning about possible identity.
In a bibliographic context, a name presented following the conventions usually employed for personal names will be assumed to correspond to an actual real person (an instance of E21 Person), unless evidence is available to indicate that this is not the case. The fact that a persona may erroneously be classified as an instance of E21 Person does not imply that the concept comprises personae.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (12, 'E10', 'Transfer of Custody', 'This class comprises transfers of the physical custody or the legal responsibility for the physical custody of objects. The recording of the donor or recipient is optional. It is possible that in an instance of E10 Transfer of Custody there is either no donor or no recipient.
Depending on the circumstances, it may describe:
1. the beginning of custody (there is no previous custodian)
2. the end of custody (there is no subsequent custodian)
3. the transfer of custody (transfer from one custodian to the next)
4. the receipt of custody from an unknown source (the previous custodian is unknown)
5. the declared loss of an object (the current or subsequent custodian is unknown)
In the event that only a single kind of transfer of custody occurs, either the legal responsibility for the custody or the actual physical possession of the object but not both, this difference should be expressed using the property P2 has type (is type of).
The sense of physical possession requires that the object of custody be in the hands of the keeper at least with a part representative for the whole. The way, in which a representative part is defined, should ensure that it is unambiguous who keeps a part and who the whole and should be consistent with the identity criteria of the kept instance of E18 Physical Thing.
The interpretation of the museum notion of "accession" differs between institutions. The CIDOC CRM therefore models legal ownership and physical custody separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.
Theft is a specific case of illegal transfer of custody.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (13, 'E5', 'Event', 'This class comprises distinct, delimited and coherent processes and interactions of a material nature, in cultural, social or physical systems, involving and affecting instances of E77 Persistent Item in a way characteristic of the kind of process. Typical examples are meetings, births, deaths, actions of decision taking, making or inventing things, but also more complex and extended ones such as conferences, elections, building of a castle, or battles.
While the continuous growth of a tree lacks the limits characteristic of an event, its germination from a seed does qualify as an event. Similarly, the blowing of the wind lacks the distinctness and limits of an event, but a hurricane, flood or earthquake would qualify as an event. Mental processes are considered as events, in cases where they are connected with the material externalization of their results; for example, the creation of a poem, a performance or a change of intention that becomes obvious from subsequent actions or declarations.
The effects of an instance of E5 Event may not lead to relevant permanent changes of properties or relations of the items involved in it, for example an unrecorded performance. Of course, in order to be documented, some kind of evidence for an event must exist, be it witnesses, traces or products of the event.
While instances of E4 Period always require some form of coherence between its constituent phenomena, in addition, the essential constituents of instances of E5 Event should contribute to an overall effect; for example, the statements made during a meeting and the listening of the audience.
Viewed at a coarse level of detail, an instance of E5 Event may appear as if it had an ‘instantaneous’ overall effect, but any process or interaction of material nature in reality have an extent in time and space. At a fine level, instances of E5 Event may be analyzed into component phenomena and phases within a space and timeframe, and as such can be seen as a period, regardless of the size of the phenomena. The reverse is not necessarily the case: not all instances of E4 Period give rise to a noteworthy overall effect and are thus not instances of E5 Event.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (16, 'E54', 'Dimension', 'This class comprises quantifiable properties that can be measured by some calibrated means and can be approximated by values, i.e., by points or regions in a mathematical or conceptual space, such as natural or real numbers, RGB values etc.
An instance of E54 Dimension represents the empirical or theoretically derived quantity, including the precision tolerances resulting from the particular method or calculation. The identity of an instance of E54 Dimension depends on the method of its determination because each method may produce different values even when determining comparable qualities. For instance, the wingspan of a bird alive or dead is a different dimension. Thermoluninescence dating and Rehydroxylation [RHX] dating are different dimensions of temporal distance from now, even if they aim at dating the same object. The method of determination should be expressed using the property P2 has type (is type of). Note that simple terms such as “diameter” or “length” are normally insufficient to unambiguously describe a respective dimension. In contrast, “maximum linear extent” may be sufficient.
The properties of the class E54 Dimension allow for expressing the numerical approximation of the values of instances of E54 Dimension adequate to the precision of the applied method of determination. If the respective quantity belongs to a non-discrete space according to the laws of physics, such as spatial distances, it is recommended to record them as approximations by intervals or regions of indeterminacy enclosing the assumed true values. For instance, a length of 5 cm may be recorded as 4.5-5.5 cm, according to the precision of the respective observation. Note, that comparability of values described in different units depends critically on the representation as value regions.
Numerical approximations in archaic instances of E58 Measurement Unit used in historical records should be preserved. Equivalents corresponding to current knowledge should be recorded as additional instances of E54 Dimension, as appropriate.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (17, 'E85', 'Joining', 'This class comprises the activities that result in an instance of E39 Actor becoming a member of an instance of E74 Group. This class does not imply initiative by either party. It may be the initiative of a third party.
Typical scenarios include becoming a member of a social organisation, becoming employee of a company, marriage, the adoption of a child by a family and the inauguration of somebody into an official position.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (18, 'E97', 'Monetary Amount', 'This class comprises quantities of monetary possessions or obligations in terms of their nominal value with respect to a particular currency. These quantities may be abstract accounting units, the nominal value of a heap of coins or bank notes at the time of validity of the respective currency, the nominal value of a bill of exchange or other documents expressing monetary claims or obligations. It specifically excludes amounts expressed in terms of weights of valuable items, like gold and diamonds, and quantities of other non-currency items, like goats or stocks and bonds.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (19, 'E30', 'Right', 'This class comprises legal privileges concerning material and immaterial things or their derivatives.
These include reproduction and property rights.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (20, 'E41', 'Appellation', 'This class comprises signs, either meaningful or not, or arrangements of signs following a specific syntax, that are used or can be used to refer to and identify a specific instance of some class or category within a certain context.
Instances of E41 Appellation do not identify things by their meaning, even if they happen to have one, but instead by convention, tradition, or agreement. Instances of E41 Appellation are cultural constructs; as such, they have a context, a history, and a use in time and space by some group of users. A given instance of E41 Appellation can have alternative forms, i.e., other instances of E41 Appellation that are always regarded as equivalent independent from the thing it denotes.
Different languages may use different appellations for the same thing, such as the names of major cities. Some appellations may be formulated using a valid noun phrase of a particular language. In these cases, the respective instances of E41 Appellation should also be declared as instances of E33 Linguistic Object. Then the language using the appellation can be declared with the property P72 has language: E56 Language.
Instances of E41 Appellation may be used to identify any instance of E1 CRM Entity and sometimes are characteristic for instances of more specific subclasses E1 CRM Entity, such as for instances of E52 Time-Span (for instance “dates”), E39 Actor, E53 Place or E28 Conceptual Object. Postal addresses and E-mail addresses are characteristic examples of identifiers used by services transporting things between clients.
Even numerically expressed identifiers for extents in space or time are also regarded as instances of E41 Appellation, such as Gregorian dates or spatial coordinates, even though they allow for determining some time or location by a known procedure starting from a reference point and by virtue of that fact play a double role as instances of E59 Primitive Value.
E41 Appellation should not be confused with the act of naming something. Cf. E15 Identifier Assignment');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (21, 'E9', 'Move', 'This class comprises changes of the physical location of the instances of E19 Physical Object.
Note, that the class E9 Move inherits the property P7 took place at (witnessed): E53 Place. This property should be used to describe the trajectory or a larger area within which a move takes place, whereas the properties P26 moved to (was destination of), P27 moved from (was origin of) describe the start and end points only. Moves may also be documented to consist of other moves (via P9 consists of (forms part of)), in order to describe intermediate stages on a trajectory. In that case, start and end points of the partial moves should match appropriately between each other and with the overall event.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (22, 'E31', 'Document', 'This class comprises identifiable immaterial items that make propositions about reality.
These propositions may be expressed in text, graphics, images, audiograms, videograms or by other similar means. Documentation databases are regarded as instances of E31 Document. This class should not be confused with the concept “document” in Information Technology, which is compatible with E73 Information Object.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (23, 'E8', 'Acquisition', 'This class comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor.
The class also applies to the establishment or loss of ownership of instances of E18 Physical Thing. It does not, however, imply changes of any other kinds of right. The recording of the donor and/or recipient is optional. It is possible that in an instance of E8 Acquisition there is either no donor or no recipient. Depending on the circumstances, it may describe:
1. the beginning of ownership
2. the end of ownership
3. the transfer of ownership
4. the acquisition from an unknown source
5. the loss of title due to destruction of the item
It may also describe events where a collector appropriates legal title, for example by annexation or field collection. The interpretation of the museum notion of "accession" differs between institutions. The CIDOC CRM therefore models legal ownership (E8 Acquisition) and physical custody (E10 Transfer of Custody) separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (24, 'E36', 'Visual Item', 'This class comprises the intellectual or conceptual aspects of recognisable marks, images and other visual works.
This class does not intend to describe the idiosyncratic characteristics of an individual physical embodiment of a visual item, but the underlying prototype. For example, a mark such as the ICOM logo is generally considered to be the same logo when used on any number of publications. The size, orientation and colour may change, but the logo remains uniquely identifiable. The same is true of images that are reproduced many times. This means that visual items are independent of their physical support.
The class E36 Visual Item provides a means of identifying and linking together instances of E24 Physical Human-Made Thing that carry the same visual qualities (symbols, marks or images etc.). The property P62 depicts (is depicted by) between E24 Physical Human-Made Thing and depicted subjects (E1 CRM Entity) is a shortcut of the more fully developed path from E24 Physical Human-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1CRM Entity, which in addition captures the optical features of the depiction.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (25, 'E11', 'Modification', 'This class comprises instances of E7 Activity that are undertaken to create, alter or change instances of E24 Physical Human-Made Thing.
This class includes the production of an item from raw materials and other so far undocumented objects. It also includes the conservation treatment of an object.
Since the distinction between modification and production is not always clear, modification is regarded as the more generally applicable concept. This implies that some items may be consumed or destroyed in an instance of E11 Modification, and that others may be produced as a result of it. An event should also be documented using an instance of E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities.
An activity undertaken on an object which was designed to alter it, but which, in fact, it did not in any seemingly significant way (such as the application of a solvent during conservation which failed to dissolve any part of the object), is still considered as an instance of E11 Modification. Typically, any such activity will leave at least forensic traces of evidence on the object.
If the instance of E29 Design or Procedure utilized for the modification prescribes the use of specific materials, they should be documented using property P68 foresees use of (use foreseen by): E57 Material of E29 Design or Procedure, rather than via P126 employed (was employed in): E57 Material.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (26, 'E16', 'Measurement', 'This class comprises actions measuring quantitative physical properties and other values that can be determined by a systematic, objective procedure of direct observation of particular states of physical reality.
An instance of E16 Measurement may us simple counting or tools, such as yardsticks or radiation detection devices. The interest is in the method and care applied, so that the reliability of the result may be judged at a later stage, or research continued on the associated documents. The date of the event is important for dimensions, which may change value over time, such as the length of an object subject to shrinkage. Methods and devices employed should be associated with instances of E16 Measurement by properties such as P33 used specific technique: E29 Design or Procedure, P125 used object of type: E55 Type, P16 used specific object (was used for): E70 Thing, whereas basic techniques such as "carbon 14 dating" should be encoded using P2 has type (is type of): E55 Type. Details of methods and devices reused or reusable in other instances of E16 Measurement should be documented for these entities rather than the measurements themselves, whereas details of particular execution may be documented by free text or by instantiating adequate sub-activities, if the detail may be of interest for an overarching query.
Regardless whether a measurement is made by an instrument or by human senses, it represents the initial transition from physical reality to information without any other documented information object in between within the reasoning chain that would represent the result of the interaction of the observer or device with reality. Therefore, determining properties of an instance of E90 Symbolic Object is regarded as an instance of E13 Attribute Assignment, which may be inferred from observing and measuring representative carriers. In the case that the carrier can be named, the property P16 used specific object (was used for): should be used to indicate the instance(s) of E18 Physical Thing that was used as the empirical basis for the attribute assignment. For instance, inferring properties of depicted items using image material, such as satellite images, is not regarded as an instance of E16 Measurement, but as a subsequent instance of E13 Attribute Assignment. Rather, only the production of the images, understood as arrays of radiation intensities, is regarded as an instance of E16 Measurement. The same reasoning holds for other sensor data.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (27, 'E89', 'Propositional Object', 'This class comprises immaterial items, including but not limited to stories, plots, procedural prescriptions, algorithms, laws of physics or images that are, or represent in some sense, sets of propositions about real or imaginary things and that are documented as single units or serve as topic of discourse.
This class also comprises items that are “about” something in the sense of a subject. In the wider sense, this class includes expressions of psychological value such as non-figural art and musical themes. However, conceptual items such as types and classes are not instances of E89 Propositional Object. This should not be confused with the definition of a type, which is indeed an instance of E89 Propositional Object.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (28, 'E18', 'Physical Thing', 'This class comprises all persistent physical items with a relatively stable form, human-made or natural.
Depending on the existence of natural boundaries of such things, the CIDOC CRM distinguishes the instances of E19 Physical Object from instances of E26 Physical Feature, such as holes, rivers, pieces of land etc. Most instances of E19 Physical Object can be moved (if not too heavy), whereas features are integral to the surrounding matter.
An instance of E18 Physical Thing occupies not only a particular geometric space at any instant of its existence, but in the course of its existence it also forms a trajectory through spacetime, which occupies a real, that is phenomenal, volume in spacetime. We include in the occupied space the space filled by the matter of the physical thing and all its inner spaces, such as the interior of a box. For the purpose of more detailed descriptions of the presence of an instance of E18 Physical Thing in space and time it can be associated with its specific instance of E92 Spacetime Volume by the property P196 defines (is defined by).
The CIDOC CRM is generally not concerned with amounts of matter in fluid or gaseous states, as long as they are not confined in an identifiable way for an identifiable minimal time-span.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (29, 'E14', 'Condition Assessment', 'This class describes the act of assessing the state of preservation of an object during a particular period.
The condition assessment may be carried out by inspection, measurement or through historical research. This class is used to document circumstances of the respective assessment that may be relevant to interpret its quality at a later stage, or to continue research on related documents.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (30, 'E1', 'CRM Entity', 'This class comprises all things in the universe of discourse of the CIDOC Conceptual Reference Model.
It is an abstract concept providing for three general properties:
Identification by name or appellation, and in particular by a preferred identifier
Classification by type, allowing further refinement of the specific subclass an instance belongs to
Attachment of free text and other unstructured data for the expression of anything not captured by formal properties
All other classes within the CIDOC CRM are directly or indirectly specialisations of E1 CRM Entity.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (31, 'E68', 'Dissolution', 'This class comprises the events that result in the formal or informal termination of an instance of E74 Group.
If the dissolution was deliberate, the Dissolution event should also be instantiated as an instance of E7 Activity.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (32, 'E64', 'End of Existence', 'This class comprises events that end the existence of any instance of E77 Persistent Item.
It may be used for temporal reasoning about things (physical items, groups of people, living beings) ceasing to exist; it serves as a hook for determination of a “terminus post quem” or “terminus ante quem”. In cases where substance from an instance of E64 Persistent Item continues to exist in a new form, the process would be documented as instances of E81 Transformation.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (33, 'E65', 'Creation', 'This class comprises events that result in the creation of conceptual items or immaterial products, such as legends, poems, texts, music, images, movies, laws, types etc.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (34, 'E63', 'Beginning of Existence', 'This class comprises events that bring into existence any instance of E77 Persistent Item.
It may be used for temporal reasoning about things (intellectual products, physical items, groups of people, living beings) beginning to exist; it serves as a hook for determination of a “terminus post quem” or “terminus ante quem”.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (35, 'E42', 'Identifier', 'This class comprises strings or codes assigned to instances of E1 CRM Entity in order to identify them uniquely and permanently within the context of one or more organisations. Such codes are often known as inventory numbers, registration codes, etc. and are typically composed of alphanumeric sequences. Postal addresses, telephone numbers, urls and e-mail addresses are characteristic examples of identifiers used by services transporting things between clients.
The class E42 Identifier is not normally used for machine-generated identifiers used for automated processing unless these are also used by human agents.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (36, 'E81', 'Transformation', 'This class comprises the events that result in the simultaneous destruction of one or more than one E18 Physical Thing and the creation of one or more than one E18 Physical Thing that preserves recognizable substance and structure from the first one(s) but has fundamentally different nature or identity.
Although the old and the new instances of E18 Physical Thing are treated as discrete entities having separate, unique identities, they are causally connected through the E81 Transformation; the destruction of the old E18 Physical Thing(s) directly causes the creation of the new one(s) using or preserving some relevant substance and structure. Instances of E81 Transformation are therefore distinct from re-classifications (documented using E17 Type Assignment) or modifications (documented using E11 Modification) of objects that do not fundamentally change their nature or identity. Characteristic cases are reconstructions and repurposing of historical buildings or ruins, fires leaving buildings in ruins, taxidermy of specimen in natural history.
Even though such instances of E81 Transformation are often motivated by a change of intended use, substantial material changes should justify the documentation of the result as a new instance of E18 Physical Thing and not just the change of function. The latter may be documented as an extended activity (instance of E7 Activity) of using it.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (37, 'E78', 'Curated Holding', 'This class comprises aggregations of instances of E18 Physical Thing that are assembled and maintained (“curated” and “preserved,” in museological terminology) by one or more instances of E39 Actor over time for a specific purpose and audience, and according to a particular collection development plan. Typical instances of curated holdings are museum collections, archives, library holdings and digital libraries. A digital library is regarded as an instance of E18 Physical Thing because it requires keeping physical carriers of the electronic content.
Items may be added or removed from an E78 Curated Holding in pursuit of this plan. This class should not be confused with the E39 Actor maintaining the E78 Curated Holding often referred to with the name of the E78 Curated Holding (e.g., “The Wallace Collection decided…”).
Collective objects in the general sense, like a tomb full of gifts, a folder with stamps or a set of chessmen, should be documented as instances of E19 Physical Object, and not as instances of E78 Curated Holding. This is because they form wholes either because they are physically bound together or because they are kept together for their functionality.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (38, 'E58', 'Measurement Unit', 'This class is a specialization of E55 Type and comprises the types of measurement units: feet, inches, centimetres, litres, lumens, etc.
This type is used categorically in the model without reference to instances of it, i.e., the Model does not foresee the description of instances of instances of E58 Measurement Unit, e.g.: “instances of cm”.
Système International (SI) units or internationally recognized non-SI terms should be used whenever possible, such as those defined by ISO80000:2009. Archaic Measurement Units used in historical records should be preserved.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (39, 'E2', 'Temporal Entity', 'This class comprises all phenomena, such as the instances of E4 Periods and E5 Events, which happen over a limited extent in time. This extent in time must be contiguous, i.e., without gaps. In case the defining kinds of phenomena for an instance of E2 Temporal Entity cease to happen, and occur later again at another time, we regard that the former instance of E2 Temporal Entity has ended and a new instance has come into existence. In more intuitive terms, the same event cannot happen twice.
In some contexts, such phenomena are also called perdurants. This class is disjoint from E77 Persistent Item and is an abstract class that typically has no direct instances. E2 Temporal Entity is specialized into E4 Period, which applies to a particular geographic area (defined with a greater or lesser degree of precision), and E3 Condition State, which applies to instances of E18 Physical Thing.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (40, 'E17', 'Type Assignment', 'This class comprises the actions of classifying items of whatever kind. Such items include objects, specimens, people, actions and concepts.
This class allows for the documentation of the context of classification acts in cases where the value of the classification depends on the personal opinion of the classifier, and the date that the classification was made. This class also encompasses the notion of "determination," i.e., the systematic and molecular identification of a specimen in biology.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (41, 'E53', 'Place', 'This class comprises extents in space, in particular on the surface of the earth, in the pure sense of physics: independent from temporal phenomena and matter.
The instances of E53 Place are usually determined by reference to the position of “immobile” objects such as buildings, cities, mountains, rivers, or dedicated geodetic marks, but may also be determined by reference to mobile objects. A Place can be determined by combining a frame of reference and a location with respect to this frame.
It is sometimes argued that instances of E53 Place are best identified by global coordinates or absolute reference systems. However, relative references are often more relevant in the context of cultural documentation and tend to be more precise. In particular, we are often interested in position in relation to large, mobile objects, such as ships. For example, the Place at which Nelson died is known with reference to a large mobile object – H.M.S Victory. A resolution of this Place in terms of absolute coordinates would require knowledge of the movements of the vessel and the precise time of death, either of which may be revised, and the result would lack historical and cultural relevance.
Any instance of E18 Physical Thing can serve as a frame of reference for an instance of E53 Place. This may be documented using the property P157 is at rest relative to (provides reference space for).');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (67, 'E87', 'Curation Activity', 'This class comprises the activities that result in the continuity of management and the preservation and evolution of instances of E78 Curated Holding, following an implicit or explicit curation plan.
It specializes the notion of activity into the curation of a collection and allows the history of curation to be recorded.
Items are accumulated and organized following criteria like subject, chronological period, material type, style of art etc. and can be added or removed from an instance of E78 Curated Holding for a specific purpose and/or audience. The initial aggregation of items of a collection is regarded as an instance of E12 Production Event while the activity of evolving, preserving and promoting a collection is regarded as an instance of E87 Curation Activity.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (42, 'E26', 'Physical Feature', 'This class comprises identifiable features that are physically attached in an integral way to particular physical objects.
Instances of E26 Physical Feature share many of the attributes of instances of E19 Physical Object. They may have a one-, two- or three-dimensional geometric extent, but there are no natural borders that separate them completely in an objective way from the carrier objects. For example, a doorway is a feature but the door itself, being attached by hinges, is not.
Instances of E26 Physical Feature can be features in a narrower sense, such as scratches, holes, reliefs, surface colours, reflection zones in an opal crystal or a density change in a piece of wood. In the wider sense, they are portions of particular objects with partially imaginary borders, such as the core of the Earth, an area of property on the surface of the Earth, a landscape or the head of a contiguous marble statue. They can be measured and dated, and it is sometimes possible to state who or what is or was responsible for them. They cannot be separated from the carrier object, but a segment of the carrier object may be identified (or sometimes removed) carrying the complete feature.
This definition coincides with the definition of "fiat objects" (Smith &amp; Varzi, 2000, pp.401-420), with the exception of aggregates of “bona fide objects”.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (43, 'E28', 'Conceptual Object', 'This class comprises non-material products of our minds and other human produced data that have become objects of a discourse about their identity, circumstances of creation or historical implication. The production of such information may have been supported by the use of technical devices such as cameras or computers.
Characteristically, instances of this class are created, invented or thought by someone, and then may be documented or communicated between persons. Instances of E28 Conceptual Object have the ability to exist on more than one particular carrier at the same time, such as paper, electronic signals, marks, audio media, paintings, photos, human memories, etc.
They cannot be destroyed. They exist as long as they can be found on at least one carrier or in at least one human memory. Their existence ends when the last carrier and the last memory are lost.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (44, 'E19', 'Physical Object', 'This class comprises items of a material nature that are units for documentation and have physical boundaries that separate them completely in an objective way from other objects.
The class also includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen. Typically, instances of E19 Physical Object can be moved (if not too heavy).
In some contexts, such objects, except for aggregates, are also called “bona fide objects” (Smith &amp; Varzi, 2000, pp.401-420), i.e., naturally defined objects.
The decision as to what is documented as a complete item, rather than by its parts or components, may be a purely administrative decision or may be a result of the order in which the item was acquired.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (45, 'E70', 'Thing', 'This general class comprises discrete, identifiable, instances of E77 Persistent Item that are documented as single units, that either consist of matter or depend on being carried by matter and are characterized by relative stability.
They may be intellectual products or physical things. They may for instance have a solid physical form, an electronic encoding, or they may be a logical concept or structure.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (46, 'E77', 'Persistent Item', 'This class comprises items that have persistent characteristics of structural nature substantially related to their identity and their integrity, sometimes known as “endurants” in philosophy. Persistent Items may be physical entities, such as people, animals or things, conceptual entities such as ideas, concepts, products of the imagination or even names.
Instances of E77 Persistent Item may be present or be part of interactions in different periods or events. They can repeatedly be recognized at disparate occasions during their existence by characteristics of structural nature. The respective characteristics need not be exactly the same during all the existence of an instance of E77 Persistent Item. Often, they undergo gradual change, still bearing some similarities with that of previous times, or disappear completely and new emerge. For instance, a person, from the time of being born on, will gradually change all its features and acquire new ones, such as a scar. Even the DNA in different body cells will develop defects and mutations. Nevertheless, relevant characteristics use to be sufficiently similar to recognize the instance for some substantial period of time.
The more specific criteria that determine the identity of instances of subclasses of E77 Persistent Item may vary considerably and are described of referred to in the respective scope notes. The decision about which exact criteria to use depends on whether the observable behaviour of the respective part of reality such confined conforms to the reasoning the user is interested in. For example, a building can be regarded as no longer existing if it is dismantled and the materials reused in a different configuration. On the other hand, human beings go through radical and profound changes during their life-span, affecting both material composition and form, yet preserve their identity by other criteria, such as being bodily separated from other persons. Similarly, inanimate objects may be subject to exchange of parts and matter. On the opposite, the identity of a (version of a) text of a scientific publication is given by the exact arrangement of its relevant symbols.
The main classes of objects that fall outside the scope of the E77 Persistent Item class are temporal objects such as periods, events and acts, and descriptive properties.
An instance of E77 Persistent Item does not require actual knowledge of the identifying features of the instance being currently known. There may be cases, where the actual identifying features of an instance of E77 Persistent Item are not decidable at a particular state of knowledge.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (47, 'E98', 'Currency', 'This class comprises the units in which a monetary system, supported by an administrative authority or other community, quantifies and arithmetically compares all monetary amounts declared in the unit. The unit of a monetary system must describe a nominal value which is kept constant by its administrative authority and an associated banking system if it exists, and not by market value. For instance, one may pay with grams of gold, but the respective monetary amount would have been agreed as the gold price in US dollars on the day of the payment. Under this definition, British Pounds, U.S. Dollars, and European Euros are examples of currency, but “grams of gold” is not. One monetary system has one and only one currency. Instances of this class must not be confused with coin denominations, such as “Dime” or “Sestertius”. Non-monetary exchange of value in terms of quantities of a particular type of goods, such as cows, do not constitute a currency.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (48, 'E27', 'Site', 'This class comprises pieces of land or sea floor.
In contrast to the purely geometric notion of E53 Place, this class describes constellations of matter on the surface of the Earth or other celestial body, which can be represented by photographs, paintings and maps.
Instances of E27 Site are composed of relatively immobile material items and features in a particular configuration at a particular location.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (49, 'E35', 'Title', 'This class comprises textual strings that within a cultural context can be clearly identified as titles due to their form. Being a subclass of E41 Appellation, E35 Title can only be used when such a string is actually used as a title of a work, such as a text, an artwork, or a piece of music.
Titles are proper noun phrases or verbal phrases, and should not be confused with generic object names such as “chair”, “painting” or “book” (the latter are common nouns that stand for instances of E55 Type). Titles may be assigned by the creator of the work itself, or by a social group.
This class also comprises the translations of titles that are used as surrogates for the original titles in different social contexts.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (50, 'E29', 'Design or Procedure', 'This class comprises documented plans for the execution of actions in order to achieve a result of a specific quality, form or contents. In particular, it comprises plans for deliberate human activities that may result in new instances of E71 Human-Made Thing or for shaping or guiding the execution of an instance of E7 Activity.
Instances of E29 Design or Procedure can be structured in parts and sequences or depend on others.
This is modelled using P69 has association with (is associated with): E29 Design or Procedure.
Designs or procedures can be seen as one of the following
1. A schema for the activities it describes
2. A schema of the products that result from their application.
3. An independent intellectual product that may have never been applied, such as Leonardo da Vinci’s famous plans for flying machines.
Because designs or procedures may never be applied or only partially executed, the CIDOC CRM models a loose relationship between the plan and the respective product.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (51, 'E83', 'Type Creation', 'This class comprises activities formally defining new types of items.
It is typically a rigorous scholarly or scientific process that ensures a type is exhaustively described and appropriately named. In some cases, particularly in archaeology and the life sciences, E83 Type Creation requires the identification of an exemplary specimen and the publication of the type definition in an appropriate scholarly forum. The activity modelled as an instance of E83 Type Creation is central to research in the life sciences, where a type would be referred to as a “taxon,” the type description as a “protologue,” and the exemplary specimens as “original element” or “holotype”.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (52, 'E74', 'Group', 'This class comprises any gatherings or organizations of human individuals or groups that act collectively or in a similar way due to any form of unifying relationship. In the wider sense this class also comprises official positions which used to be regarded in certain contexts as one actor, independent of the current holder of the office, such as the president of a country. In such cases, it may happen that the group never had more than one member. A joint pseudonym (i.e., a name that seems indicative of an individual but that is actually used as a persona by two or more people) is a particular case of E74 Group.
A gathering of people becomes an instance of E74 Group when it exhibits organizational characteristics usually typified by a set of ideas or beliefs held in common, or actions performed together. These might be communication, creating some common artifact, a common purpose such as study, worship, business, sports, etc. Nationality can be modelled as membership in an instance of E74 Group. Married couples and other concepts of family are regarded as particular examples of E74 Group.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (53, 'E25', 'Human-Made Feature', 'This class comprises physical features that are purposely created by human activity, such as scratches, artificial caves, artificial water channels, etc. In particular, it includes the information encoding features on mechanical or digital carriers.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (54, 'E22', 'Human-Made Object', 'This class comprises all persistent physical objects of any size that are purposely created by human activity and have physical boundaries that separate them completely in an objective way from other objects.
The class also includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (55, 'E72', 'Legal Object', 'This class comprises those material or immaterial items to which instances of E30 Right, such as the right of ownership or use, can be applied.
This is true for all instances of E18 Physical Thing. In the case of instances of E28 Conceptual Object, however, the identity of an instance of E28 Conceptual Object or the method of its use may be too ambiguous to reliably establish instances of E30 Right, as in the case of taxa and inspirations. Ownership of corporations is currently regarded as out of scope of the CIDOC CRM.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (56, 'E32', 'Authority Document', 'This class comprises encyclopaedia, thesauri, authority lists and other documents that define terminology or conceptual systems for consistent use.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (57, 'E34', 'Inscription', 'This class comprises recognisable, texts attached to instances of E24 Physical Human-Made Thing.
The transcription of the text can be documented in a note by P3 has note: E62 String. The alphabet used can be documented by P2 has type: E55 Type. This class does not intend to describe the idiosyncratic characteristics of an individual physical embodiment of an inscription, but the underlying prototype. The physical embodiment is modelled in the CIDOC CRM as instances of E24 Physical Human-Made Thing.
The relationship of a physical copy of a book to the text it contains is modelled using E18 Physical Thing. P128 carries (is carried by): E33 Linguistic Object.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (58, 'E80', 'Part Removal', 'This class comprises the activities that result in an instance of E18 Physical Thing being decreased by the removal of a part.
Typical scenarios include the detachment of an accessory, the removal of a component or part of a composite object, or the deaccessioning of an object from a curated collection, an instance of E78 Curated Holding. If the instance of E80 Part Removal results in the total decomposition of the original object into pieces, such that the whole ceases to exist, the activity should instead be modelled as an instance of E81 Transformation, i.e., a simultaneous destruction and production. In cases where the part removed has no discernible identity prior to its removal but does have an identity subsequent to its removal, the activity should be modelled as both an instance of E80 Part Removal and E12 Production. This class of activities forms a basis for reasoning about the history, and continuity of identity over time, of objects that are removed from other objects, such as precious gemstones being extracted from different items of jewellry, or cultural artifacts being deaccessioned from different museum collections over their lifespan.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (59, 'E56', 'Language', 'This class is a specialization of E55 Type and comprises the natural languages in the sense of concepts.
This type is used categorically in the model without reference to instances of it, i.e., the Model does not foresee the description of instances of instances of E56 Language, e.g.: “instances of Mandarin Chinese”.
It is recommended that internationally or nationally agreed codes and terminology are used to denote instances of E56 Language, such as those defined in ISO 639-1:2002 and later versions.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (60, 'E79', 'Part Addition', 'This class comprises activities that result in an instance of E24 Physical Human-Made Thing being increased, enlarged or augmented by the addition of a part.
Typical scenarios include the attachment of an accessory, the integration of a component, the addition of an element to an aggregate object, or the accessioning of an object into a curated instance of E78 Curated Holding. Objects to which parts are added are, by definition, human-made, since the addition of a part implies a human activity. Following the addition of parts, the resulting human-made assemblages are treated objectively as single identifiable wholes, made up of constituent or component parts bound together either physically (for example the engine becoming a part of the car), or by sharing a common purpose (such as the 32 chess pieces that make up a chess set). This class of activities forms a basis for reasoning about the history and continuity of identity of objects that are integrated into other objects over time, such as precious gemstones being repeatedly incorporated into different items of jewellery, or cultural artifacts being added to different museum instances of E78 Curated Holding over their lifespan.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (61, 'E13', 'Attribute Assignment', 'This class comprises the actions of making assertions about one property of an object or any single relation between two items or concepts. The type of the property asserted to hold between two items or concepts can be described by the property P177 assigned property type: E55 Type.
For example, the class describes the actions of people making propositions and statements during certain scientific/scholarly procedures, e.g., the person and date when a condition statement was made, an identifier was assigned, the museum object was measured, etc. Which kinds of such assignments and statements need to be documented explicitly in structures of a schema rather than free text, depends on whether this information should be accessible by structured queries.
This class allows for the documentation of how the respective assignment came about, and whose opinion it was. Note that all instances of properties described in a knowledge base are the opinion of someone. Per default, they are the opinion of the team maintaining the knowledge base. This fact must not individually be registered for all instances of properties provided by the maintaining team, because it would result in an endless recursion of whose opinion was the description of an opinion. Therefore, the use of instances of E13 Attribute Assignment marks the fact, that the maintaining team is in general neutral to the validity of the respective assertion, but registers someone else’s opinion and how it came about.
All properties assigned in such an action can also be seen as directly relating the respective pair of items or concepts. Multiple use of instances of E13 Attribute Assignment may possibly lead to a collection of contradictory values.
All cases of properties in this model that are also described indirectly through a subclass of E13 Attribute Assignment are characterised as "short cuts" of a path via this subclass. This redundant modelling of two alternative views is preferred because many implementations may have good reasons to model either the action of assertion or the short cut, and the relation between both alternatives can be captured by simple rules.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (62, 'E37', 'Mark', 'This class comprises symbols, signs, signatures or short texts applied to instances of E24 Physical Human-Made Thing by arbitrary techniques, often in order to indicate such things as creator, owner, dedications, purpose or to communicate information generally. Instances of E37 Mark do not represent the actual image of a mark, but the abstract ideal (or archetype) as used for codification in reference documents forming cultural documentation.
This class specifically excludes features that have no semantic significance, such as scratches or tool marks. These should be documented as instances of E25 Human-Made Feature.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (63, 'E90', 'Symbolic Object', 'This class comprises identifiable symbols and any aggregation of symbols, such as characters, identifiers, traffic signs, emblems, texts, data sets, images, musical scores, multimedia objects, computer program code or mathematical formulae that have an objectively recognizable structure and that are documented as single units.
It includes sets of signs of any nature, which may serve to designate something, or to communicate some propositional content. An instance of E90 Symbolic Object may or may not have a specific meaning, for example an arbitrary character string.
In some cases, the content of an instance of E90 Symbolic Object may completely be represented by a serialized digital content model, such as a sequence of ASCII-encoded characters, an XML or HTML document, or a TIFF image. The property P3 has note and its subproperty P190 has symbolic content allow for the description of this content model. In order to disambiguate which symbolic level is the carrier of the meaning, the property P3.1 has type can be used to specify the encoding (e.g., "bit", "Latin character", RGB pixel).');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (64, 'E86', 'Leaving', 'This class comprises the activities that result in an instance of E39 Actor to be disassociated from an instance of E74 Group. This class does not imply initiative by either party. It may be the initiative of a third party.
Typical scenarios include the termination of membership in a social organisation, ending the employment at a company, divorce, and the end of tenure of somebody in an official position.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (65, 'E24', 'Physical Human-Made Thing', 'This class comprises all persistent physical items of any size that are purposely created by human activity. This class comprises, besides others, Human-Made objects, such as a sword, and Human-Made features, such as rock art. For example, a “cup and ring” carving on bedrock is regarded as instance of E24 Physical Human-Made Thing.
Instances of Human-Made thing may be the result of modifying pre-existing physical things, preserving larger parts or most of the original matter and structure, which poses the question if they are new or even Human-Made, the respective interventions of production made on such original material should be obvious and sufficient to regard that the product has a new, distinct identity and intended function and is human-made. Substantial continuity of the previous matter and structure in the new product can be documented by describing the production process also as an instance of E81 Transformation.
Whereas interventions of conservation and repair are not regarded to produce a new Human-Made thing, the results of preparation of natural history specimens that substantially change their natural or original state should be regarded as physical Human-Made things, including the uncovering of petrified biological features from a solid piece of stone. On the other side, scribbling a museum number on a natural object should not be regarded to make it Human-Made. This notwithstanding, parts, sections, segments, or features of a physical Human-Made thing may continue to be non-Human-Made and preserved during the production process, for example natural pearls used as a part of an eardrop.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (66, 'E93', 'Presence', 'This class comprises instances of E92 Spacetime Volume, whose temporal extent has been chosen in order to determine the spatial extent of a phenomenon over the chosen time-span. Respective phenomena may, for instance, be historical events or periods, but can also be the diachronic extent and existence of physical things. In other words, instances of this class fix a slice of another instance of E92 Spacetime Volume in time.
The temporal extent of an instance of E93 Presence typically is predetermined by the researcher so as to focus the investigation particularly on finding the spatial extent of the phenomenon by testing for its characteristic features. There are at least two basic directions such investigations might take. The investigation may wish to determine where something was during some time or it may wish to reconstruct the total passage of a phenomenon’s spacetime volume through an examination of discrete presences. Observation and measurement of features indicating the presence or absence of a phenomenon in some space allows for the progressive approximation of spatial extents through argumentation typically based on inclusion, exclusion and various overlaps.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (68, 'E96', 'Purchase', 'This class comprises transfers of legal ownership from one or more instances of E39 Actor to one or more different instances of E39 Actor, where the transferring party is completely compensated by the payment of a monetary amount. In more detail, a purchase agreement establishes a fixed monetary obligation at its initialization on the receiving party, to the giving party. An instance of E96 Purchase begins with the contract or equivalent agreement and ends with the fulfilment of all contractual obligations. In the case that the activity is abandoned before both parties have fulfilled these obligations, the activity is not regarded as an instance of E96 Purchase.
This class is a very specific case of the much more complex social business practices of exchange of goods and the creation and satisfaction of related social obligations. Purchase activities which define individual sales prices per object can be modelled by instantiating E96 Purchase for each object individually and as part of an overall instance of E96 Purchase transaction.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (69, 'E4', 'Period', 'This class comprises sets of coherent phenomena or cultural manifestations occurring in time and space.
It is the social or physical coherence of these phenomena that identify an instance of E4 Period and not the associated spatiotemporal extent. This extent is only the “ground” or space in an abstract physical sense that the actual process of growth, spread and retreat has covered. Consequently, different periods can overlap and coexist in time and space, such as when a nomadic culture exists in the same area and time as a sedentary culture. This also means that overlapping land use rights, common among first nations, amounts to overlapping periods.
Often, this class is used to describe prehistoric or historic periods such as the “Neolithic Period”, the “Ming Dynasty” or the “McCarthy Era”, but also geopolitical units and activities of settlements are regarded as special cases of E4 Period. However, there are no assumptions about the scale of the associated phenomena. In particular all events are seen as synthetic processes consisting of coherent phenomena. Therefore, E4 Period is a superclass of E5 Event. For example, a modern clinical birth, an instance of E67 Birth, can be seen as both a single event, i.e., an instance of E5 Event, and as an extended period, i.e., an instance of E4 Period, that consists of multiple physical processes and complementary activities performed by multiple instances of E39 Actor.
As the actual extent of an instance of E4 Period in spacetime we regard the trajectories of the participating physical things during their participation in an instance of E4 Period. This includes the open spaces via which these things have interacted and the spaces by which they had the potential to interact during that period or event in the way defined by the type of the respective period or event. Examples include the air in a meeting room transferring the voices of the participants. Since these phenomena are fuzzy, we assume the spatiotemporal extent to be contiguous, except for cases of phenomena spreading out over islands or other separated areas, including geopolitical units distributed over disconnected areas such as islands or colonies.
Whether the trajectories necessary for participants to travel between these areas are regarded as part of the spatiotemporal extent or not has to be decided in each case based on a concrete analysis, taking use of the sea for other purposes than travel, such as fishing, into consideration. One may also argue that the activities to govern disconnected areas imply travelling through spaces connecting them and that these areas hence are spatially connected in a way, but it appears counterintuitive to consider for instance travel routes in international waters as extensions of geopolitical units.
Consequently, an instance of E4 Period may occupy a number of disjoint spacetime volumes, however there must not be a discontinuity in the timespan covered by these spacetime volumes. This means that an instance of E4 Period must be contiguous in time. If it has ended in all areas, it has ended as a whole. However, it may end in one area before another, such as in the Polynesian migration, and it continues as long as it is ongoing in at least one area.
We model E4 Period as a subclass of E2 Temporal Entity and of E92 Spacetime Volume. The latter is intended as a phenomenal spacetime volume as defined in CIDOC CRMgeo (Doerr &amp; Hiebel, 2013). By virtue of this multiple inheritance, we can discuss the physical extent of an instance of E4 Period without representing each instance of it together with an instance of its associated spacetime volume. This model combines two quite different kinds of substance: an instance of E4 Period is a phenomenon while an instance of E92 Spacetime Volume is an aggregation of points in spacetime. However, the real spatiotemporal extent of an instance of E4 Period is regarded to be unique to it due to all its details and fuzziness; its identity and existence depends uniquely on the identity of the instance of E4 Period. Therefore, this multiple inheritance is unambiguous and effective and furthermore corresponds to the intuitions of natural language.
Typical use of this class in cultural heritage documentation is for documenting cultural and artistic periods. There are two different conceptualisations of ‘artistic style’, defined either by physical features or by historical context. For example, “Impressionism” can be viewed as a period in the European sphere of influence lasting from approximately 1870 to 1905 during which paintings with particular characteristics were produced by a group of artists that included (among others) Monet, Renoir, Pissarro, Sisley and Degas. Alternatively, it can be regarded as a style applicable to all paintings sharing the characteristics of the works produced by the Impressionist painters, regardless of historical context. The first interpretation is an instance of E4 Period, and the second defines morphological object types that fall under E55 Type.
A geopolitical unit as a specific case of an instance of E4 Period is the set of activities and phenomena related to the claim of power, the consequences of belonging to a jurisdictional area and an administrative system that establishes a geopolitical unit. Examples from the modern period are countries or administrative areas of countries such as districts whose actions and structures define activities and phenomena in the area that they intend to govern. The borders of geopolitical units are often defined in contracts or treaties although they may deviate from the actual practice. The spatiotemporal properties of Geopolitical units can be modelled through the properties inherited from E92 Spacetime Volume.
Another specific case of an instance of E4 Period is the actual extent of the set of activities and phenomena as evidenced by their physical traces that define a settlement, such as the populated period of Nineveh.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (70, 'E73', 'Information Object', 'This class comprises identifiable immaterial items, such as poems, jokes, data sets, images, texts, multimedia objects, procedural prescriptions, computer program code, algorithm or mathematical formulae, that have an objectively recognizable structure and are documented as single units. The encoding structure known as a "named graph" also falls under this class, so that each "named graph" is an instance of E73 Information Object.
An instance of E73 Information Object does not depend on a specific physical carrier, which can include human memory, and it can exist on one or more carriers simultaneously.
Instances of E73 Information Object of a linguistic nature should be declared as instances of the E33 Linguistic Object subclass. Instances of E73 Information Object of a documentary nature should be declared as instances of the E31 Document subclass. Conceptual items such as types and classes are not instances of E73 Information Object, nor are ideas without a reproducible expression.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (71, 'E99', 'Product Type', 'This classes comprises types that stand as the models for instances of E22 Human-Made Object that are produced as the result of production activities using plans exact enough to result in one or more series of uniform, functionally and aesthetically identical and interchangeable items. The product type is the intended ideal form of the manufacture process. It is typical of instances of E22 that conform to an instance of E99 Product Type that its component parts are interchangeable with component parts of other instances of E22 made after the model of the same instance of E99. Frequently, the uniform production according to a given instance of E99 Product Type is achieved by creating individual tools, such as moulds or print plates that are themselves carriers of the design of the product type. Modern tools may use the flexibility of electronically controlled devices to achieve such uniformity. The product type itself, i.e., the potentially unlimited series of aesthetically equivalent items, may be the target of artistic design, rather than the individual object. In extreme cases, only one instance of a product type may have been produced, such as in a "print on demand" process which was only triggered once. However, this should not be confused with industrial prototypes, such as car prototypes, which are produced prior to the production line being set up, or test the production line itself.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (72, 'E71', 'Human-Made Thing', 'This class comprises discrete, identifiable human-made items that are documented as single units.
These items are either intellectual products or human-made physical things, and are characterized by relative stability. They may for instance have a solid physical form, an electronic encoding, or they may be logical concepts or structures.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (73, 'E67', 'Birth', 'This class comprises the births of human beings. E67 Birth is a biological event focussing on the context of people coming into life. (E63 Beginning of Existence comprises the coming into life of any living being).
Twins, triplets etc. are typically brought into life by the same instance of E67 Birth. The introduction of E67 Birth as a documentation element allows the description of a range of family relationships in a simple model. Suitable extensions may describe more details and the complexity of motherhood with the intervention of modern medicine. In this model, the biological father is not seen as a necessary participant in the birth.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (74, 'E92', 'Spacetime Volume', 'This class comprises 4-dimensional point sets (volumes) in physical spacetime (in contrast to mathematical models of it) regardless their true geometric forms. They may derive their identity from being the extent of a material phenomenon or from being the interpretation of an expression defining an extent in spacetime. Intersections of instances of E92 Spacetime Volume, E53 Place and E52 Timespan are also regarded as instances of E92 Spacetime Volume. An instance of E92 Spacetime Volume is either contiguous or composed of a finite number of contiguous subsets. Its boundaries may be fuzzy due to the properties of the phenomena it derives from or due to the limited precision up to which defining expression can be identified with a real extent in spacetime. The duration of existence of an instance of E92 Spacetime Volume is its projection on time.');
INSERT INTO model.cidoc_class (id, code, name, comment) VALUES (75, 'E69', 'Death', 'This class comprises the deaths of human beings.
If a person is killed, the death should be documented as an instance of both E69 Death and E7 Activity. The death or perishing of other living beings should be documented as instances of E64 End of Existence.');

INSERT INTO model.cidoc_class_inheritance (id, super_code, sub_code) VALUES
	(1, 'E13', 'E15'),
	(2, 'E63', 'E12'),
	(3, 'E11', 'E12'),
	(4, 'E77', 'E39'),
	(5, 'E5', 'E7'),
	(6, 'E73', 'E33'),
	(8, 'E41', 'E33'),
	(9, 'E7', 'E66'),
	(10, 'E63', 'E66'),
	(11, 'E55', 'E57'),
	(12, 'E1', 'E52'),
	(13, 'E28', 'E55'),
	(14, 'E2', 'E3'),
	(15, 'E20', 'E21'),
	(16, 'E39', 'E21'),
	(17, 'E7', 'E10'),
	(18, 'E4', 'E5'),
	(19, 'E64', 'E6'),
	(20, 'E19', 'E20'),
	(21, 'E1', 'E54'),
	(22, 'E7', 'E85'),
	(23, 'E54', 'E97'),
	(24, 'E89', 'E30'),
	(25, 'E90', 'E41'),
	(26, 'E7', 'E9'),
	(27, 'E73', 'E31'),
	(28, 'E7', 'E8'),
	(29, 'E73', 'E36'),
	(30, 'E7', 'E11'),
	(31, 'E13', 'E16'),
	(32, 'E28', 'E89'),
	(33, 'E72', 'E18'),
	(34, 'E13', 'E14'),
	(35, 'E64', 'E68'),
	(36, 'E5', 'E64'),
	(37, 'E63', 'E65'),
	(38, 'E7', 'E65'),
	(39, 'E5', 'E63'),
	(40, 'E41', 'E42'),
	(41, 'E63', 'E81'),
	(42, 'E64', 'E81'),
	(43, 'E24', 'E78'),
	(44, 'E55', 'E58'),
	(45, 'E1', 'E2'),
	(46, 'E13', 'E17'),
	(47, 'E1', 'E53'),
	(48, 'E18', 'E26'),
	(49, 'E71', 'E28'),
	(50, 'E18', 'E19'),
	(51, 'E77', 'E70'),
	(52, 'E1', 'E77'),
	(53, 'E58', 'E98'),
	(54, 'E26', 'E27'),
	(55, 'E33', 'E35'),
	(56, 'E41', 'E35'),
	(57, 'E73', 'E29'),
	(58, 'E65', 'E83'),
	(59, 'E39', 'E74'),
	(60, 'E26', 'E25'),
	(61, 'E24', 'E25'),
	(62, 'E19', 'E22'),
	(63, 'E24', 'E22'),
	(64, 'E70', 'E72'),
	(65, 'E31', 'E32'),
	(66, 'E37', 'E34'),
	(67, 'E33', 'E34'),
	(68, 'E11', 'E80'),
	(69, 'E55', 'E56'),
	(70, 'E11', 'E79'),
	(71, 'E7', 'E13'),
	(72, 'E36', 'E37'),
	(73, 'E28', 'E90'),
	(74, 'E72', 'E90'),
	(75, 'E7', 'E86'),
	(76, 'E18', 'E24'),
	(77, 'E71', 'E24'),
	(78, 'E92', 'E93'),
	(79, 'E7', 'E87'),
	(80, 'E8', 'E96'),
	(81, 'E2', 'E4'),
	(82, 'E92', 'E4'),
	(83, 'E90', 'E73'),
	(84, 'E89', 'E73'),
	(85, 'E55', 'E99'),
	(86, 'E70', 'E71'),
	(87, 'E63', 'E67'),
	(88, 'E1', 'E92'),
	(89, 'E64', 'E69');

INSERT INTO model.cidoc_class_i18n (id, class_code, language_code, text) VALUES
	(1, 'E15', 'de', 'Kennzeichenzuweisung'),
	(2, 'E15', 'en', 'Identifier Assignment'),
	(3, 'E15', 'fr', 'Attribution d’identificateur'),
	(4, 'E15', 'ru', 'Назначение Идентификатора'),
	(5, 'E15', 'el', 'Απόδοση Αναγνωριστικού'),
	(6, 'E15', 'pt', 'Atribuição de Identificador'),
	(7, 'E15', 'zh', '标识符赋值'),
	(8, 'E12', 'de', 'Herstellung'),
	(9, 'E12', 'en', 'Production'),
	(10, 'E12', 'fr', 'Production'),
	(11, 'E12', 'ru', 'Событие Производства'),
	(12, 'E12', 'el', 'Παραγωγή'),
	(13, 'E12', 'pt', 'Produção'),
	(14, 'E12', 'zh', '生产'),
	(15, 'E39', 'de', 'Akteur'),
	(16, 'E39', 'en', 'Actor'),
	(17, 'E39', 'fr', 'Agent'),
	(18, 'E39', 'ru', 'Агент'),
	(19, 'E39', 'el', 'Δράστης'),
	(20, 'E39', 'pt', 'Agente'),
	(21, 'E39', 'zh', '参与者'),
	(22, 'E7', 'de', 'Handlung'),
	(23, 'E7', 'en', 'Activity'),
	(24, 'E7', 'fr', 'Activité'),
	(25, 'E7', 'ru', 'Деятельность'),
	(26, 'E7', 'el', 'Δράση'),
	(27, 'E7', 'pt', 'Atividade'),
	(28, 'E7', 'zh', '活动'),
	(29, 'E33', 'de', 'Sprachlicher Gegenstand'),
	(30, 'E33', 'en', 'Linguistic Object'),
	(31, 'E33', 'fr', 'Objet linguistique'),
	(32, 'E33', 'ru', 'Линвистический Объект'),
	(33, 'E33', 'el', 'Γλωσσικό Αντικείμενο'),
	(34, 'E33', 'pt', 'Objeto Lingüístico'),
	(35, 'E33', 'zh', '语言对象'),
	(36, 'E66', 'de', 'Gruppenbildung'),
	(37, 'E66', 'en', 'Formation'),
	(38, 'E66', 'fr', 'Formation'),
	(39, 'E66', 'ru', 'Событие Формирования'),
	(40, 'E66', 'el', 'Συγκρότηση Ομάδας'),
	(41, 'E66', 'pt', 'Formação'),
	(42, 'E66', 'zh', '组成'),
	(43, 'E57', 'de', 'Material'),
	(44, 'E57', 'en', 'Material'),
	(45, 'E57', 'fr', 'Matériau'),
	(46, 'E57', 'ru', 'Материал'),
	(47, 'E57', 'el', 'Υλικό'),
	(48, 'E57', 'pt', 'Material'),
	(49, 'E57', 'zh', '材质'),
	(50, 'E52', 'de', 'Zeitspanne'),
	(51, 'E52', 'en', 'Time-Span'),
	(52, 'E52', 'fr', 'Durée'),
	(53, 'E52', 'ru', 'Интервал Времени'),
	(54, 'E52', 'el', 'Χρονικό Διάστημα'),
	(55, 'E52', 'pt', 'Período de Tempo'),
	(56, 'E52', 'zh', '时段'),
	(57, 'E55', 'de', 'Typus'),
	(58, 'E55', 'en', 'Type'),
	(59, 'E55', 'fr', 'Type'),
	(60, 'E55', 'ru', 'Тип'),
	(61, 'E55', 'el', 'Τύπος'),
	(62, 'E55', 'pt', 'Tipo'),
	(63, 'E55', 'zh', '类型'),
	(64, 'E3', 'de', 'Zustandsphase'),
	(65, 'E3', 'en', 'Condition State'),
	(66, 'E3', 'fr', 'État matériel'),
	(67, 'E3', 'ru', 'Состояние'),
	(68, 'E3', 'el', 'Κατάσταση'),
	(69, 'E3', 'pt', 'Estado Material'),
	(70, 'E3', 'zh', '条件状态'),
	(71, 'E21', 'de', 'Person'),
	(72, 'E21', 'en', 'Person'),
	(73, 'E21', 'fr', 'Personne'),
	(74, 'E21', 'ru', 'Личность'),
	(75, 'E21', 'el', 'Πρόσωπο'),
	(76, 'E21', 'pt', 'Pessoa'),
	(77, 'E21', 'zh', '人物'),
	(78, 'E10', 'de', 'Übertragung des Gewahrsams'),
	(79, 'E10', 'en', 'Transfer of Custody'),
	(80, 'E10', 'fr', 'Changement de détenteur'),
	(81, 'E10', 'ru', 'Передача Опеки'),
	(82, 'E10', 'el', 'Μεταβίβαση Κατοχής'),
	(83, 'E10', 'pt', 'Transferência de Custódia'),
	(84, 'E10', 'zh', '转移监护权'),
	(85, 'E5', 'de', 'Ereignis'),
	(86, 'E5', 'en', 'Event'),
	(87, 'E5', 'fr', 'Événement'),
	(88, 'E5', 'ru', 'Событие'),
	(89, 'E5', 'el', 'Συμβάν'),
	(90, 'E5', 'pt', 'Evento'),
	(91, 'E5', 'zh', '事件'),
	(92, 'E6', 'de', 'Zerstörung'),
	(93, 'E6', 'en', 'Destruction'),
	(94, 'E6', 'fr', 'Destruction'),
	(95, 'E6', 'ru', 'Разрушение'),
	(96, 'E6', 'el', 'Καταστροφή'),
	(97, 'E6', 'pt', 'Destruição'),
	(98, 'E6', 'zh', '破坏'),
	(99, 'E20', 'de', 'Biologischer Gegenstand'),
	(100, 'E20', 'en', 'Biological Object'),
	(101, 'E20', 'fr', 'Objet biologique'),
	(102, 'E20', 'ru', 'Биологический Объект'),
	(103, 'E20', 'el', 'Βιολογικό Ακτικείμενο'),
	(104, 'E20', 'pt', 'Objeto Biológico'),
	(105, 'E20', 'zh', '生物对象'),
	(106, 'E54', 'de', 'Maß'),
	(107, 'E54', 'en', 'Dimension'),
	(108, 'E54', 'fr', 'Dimensions'),
	(109, 'E54', 'ru', 'Величина'),
	(110, 'E54', 'el', 'Μέγεθος'),
	(111, 'E54', 'pt', 'Dimensão'),
	(112, 'E54', 'zh', '度量规格'),
	(113, 'E85', 'de', 'Beitritt'),
	(114, 'E85', 'en', 'Joining'),
	(115, 'E85', 'zh', '加入'),
	(116, 'E97', 'en', 'Monetary Amount'),
	(117, 'E30', 'de', 'Recht'),
	(118, 'E30', 'en', 'Right'),
	(119, 'E30', 'fr', 'Droit'),
	(120, 'E30', 'ru', 'Право'),
	(121, 'E30', 'el', 'Δικαίωμα'),
	(122, 'E30', 'pt', 'Direitos'),
	(123, 'E30', 'zh', '权限'),
	(124, 'E41', 'de', 'Benennung'),
	(125, 'E41', 'en', 'Appellation'),
	(126, 'E41', 'fr', 'Appellation'),
	(127, 'E41', 'ru', 'Обозначение'),
	(128, 'E41', 'el', 'Ονομασία'),
	(129, 'E41', 'pt', 'Designação'),
	(130, 'E41', 'zh', '称谓'),
	(131, 'E9', 'de', 'Objektbewegung'),
	(132, 'E9', 'en', 'Move'),
	(133, 'E9', 'fr', 'Déplacement'),
	(134, 'E9', 'ru', 'Перемещение'),
	(135, 'E9', 'el', 'Μετακίνηση'),
	(136, 'E9', 'pt', 'Locomoção'),
	(137, 'E9', 'zh', '移动'),
	(138, 'E31', 'de', 'Dokument'),
	(139, 'E31', 'en', 'Document'),
	(140, 'E31', 'fr', 'Document'),
	(141, 'E31', 'ru', 'Документ'),
	(142, 'E31', 'el', 'Τεκμήριο'),
	(143, 'E31', 'pt', 'Documento'),
	(144, 'E31', 'zh', '文献'),
	(145, 'E8', 'de', 'Erwerb'),
	(146, 'E8', 'en', 'Acquisition'),
	(147, 'E8', 'fr', 'Acquisition'),
	(148, 'E8', 'ru', 'Событие Приобретения'),
	(149, 'E8', 'el', 'Απόκτηση'),
	(150, 'E8', 'pt', 'Aquisição'),
	(151, 'E8', 'zh', '采访'),
	(152, 'E36', 'de', 'Bildliches'),
	(153, 'E36', 'en', 'Visual Item'),
	(154, 'E36', 'fr', 'Item visuel'),
	(155, 'E36', 'ru', 'Визуальный Предмет'),
	(156, 'E36', 'el', 'Οπτικό Στοιχείο'),
	(157, 'E36', 'pt', 'Item Visual'),
	(158, 'E36', 'zh', '可视项'),
	(159, 'E11', 'de', 'Bearbeitung'),
	(160, 'E11', 'en', 'Modification'),
	(161, 'E11', 'fr', 'Modification'),
	(162, 'E11', 'ru', 'Событие Изменения'),
	(163, 'E11', 'el', 'Τροποποίηση'),
	(164, 'E11', 'pt', 'Modificação'),
	(165, 'E11', 'zh', '修改'),
	(166, 'E16', 'de', 'Messung'),
	(167, 'E16', 'en', 'Measurement'),
	(168, 'E16', 'fr', 'Mesurage'),
	(169, 'E16', 'ru', 'Событие Измерения'),
	(170, 'E16', 'el', 'Μέτρηση'),
	(171, 'E16', 'pt', 'Medição'),
	(172, 'E16', 'zh', '测量'),
	(173, 'E89', 'de', 'Aussagenobjekt'),
	(174, 'E89', 'en', 'Propositional Object'),
	(175, 'E89', 'zh', '命题对象'),
	(176, 'E18', 'de', 'Materielles'),
	(177, 'E18', 'en', 'Physical Thing'),
	(178, 'E18', 'fr', 'Chose matérielle'),
	(179, 'E18', 'ru', 'Физическая Вещь'),
	(180, 'E18', 'el', 'Υλικό Πράγμα'),
	(181, 'E18', 'pt', 'Coisa Material'),
	(182, 'E18', 'zh', '实物'),
	(183, 'E14', 'de', 'Zustandsfeststellung'),
	(184, 'E14', 'en', 'Condition Assessment'),
	(185, 'E14', 'fr', 'Expertise de l''état matériel'),
	(186, 'E14', 'ru', 'Оценка Состояния'),
	(187, 'E14', 'el', 'Εκτίμηση Κατάστασης'),
	(188, 'E14', 'pt', 'Avaliação do Estado Material'),
	(189, 'E14', 'zh', '状态评估'),
	(190, 'E1', 'de', 'CRM Entität'),
	(191, 'E1', 'en', 'CRM Entity'),
	(192, 'E1', 'fr', 'Entité CRM'),
	(193, 'E1', 'ru', 'CRM Сущность'),
	(194, 'E1', 'el', 'Οντότητα CIDOC CRM'),
	(195, 'E1', 'pt', 'Entidade CRM'),
	(196, 'E1', 'zh', 'CRM实体'),
	(197, 'E68', 'de', 'Gruppenauflösung'),
	(198, 'E68', 'en', 'Dissolution'),
	(199, 'E68', 'fr', 'Dissolution'),
	(200, 'E68', 'ru', 'Роспуск'),
	(201, 'E68', 'el', 'Διάλυση Ομάδας'),
	(202, 'E68', 'pt', 'Dissolução'),
	(203, 'E68', 'zh', '解散'),
	(204, 'E64', 'de', 'Daseinsende'),
	(205, 'E64', 'en', 'End of Existence'),
	(206, 'E64', 'fr', 'Fin d''existence'),
	(207, 'E64', 'ru', 'Конец Существования'),
	(208, 'E64', 'el', 'Τέλος Ύπαρξης'),
	(209, 'E64', 'pt', 'Fim da Existência'),
	(210, 'E64', 'zh', '结束'),
	(211, 'E65', 'de', 'Begriffliche Schöpfung'),
	(212, 'E65', 'en', 'Creation'),
	(213, 'E65', 'fr', 'Création'),
	(214, 'E65', 'ru', 'Событие Творения'),
	(215, 'E65', 'el', 'Δημιουργία'),
	(216, 'E65', 'pt', 'Criação'),
	(217, 'E65', 'zh', '创建'),
	(218, 'E63', 'de', 'Daseinsbeginn'),
	(219, 'E63', 'en', 'Beginning of Existence'),
	(220, 'E63', 'fr', 'Début d''existence'),
	(221, 'E63', 'ru', 'Начало Существования'),
	(222, 'E63', 'el', 'Αρχή Ύπαρξης'),
	(223, 'E63', 'pt', 'Início da Existência'),
	(224, 'E63', 'zh', '初始'),
	(225, 'E42', 'de', 'Kennung'),
	(226, 'E42', 'en', 'Identifier'),
	(227, 'E42', 'fr', 'Identificateur d''objet'),
	(228, 'E42', 'ru', 'Идентификатор Объекта'),
	(229, 'E42', 'el', 'Κωδικός Αναγνώρισης'),
	(230, 'E42', 'pt', 'Identificador de Objeto'),
	(231, 'E42', 'zh', '标识符'),
	(232, 'E81', 'de', 'Umwandlung'),
	(233, 'E81', 'en', 'Transformation'),
	(234, 'E81', 'fr', 'Transformation'),
	(235, 'E81', 'ru', 'Трансформация'),
	(236, 'E81', 'el', 'Μετατροπή'),
	(237, 'E81', 'pt', 'Transformação'),
	(238, 'E81', 'zh', '转变'),
	(239, 'E78', 'en', 'Curated Holding'),
	(240, 'E58', 'de', 'Maßeinheit'),
	(241, 'E58', 'en', 'Measurement Unit'),
	(242, 'E58', 'fr', 'Unité de mesure'),
	(243, 'E58', 'ru', 'Единица Измерения'),
	(244, 'E58', 'el', 'Μονάδα Μέτρησης'),
	(245, 'E58', 'pt', 'Unidade de Medida'),
	(246, 'E58', 'zh', '测量单位'),
	(247, 'E2', 'de', 'Geschehendes'),
	(248, 'E2', 'en', 'Temporal Entity'),
	(249, 'E2', 'fr', 'Entité temporelle'),
	(250, 'E2', 'ru', 'Временная Сущность'),
	(251, 'E2', 'el', 'Έγχρονη Οντότητα'),
	(252, 'E2', 'pt', 'Entidade Temporal'),
	(253, 'E2', 'zh', '时序实体'),
	(254, 'E17', 'de', 'Typuszuweisung'),
	(255, 'E17', 'en', 'Type Assignment'),
	(256, 'E17', 'fr', 'Attribution de type'),
	(257, 'E17', 'ru', 'Присвоение Типа'),
	(258, 'E17', 'el', 'Απόδοση Τύπου'),
	(259, 'E17', 'pt', 'Atribuição de Tipo'),
	(260, 'E17', 'zh', '类型赋值'),
	(261, 'E53', 'de', 'Ort'),
	(262, 'E53', 'en', 'Place'),
	(263, 'E53', 'fr', 'Lieu'),
	(264, 'E53', 'ru', 'Место'),
	(265, 'E53', 'el', 'Τόπος'),
	(266, 'E53', 'pt', 'Local'),
	(267, 'E53', 'zh', '地点'),
	(268, 'E26', 'de', 'Materielles Merkmal'),
	(269, 'E26', 'en', 'Physical Feature'),
	(270, 'E26', 'fr', 'Caractéristique matérielle'),
	(271, 'E26', 'ru', 'Физический Признак'),
	(272, 'E26', 'el', 'Υλικό Μόρφωμα'),
	(273, 'E26', 'pt', 'Característica Material'),
	(274, 'E26', 'zh', '物理特征'),
	(275, 'E28', 'de', 'Begrifflicher Gegenstand'),
	(276, 'E28', 'en', 'Conceptual Object'),
	(277, 'E28', 'fr', 'Objet conceptuel'),
	(278, 'E28', 'ru', 'Концептуальный Объект'),
	(279, 'E28', 'el', 'Νοητικό Αντικείμενο'),
	(280, 'E28', 'pt', 'Objeto Conceitual'),
	(281, 'E28', 'zh', '概念对象'),
	(282, 'E19', 'de', 'Materieller Gegenstand'),
	(283, 'E19', 'en', 'Physical Object'),
	(284, 'E19', 'fr', 'Objet matériel'),
	(285, 'E19', 'ru', 'Физический Объект'),
	(286, 'E19', 'el', 'Υλικό Αντικείμενο'),
	(287, 'E19', 'pt', 'Objeto Material'),
	(288, 'E19', 'zh', '物质对象'),
	(289, 'E70', 'de', 'Sache'),
	(290, 'E70', 'en', 'Thing'),
	(291, 'E70', 'fr', 'Chose'),
	(292, 'E70', 'ru', 'Вещь'),
	(293, 'E70', 'el', 'Πράγμα'),
	(294, 'E70', 'pt', 'Coisa'),
	(295, 'E70', 'zh', '事物'),
	(296, 'E77', 'de', 'Seiendes'),
	(297, 'E77', 'en', 'Persistent Item'),
	(298, 'E77', 'fr', 'Entité persistante'),
	(299, 'E77', 'ru', 'Постоянная Сущность'),
	(300, 'E77', 'el', 'Ον'),
	(301, 'E77', 'pt', 'Entidade Persistente'),
	(302, 'E77', 'zh', '持久项'),
	(303, 'E98', 'en', 'Currency'),
	(304, 'E27', 'de', 'Gelände'),
	(305, 'E27', 'en', 'Site'),
	(306, 'E27', 'fr', 'Site'),
	(307, 'E27', 'ru', 'Участок'),
	(308, 'E27', 'el', 'Φυσικός Χώρος'),
	(309, 'E27', 'pt', 'Lugar'),
	(310, 'E27', 'zh', '场地'),
	(311, 'E35', 'de', 'Titel'),
	(312, 'E35', 'en', 'Title'),
	(313, 'E35', 'fr', 'Titre'),
	(314, 'E35', 'ru', 'Заголовок'),
	(315, 'E35', 'el', 'Τίτλος'),
	(316, 'E35', 'pt', 'Título'),
	(317, 'E35', 'zh', '题名'),
	(318, 'E29', 'de', 'Entwurf oder Verfahren'),
	(319, 'E29', 'en', 'Design or Procedure'),
	(320, 'E29', 'fr', 'Conception ou procédure'),
	(321, 'E29', 'ru', 'Проект или Процедура'),
	(322, 'E29', 'el', 'Σχέδιο'),
	(323, 'E29', 'pt', 'Projeto ou Procedimento'),
	(324, 'E29', 'zh', '设计或程序'),
	(325, 'E83', 'de', 'Typuserfindung'),
	(326, 'E83', 'en', 'Type Creation'),
	(327, 'E83', 'fr', 'Création de type'),
	(328, 'E83', 'ru', 'Создание Типа'),
	(329, 'E83', 'el', 'Δημιουργία Τύπου'),
	(330, 'E83', 'pt', 'Criação de Tipo'),
	(331, 'E83', 'zh', '类型创建'),
	(332, 'E74', 'de', 'Menschliche Gruppe'),
	(333, 'E74', 'en', 'Group'),
	(334, 'E74', 'fr', 'Groupe'),
	(335, 'E74', 'ru', 'Группа'),
	(336, 'E74', 'el', 'Ομάδα'),
	(337, 'E74', 'pt', 'Grupo'),
	(338, 'E74', 'zh', '团体'),
	(339, 'E25', 'en', 'Human-Made Feature'),
	(340, 'E22', 'en', 'Human-Made Object'),
	(341, 'E72', 'de', 'Rechtsobjekt'),
	(342, 'E72', 'en', 'Legal Object'),
	(343, 'E72', 'fr', 'Objet juridique'),
	(344, 'E72', 'ru', 'Объект Права'),
	(345, 'E72', 'el', 'Νομικό Αντικείμενο'),
	(346, 'E72', 'pt', 'Objeto Jurídico'),
	(347, 'E72', 'zh', '法律对象'),
	(348, 'E32', 'de', 'Referenzdokument'),
	(349, 'E32', 'en', 'Authority Document'),
	(350, 'E32', 'fr', 'Document de référence'),
	(351, 'E32', 'ru', 'Официальный Документ'),
	(352, 'E32', 'el', 'Πηγή Καθιερωμένων Όρων'),
	(353, 'E32', 'pt', 'Documento de Referência'),
	(354, 'E32', 'zh', '规范文档'),
	(355, 'E34', 'de', 'Inschrift'),
	(356, 'E34', 'en', 'Inscription'),
	(357, 'E34', 'fr', 'Inscription'),
	(358, 'E34', 'ru', 'Надпись'),
	(359, 'E34', 'el', 'Επιγραφή'),
	(360, 'E34', 'pt', 'Inscrição'),
	(361, 'E34', 'zh', '题识'),
	(362, 'E80', 'de', 'Teilentfernung'),
	(363, 'E80', 'en', 'Part Removal'),
	(364, 'E80', 'fr', 'Soustraction d''élément'),
	(365, 'E80', 'ru', 'Удаление Части'),
	(366, 'E80', 'el', 'Αφαίρεση Μερών'),
	(367, 'E80', 'pt', 'Remoção de Parte'),
	(368, 'E80', 'zh', '部分去除'),
	(369, 'E56', 'de', 'Sprache'),
	(370, 'E56', 'en', 'Language'),
	(371, 'E56', 'fr', 'Langue'),
	(372, 'E56', 'ru', 'Язык'),
	(373, 'E56', 'el', 'Γλώσσα'),
	(374, 'E56', 'pt', 'Língua'),
	(375, 'E56', 'zh', '语种'),
	(376, 'E79', 'de', 'Teilhinzufügung'),
	(377, 'E79', 'en', 'Part Addition'),
	(378, 'E79', 'fr', 'Addition d''élément'),
	(379, 'E79', 'ru', 'Добавление Части'),
	(380, 'E79', 'el', 'Προσθήκη Μερών'),
	(381, 'E79', 'pt', 'Adição de Parte'),
	(382, 'E79', 'zh', '部分增加'),
	(383, 'E13', 'de', 'Merkmalszuweisung'),
	(384, 'E13', 'en', 'Attribute Assignment'),
	(385, 'E13', 'fr', 'Affectation d''attribut'),
	(386, 'E13', 'ru', 'Присвоение Атрибута'),
	(387, 'E13', 'el', 'Απόδοση Ιδιοτήτων'),
	(388, 'E13', 'pt', 'Atribuição de Característica'),
	(389, 'E13', 'zh', '属性赋值'),
	(390, 'E37', 'de', 'Marke'),
	(391, 'E37', 'en', 'Mark'),
	(392, 'E37', 'fr', 'Marque'),
	(393, 'E37', 'ru', 'Пометка'),
	(394, 'E37', 'el', 'Σήμανση'),
	(395, 'E37', 'pt', 'Marca'),
	(396, 'E37', 'zh', '标记'),
	(397, 'E90', 'de', 'Symbolisches Objekt'),
	(398, 'E90', 'en', 'Symbolic Object'),
	(399, 'E90', 'zh', '符号对象'),
	(400, 'E86', 'de', 'Austritt'),
	(401, 'E86', 'en', 'Leaving'),
	(402, 'E86', 'zh', '离开'),
	(403, 'E24', 'en', 'Physical Human-Made Thing'),
	(404, 'E93', 'en', 'Presence'),
	(405, 'E87', 'de', 'Kuratorische Tätigkeit'),
	(406, 'E87', 'en', 'Curation Activity'),
	(407, 'E87', 'zh', '管理'),
	(408, 'E96', 'en', 'Purchase'),
	(409, 'E4', 'de', 'Phase'),
	(410, 'E4', 'en', 'Period'),
	(411, 'E4', 'fr', 'Période'),
	(412, 'E4', 'ru', 'Период'),
	(413, 'E4', 'el', 'Περίοδος'),
	(414, 'E4', 'pt', 'Período'),
	(415, 'E4', 'zh', '时期'),
	(416, 'E73', 'de', 'Informationsgegenstand'),
	(417, 'E73', 'en', 'Information Object'),
	(418, 'E73', 'fr', 'Objet d''information'),
	(419, 'E73', 'ru', 'Информационный Объект'),
	(420, 'E73', 'el', 'Πληροφοριακό Αντικείμενο'),
	(421, 'E73', 'pt', 'Objeto de Informação'),
	(422, 'E73', 'zh', '信息对象'),
	(423, 'E99', 'en', 'Product Type'),
	(424, 'E71', 'en', 'Human-Made Thing'),
	(425, 'E67', 'de', 'Geburt'),
	(426, 'E67', 'en', 'Birth'),
	(427, 'E67', 'fr', 'Naissance'),
	(428, 'E67', 'ru', 'Рождение'),
	(429, 'E67', 'el', 'Γέννηση'),
	(430, 'E67', 'pt', 'Nascimento'),
	(431, 'E67', 'zh', '出生'),
	(432, 'E92', 'en', 'Spacetime Volume'),
	(433, 'E69', 'de', 'Tod'),
	(434, 'E69', 'en', 'Death'),
	(435, 'E69', 'fr', 'Mort'),
	(436, 'E69', 'ru', 'Смерть'),
	(437, 'E69', 'el', 'Θάνατος'),
	(438, 'E69', 'pt', 'Morte'),
	(439, 'E69', 'zh', '死亡');

INSERT INTO model.property (id, code, range_class_code, domain_class_code, name, name_inverse, comment) VALUES
	(1, 'P92', 'E77', 'E63', 'brought into existence', 'was brought into existence by', 'This property links an instance of E63 Beginning of Existence to the instance of E77 Persistent Item brought into existence by it.
It allows a “start” to be attached to any instance of E77 Persistent Item being documented, i.e., as instances of E70 Thing, E72 Legal Object, E39 Actor, E41 Appellation and E55 Type.'),
	(2, 'P101', 'E55', 'E70', 'had as general use', 'was use of', 'This property associates an instance of E70 Thing with an instance of E55 Type that describes the type of use that it was actually employed for.
It allows the relationship between particular things, both physical and immaterial, and the general methods and techniques of real use to be documented. This may well be different from the intended functional purpose of the instance of E70 Thing (which can be documented with P103 was intended for (was intention of)). For example, it could be recorded that a particular wooden crate had a general use as a shelf support on a market stall even though it had been originally intended for carrying vegetables.
The use of this property is intended to allow the documentation of usage patterns attested in historical records or through scientific investigation (for instance ceramic residue analysis). It should not be used to document the intended, and thus assumed, use of an object.'),
	(3, 'P46', 'E18', 'E18', 'is composed of', 'forms part of', 'This property associates an instance of E18 Physical Thing with another instance of Physical Thing that forms part of it. The spatial extent of the composing part is included in the spatial extent of the whole.
Component elements, since they are themselves instances of E18 Physical Thing, may be further analysed into sub-components, thereby creating a hierarchy of part decomposition. An instance of E18 Physical Thing may be shared between multiple wholes, for example two buildings may share a common wall. This property does not specify when and for how long a component element resided in the respective whole. If a component is not part of a whole from the beginning of existence or until the end of existence of the whole, the classes E79 Part Addition and E90 Part Removal can be used to document when a component became part of a particular whole and/or when it stopped being a part of it. For the time-span of being part of the respective whole, the component is completely contained in the place the whole occupies.
This property is intended to describe specific components that are individually documented, rather than general aspects. Overall descriptions of the structure of an instance of E18 Physical Thing are captured by the P3 has note property.
The instances of E57 Material of which an instance of E18 Physical Thing is composed should be documented using P45 consists of (is incorporated in).
This property is transitive and non-reflexive'),
	(4, 'P29', 'E39', 'E10', 'custody received by', 'received custody through', 'This property identifies the instance(s) E39 Actor who receive custody of an instance of E18 Physical Thing in an instance of E10 Transfer of Custody.
The property will typically describe Actors receiving custody of an object when it is handed over from another Actor’s care. On occasion, physical custody may be received involuntarily or illegally – through accident, unsolicited donation, or theft.
In reality, custody is either transferred to someone or from someone, or both.'),
	(5, 'P55', 'E53', 'E19', 'has current location', 'currently holds', 'This property records the location of an instance of E19 Physical Object at the time of validity of the record or database containing the statement that uses this property.
This property is a specialisation of P53 has former or current location (is former or current location of). It indicates that the instance of E53 Place associated with the instance of E19 Physical Object is the current location of the object. The property does not allow any indication of how long the object has been at the current location.
This property is a shortcut. A more detailed representation can make use of the fully developed (i.e., indirect) path from E19 Physical Object, through, P25i moved by, E9 Move, P26 moved to to E53 Place if and only if this Move is the most recent.'),
	(6, 'P141', 'E1', 'E13', 'assigned', 'was assigned by', 'This property associates an instance of E13 Attribute Assignment with the instance of E1 CRM Entity used in the attribution. The instance of E1 CRM Entity here plays the role of the range of the attribution.
The kind of attribution made should be documented using P177 assigned property type.'),
	(7, 'P25', 'E19', 'E9', 'moved', 'moved by', 'This property identifies an instance of E19 Physical Object that was moved by an instance of E9 Move. A move must concern at least one object.
The property implies the object’s passive participation. For example, Monet’s painting “Impression sunrise” was moved for the first Impressionist exhibition in 1874.'),
	(8, 'P39', 'E18', 'E16', 'measured', 'was measured by', 'This property associates an instance of E16 Measurement with the instance of E18 Physical Thing upon which it acted. The instance of E16 Measurement is specific to the measured object. An instance of E18 Physical Thing may be measured more than once with different results, constituting different instances of E16 Measurement.'),
	(9, 'P183', 'E2', 'E2', 'ends before the start of', 'starts after the end of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity ends definitely before the start of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-end &lt; B-start  is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to the following Allen temporal relation (Allen, 1983) : {before}.
This property is transitive.

Figure 18: Temporal entity A ends before the start of temporal entity B. Here A is longer than B

Figure 19: Temporal entity A ends before the start of temporal entity B. Here A is shorter than B'),
	(10, 'P23', 'E39', 'E8', 'transferred title from', 'surrendered title through', 'This property identifies the instance(s) of E39 Actor who relinquish legal ownership as the result of an instance of E8 Acquisition.
The property will typically be used to describe a person donating or selling an object to a museum. In reality title is either transferred to or from someone, or both.'),
	(11, 'P104', 'E30', 'E72', 'is subject to', 'applies to', 'This property links a particular instance of E72 Legal Object to the instances of E30 Right to which it is subject.
The Right is held by an E39 Actor as described by P75 possesses (is possessed by).'),
	(12, 'P123', 'E18', 'E81', 'resulted in', 'resulted from', 'This property identifies the instance or instances of E18 Physical Thing that are the result of an instance of E81 Transformation. New items replace the transformed item or items, which cease to exist as units of documentation. The physical continuity between the old and the new is expressed by the links to the common instance of E81 Transformation.'),
	(13, 'P148', 'E89', 'E89', 'has component', 'is component of', 'This property associates an instance of E89 Propositional Object with a structural part of it that is by itself an instance of E89 Propositional Object.
This property is transitive.'),
	(14, 'P71', 'E1', 'E32', 'lists', 'is listed in', 'This property associates an instance of E32 Authority Document, with an instance of E1 CRM Entity which it lists for reference purposes.'),
	(15, 'P75', 'E30', 'E39', 'possesses', 'is possessed by', 'This property associates an instance of E39 Actor to an instance of E30 Right over which the actor holds or has held a legal claim.'),
	(16, 'P56', 'E26', 'E19', 'bears feature', 'is found on', 'This property links an instance of E19 Physical Object to an instance of E26 Physical Feature that it bears.
An instance of E26 Physical Feature can only exist on one object. One object may bear more than one E26 Physical Feature. An instance of E27 Site should be considered as an instance of E26 Physical Feature on the surface of the Earth.
An instance B of E26 Physical Feature being a detail of the structure of another instance A of E26 Physical Feature can be linked to B by use of the property P46 is composed of (forms part of). This implies that the subfeature B is P56i is found on the same E19 Physical Object as A.
This property is a shortcut. A more detailed representation can make use of the fully developed (i.e., indirect) path E19 Physical Object, through, P59 has section, E53 Place, P53i is former or current location of to E26 Physical Feature.'),
	(17, 'P102', 'E35', 'E71', 'has title', 'is title of', 'This property associates an instance of E35 Title has been applied to an instance of E71 Human-Made Thing.
The P102.1 has type property of the P102 has title (is title of) property enables the relationship between the title and the thing to be further clarified, for example, if the title was a given title, a supplied title etc.
It allows any human-made material or immaterial thing to be given a title. It is possible to imagine a title being created without a specific object in mind.'),
	(18, 'P100', 'E21', 'E69', 'was death of', 'died in', 'This property links an instance of E69 Death to the instance of E21 Person that died.
An instance of E69 Death may involve multiple people, for example in the case of a battle or disaster.
This is not intended for use with general natural history material, only people.'),
	(19, 'P184', 'E2', 'E2', 'ends before or with the end of', 'ends with or after the end of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity ends before or simultaneously with the end of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-end ≤ B-end is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to a disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets, overlaps, finished by, start, equals, during, finishes}.

Figure 20: Temporal entity A ends before or with the end of temporal entity B. Here A is longer than B

Figure 21: Temporal entity A ends before or with the end of temporal entity B. Here A is shorter than B'),
	(20, 'P1', 'E41', 'E1', 'is identified by', 'identifies', 'This property describes the naming or identification of any real-world item by a name or any other identifier.
This property is intended for identifiers in general use, which form part of the world the model intends to describe, and not merely for internal database identifiers which are specific to a technical system, unless these latter also have a more general use outside the technical context. This property includes in particular identification by mathematical expressions such as coordinate systems used for the identification of instances of E53 Place. The property does not reveal anything about when, where and by whom this identifier was used. A more detailed representation can be made using the fully developed (i.e., indirect) path through E15 Identifier Assignment.
This property is a shortcut for the path from E1 CRM Entity through P140i was attributed by, E15 Identifier Assignment, P37 assigned to E42 Identifier.
It is also a shortcut for the path from E1 CRM Entity through P1 is identified by, E41 Appellation, P139 has alternative form to E41 Appellation.'),
	(21, 'P76', 'E41', 'E39', 'has contact point', 'provides access to', 'This property associates an instance of E39 Actor to an instance of E41 Appellation which a communication service uses to direct communications to this actor, such as an e-mail address, fax number, or postal address.'),
	(22, 'P139', 'E41', 'E41', 'has alternative form', NULL, 'This property associates an instance of E41 Appellation with another instance of E41 Appellation that constitutes a derivative or variant of the former and that may also be used for identifying items identified by the former, in suitable contexts, independent from the particular item to be identified. This property should not be confused with additional variants of names used characteristically for a single, particular item, such as individual nicknames. It is an asymmetric relationship, where the range expresses the derivative, if such a direction can be established. Otherwise, the relationship is symmetric. The relationship is not transitive.
Multiple names assigned to an object, which do not apply to all things identified with the specific instance of E41 Appellation, should be modelled as repeated values of P1 is identified by (identifies) of this object.
P139.1 has type allows the type of derivation to be refined, for instance “transliteration from Latin 1 to ASCII”.'),
	(23, 'P37', 'E42', 'E15', 'assigned', 'was assigned by', 'This property records the identifier that was assigned to an item in an instance of P37 Identifier Assignment.
The same identifier may be assigned on more than one occasion.
An Identifier might be created prior to an assignment.'),
	(24, 'P142', 'E90', 'E15', 'used constituent', 'was used in', 'This property associates an instance of E15 Identifier Assignment with the instance of E90 Symbolic Object used as constituent of an instance of E42 Identifier in this act of assignment.'),
	(25, 'P7', 'E53', 'E4', 'took place at', 'witnessed', 'This property describes the spatial location of an instance of E4 Period.
The related instance of E53 Place should be seen as a wider approximation of the geometric area within which the phenomena that characterise the period in question occurred, see below. P7 took place at (witnessed) does not convey any meaning other than spatial positioning (frequently on the surface of the earth). For example, the period “Révolution française” can be said to have taken place in “France in 1789”; the “Victorian” period may be said to have taken place in “Britain from 1837-1901” and its colonies, as well as other parts of Europe and North America. An instance of E4 Period can take place at multiple non-contiguous, non-overlapping locations.
This property is a shortcut of the more fully developed path from E4 Period through P161 has spatial projection, E53 Place, P89 falls within to E53 Place. E4 Period is a subclass of E92 Spacetime Volume. By the definition of P161 has spatial projection an instance of E4 Period takes place on all its spatial projections, that is, instances of E53 Place. Something happening at a given place can also be considered to happen at a larger place containing the first. For example, the assault on the Bastille July 14th 1789 took place in the area covered by Paris in 1789 but also in the area covered by France in 1789.'),
	(26, 'P140', 'E1', 'E13', 'assigned attribute to', 'was attributed by', 'This property associates an instance of E13 Attribute Assignment with the instance of E1 CRM Entity about which it made an attribution. The instance of E1 CRM Entity plays the role of the domain of the attribution.
The kind of attribution made should be documented using P177 assigned property type.'),
	(27, 'P52', 'E39', 'E18', 'has current owner', 'is current owner of', 'This property identifies the instance of E21 Person or E74 Group that was the owner of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
This property is a shortcut for the more detailed path from E18 Physical Thing through, P24i changed ownership through, E8 Acquisition, P22 transferred title to to E39 Actor, if and only if this acquisition event is the most recent.'),
	(28, 'P98', 'E21', 'E67', 'brought into life', 'was born', 'This property links an instance of E67 Birth event to an instance of E21 Person in the role of offspring.
Twins, triplets etc. are brought into life by the same instance of E67 Birth. This is not intended for use with general Natural History material, only people. There is no explicit method for modelling conception and gestation except by using extensions.'),
	(29, 'P185', 'E2', 'E2', 'ends before the end of', 'ends after the end of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity ends definitely before the end of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-end &lt; B-end is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to a disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets, overlaps, starts, during}.
This property is transitive.

Figure 22: Temporal entity A ends before the end of temporal entity B. Here A is longer than B

Figure 23: Temporal entity A ends before the end of temporal entity B. Here A is shorter than B'),
	(30, 'P21', 'E55', 'E7', 'had general purpose', 'was purpose of', 'This property describes an intentional relationship between an instance of E7 Activity and some general goal or purpose, described as an instance of E55 Type.
This may involve activities intended as preparation for some type of activity or event. P21 had general purpose (was purpose of) differs from P20 had specific purpose (was purpose of) in that no occurrence of an event is implied as the purpose.'),
	(31, 'P93', 'E77', 'E64', 'took out of existence', 'was taken out of existence by', 'This property links an instance of E64 End of Existence to the instance of E77 Persistent Item taken out of existence by it.
In the case of immaterial things, the instance of E64 End of Existence is considered to take place with the destruction of the last physical carrier.
This allows an “end” to be attached to any instance of E77 Persistent Item being documented i.e., instances of E70 Thing, E72 Legal Object, E39 Actor, E41 Appellation and E55 Type. For many instances of E77 Persistent Item we know the maximum life-span and can infer, that they must have ended to exist. We assume in that case an instance of E64 End of Existence, which may be as unnoticeable as forgetting the secret knowledge by the last representative of some indigenous nation.'),
	(32, 'P108', 'E24', 'E12', 'has produced', 'was produced by', 'This property identifies the instance of E24 Physical Human-Made Thing that came into existence as a result of the instance of E12 Production.
The identity of an instance of E24 Physical Human-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Human-Made Thing.'),
	(33, 'P54', 'E53', 'E19', 'has current permanent location', 'is current permanent location of', 'This property records the foreseen permanent location of an instance of E19 Physical Object at the time of validity of the record or database containing the statement that uses this property.
P54 has current permanent location (is current permanent location of) is similar to P55 has current location (currently holds). However, it indicates the E53 Place currently reserved for an object, such as the permanent storage location or a permanent exhibit location. The object may be temporarily removed from the permanent location, for example when used in temporary exhibitions or loaned to another institution. The object may never actually be located at its permanent location.'),
	(34, 'P69', 'E29', 'E29', 'has association with', 'is associated with', 'This property generalises relationships like whole-part, sequence, prerequisite or inspired by between instances of E29 Design or Procedure. Any instance of E29 Design or Procedure may be associated with other designs or procedures. The property is considered to be symmetrical unless otherwise indicated by P69.1 has type. The property is not transitive
The P69.1 has type property of P69 has association with allows the nature of the association to be specified reading from domain to range; examples of types of association between instances of E29 Design or Procedure include: has part, follows, requires, etc.
The property can typically be used to model the decomposition of the description of a complete workflow into a series of separate procedures.'),
	(35, 'P105', 'E39', 'E72', 'right held by', 'has right on', 'This property identifies the instance of E39 Actor who holds the instances of E30 Right to an instance of E72 Legal Object.
It is a superproperty of P52 has current owner (is current owner of) because ownership is a right that is held on the owned object.
This property is a shortcut of the fully developed path from E72 Legal Object, P104 is subject to, E30 Right, P75i is possessed by to E39 Actor.'),
	(36, 'P68', 'E57', 'E29', 'foresees use of', 'use foreseen by', 'This property identifies an instance of E57 Material foreseen to be used by an instance of E29 Design or Procedure.
E29 Designs and procedures commonly foresee the use of particular instances of E57 Material. The fabrication of adobe bricks, for example, requires straw, clay and water. This property enables this to be documented.
This property is not intended for the documentation of instances of E57 Materials that were used on a particular occasion when an instance of E29 Design or Procedure was executed.'),
	(37, 'P35', 'E3', 'E14', 'has identified', 'was identified by', 'This property identifies the instance of E3 Condition State that was observed in an instance of E14 Condition Assessment activity.'),
	(38, 'P73', 'E33', 'E33', 'has translation', 'is translation of', 'This property links an instance of E33 Linguistic Object (A), to another instance of E33 Linguistic Object (B) which is the translation of A.
When an instance of E33 Linguistic Object is translated into a new language a new instance of E33 Linguistic Object is created, despite the translation being conceptually similar to the source.
This property is non-symmetric.'),
	(39, 'P13', 'E18', 'E6', 'destroyed', 'was destroyed by', 'This property links an instance of E6 Destruction to an instance of E18 Physical Thing that has been destroyed by it.
Destruction implies the end of an item’s life as a subject of cultural documentation – the physical matter of which the item was composed may in fact continue to exist. An instance of E6 Destruction may be contiguous with an instance of E12 Production that brings into existence a derived object composed partly of matter from the destroyed object.'),
	(40, 'P136', 'E1', 'E83', 'was based on', 'supported type creation', 'This property identifies one or more instances of E1 CRM Entity that were used as evidence to declare a new instance of E55 Type.
The examination of these items is often the only objective way to understand the precise characteristics of a new type. Such items should be deposited in a museum or similar institution for that reason. The taxonomic role renders the specific relationship of each item to the type, such as "holotype" or "original element".'),
	(41, 'P10', 'E92', 'E92', 'falls within', 'contains', 'This property associates an instance of E92 Spacetime Volume with another instance of E92 Spacetime Volume that falls within the latter. In other words, all points in the former are also points in the latter.
This property is transitive and reflexive.'),
	(42, 'P8', 'E18', 'E4', 'took place on or within', 'witnessed', 'This property describes the location of an instance of E4 Period with respect to an instance of E19 Physical Object.
This property is a shortcut of the more fully developed path from E4 Period through P7 took place at, E53 Place, P156i is occupied by E18 Physical Thing.
It describes a period that can be located with respect to the space defined by an E19 Physical Object such as a ship or a building. The precise geographical location of the object during the period in question may be unknown or unimportant.
For example, the French and German armistice of 22 June 1940 was signed in the same railway carriage as the armistice of 11 November 1918.'),
	(43, 'P95', 'E74', 'E66', 'has formed', 'was formed by', 'This property associates the instance of E66 Formation with the instance of E74 Group that it founded.'),
	(44, 'P132', 'E92', 'E92', 'spatiotemporally overlaps with', NULL, 'This symmetric property associates two instances of E92 Spacetime Volume that have some of their extents in common. If only the fuzzy boundaries of the instances of E92 Spacetime Volume overlap, this property cannot be determined from observation alone and therefore should not be applied. However, there may be other forms of justification that the two instances of E92 Spacetime Volume must have some of their extents in common regardless of where and when precisely.
If this property holds for two instances of E92 Spacetime Volume then it cannot be the case that P133 is spatiotemporally separated from also holds for the same two instances. Furthermore, there are cases where neither P132 spatiotemporally overlaps with nor P133 is spatiotemporally separated from holds between two instances of E92 Spacetime Volume. This would occur where only an overlap of the fuzzy boundaries of the two instances of E92 Spacetime Volume occurs and no other evidence is available.
This property is symmetric'),
	(45, 'P145', 'E39', 'E86', 'separated', 'left by', 'This property identifies the instance of E39 Actor that leaves an instance of E74 Group through an instance of E86 Leaving.'),
	(46, 'P74', 'E53', 'E39', 'has current or former residence', 'is current or former residence of', 'This property describes the current or former place of residence (an instance of E53 Place) of an instance of E39 Actor.
The residence may be either the place where the actor resides, or a legally registered address of any kind.'),
	(47, 'P135', 'E55', 'E83', 'created type', 'was created by', 'This property identifies the instance of E55 Type, which is created in an instance of E83 Type Creation activity.'),
	(48, 'P72', 'E56', 'E33', 'has language', 'is language of', 'This property associates an instance(s) of E33 Linguistic Object with an instance of E56 Language in which it is, at least partially, expressed.
Linguistic Objects are composed in one or more human Languages. This property allows these languages to be documented.'),
	(49, 'P9', 'E4', 'E4', 'consists of', 'forms part of', 'This property associates an instance of E4 Period with another instance of E4 Period that is defined by a subset of the phenomena that define the former. Therefore, the spacetime volume of the latter must fall within the spacetime volume of the former.
This property is transitive and non-symmetric.'),
	(50, 'P138', 'E1', 'E36', 'represents', 'has representation', 'This property establishes the relationship between an instance of E36 Visual Item and the instance of E1 CRM Entity that it visually represents.
Any entity may be represented visually. This property is part of the fully developed path from E24 Physical Human-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1 CRM Entity, which is shortcut by P62 depicts (is depicted by). P138.1 mode of representation allows the nature of the representation to be refined.
This property is also used for the relationship between an original and a digitisation of the original by the use of techniques such as digital photography, flatbed or infrared scanning. Digitisation is here seen as a process with a mechanical, causal component rendering the spatial distribution of structural and optical properties of the original and does not necessarily include any visual similarity identifiable by human observation.'),
	(51, 'P43', 'E54', 'E70', 'has dimension', 'is dimension of', 'This property records a E54 Dimension of some E70 Thing.
In the case that the recorded property is a result of a measurement of an instance of E18 Physical Thing, this property is a shortcut of the more fully developed path from E18 Physical Thing through P39i was measured by, E16 Measurement, P40 observed dimension to E54 Dimension.
It offers no information about how and when an E54 Dimension was established, nor by whom. Knowledge about an instance of E54 Dimension need not be the result of a measurement; it may be the result of evaluating data or other information, which should be documented as an instance of E13 Attribute Assignment.
An instance of E54 Dimension is specific to an instance of E70 Thing.'),
	(52, 'P49', 'E39', 'E18', 'has former or current keeper', 'is former or current keeper of', 'This property identifies the instance of E39 Actor who has or has had custody of an instance of E18 Physical Thing at some time. This property leaves open the question if parts of this physical thing have been added or removed during the time-spans it has been under the custody of this actor, but it is required that at least a part which can unambiguously be identified as representing the whole has been under this custody for its whole time. The way, in which a representative part is defined, should ensure that it is unambiguous who keeps a part and who the whole and should be consistent with the identity criteria of the kept instance of E18 Physical Thing.
The distinction with P50 has current keeper (is current keeper of) is that P49 has former or current keeper (is former or current keeper of) leaves open the question as to whether the specified keepers are current.
This property is a shortcut for the more detailed path from E18 Physical Thing through P30i custody transferred through, E10 Transfer of Custody, P28 custody surrendered by or P29 custody received by to E39 Actor.'),
	(53, 'P22', 'E39', 'E8', 'transferred title to', 'acquired title through', 'This property identifies the instance of E39 Actor that acquires the legal ownership of an object as a result of an instance of E8 Acquisition.
The property will typically describe an Actor purchasing or otherwise acquiring an object from another Actor. However, title may also be acquired, without any corresponding loss of title by another Actor, through legal fieldwork such as hunting, shooting or fishing.
In reality the title is either transferred to or from someone, or both.'),
	(54, 'P128', 'E90', 'E18', 'carries', 'is carried by', 'This property identifies an instance E90 Symbolic Object carried by an instance of E18 Physical Thing. Since an instance of E90 Symbolic Object is defined as an immaterial idealization over potentially multiple carriers, any individual realization on a particular physical carrier may be defective, due to deterioration or shortcomings in the process of creating the realization compared to the intended ideal. As long as such defects do not substantially affect the complete recognition of the respective symbolic object, it is still regarded as carrying an instance of this E90 Symbolic Object. If these defects are of scholarly interest, the particular realization can be modelled as an instance of E25 Human-Made Feature. Note, that any instance of E90 Symbolic Object incorporated (P165) in the carried symbolic object is also carried by the same instance of E18 Physical Thing.'),
	(55, 'P147', 'E78', 'E87', 'curated', 'was curated by', 'This property associates an instance of E87 Curation Activity with the instance of E78 Curated Holding with that is subject of that curation activity following some implicit or explicit curation plan.'),
	(56, 'P111', 'E18', 'E79', 'added', 'was added by', 'This property identifies the instance of E18 Physical Thing that is added during an instance of E79 Part Addition activity'),
	(57, 'P91', 'E58', 'E54', 'has unit', 'is unit of', 'This property shows the type of unit an instance of E54 Dimension was expressed in.'),
	(58, 'P191', 'E54', 'E52', 'had duration', 'was duration of', 'This property describes the length of time covered by an instance of E52 Time-Span. It allows an instance of E52 Time-Span to be associated with an instance of E54 Dimension representing duration independent from the actual beginning and end. Indeterminacy of the duration value can be expressed by assigning a numerical interval to the property P90 has value of E54 Dimension.'),
	(59, 'P53', 'E53', 'E18', 'has former or current location', 'is former or current location of', 'This property identifies an instance of E53 Place as the former or current location of an instance of E18 Physical Thing.
In the case of instances of E19 Physical Object, the property does not allow any indication of the Time-Span during which the instance of E19 Physical Object was located at this instance of E53 Place, nor if this is the current location.
In the case of immobile objects, the Place would normally correspond to the Place of creation.
This property is a shortcut. A more detailed representation can make use of the fully developed (i.e., indirect) path from E19 Physical Object, though, P25i moved by, E9 Move, P26 moved to or P27 moved from to E53 Place.'),
	(60, 'P12', 'E77', 'E5', 'occurred in the presence of', 'was present at', 'This property describes the active or passive presence of an E77 Persistent Item in an instance of E5 Event without implying any specific role.
It documents known events in which an instance of E77 Persistent Item was present during the course of its life or history. For example, an object may be the desk, now in a museum, on which a treaty was signed. The instance of E53 Place and the instance of E52 Time-Span where and when these events happened provide us with constraints about the presence of the related instance E77 Persistent Item in the past. Instances of E90 Symbolic Object, in particular information objects, are physically present in events via at least one of the instances of E18 Physical Thing carrying them. Note, that the human mind can be such a carrier. A precondition for a transfer of information to a person or another new physical carrier is the presence of the respective information object and this person or physical thing in one event.'),
	(61, 'P189', 'E53', 'E53', 'approximates', 'is approximated by', 'This property associates an instance of E53 Place with another instance of E53 Place, which is defined in the same reference space, and which is used to approximate the former. The property does not necessarily state the quality or accuracy of this approximation, but rather indicates the use of the first instance of place to approximate the second.
In common documentation practice, find or encounter spots e.g., in archaeology, botany or zoology are often related to the closest village, river or other named place without detailing the relation, e.g., if it is located within the village or in a certain distance of the specified place. In this case the stated “phenomenal” place found in the documentation can be seen as approximation of the actual encounter spot without more specific knowledge.
In more recent documentation often point coordinate information is provided that originates from GPS measurements or georeferencing from a map. This point coordinate information does not state the actual place of the encounter spot but tries to approximate it with a “declarative” place. The accuracy depends on the methodology used when creating the coordinates. It may be dependent on technical limitations like GPS accuracy but also on the method where the GPS location is taken in relation to the measured feature. If the methodology is known a maximum deviation from the measured point can be calculated and the encounter spot or feature may be related to the resulting circle using an instance of P171 at some place within.
This property is not transitive.'),
	(62, 'P124', 'E18', 'E81', 'transformed', 'was transformed by', 'This property identifies the instance or instances E18 Physical Thing that have ceased to exist due to an instance of E81 Transformation.
The item that has ceased to exist and was replaced by the result of the Transformation. The continuity between both items, the new and the old, is expressed by the links to the common instance of E81 Transformation.'),
	(63, 'P20', 'E5', 'E7', 'had specific purpose', 'was purpose of', 'This property identifies the relationship between a preparatory activity, an instance of E7 Activity and the instance of E7 Event it is intended to be preparation for.
This includes activities, orders and other organisational actions, taken in preparation for other activities or events.
P20 had specific purpose (was purpose of) implies that an activity succeeded in achieving its aim. If it does not succeed, such as the setting of a trap that did not catch anything, one may document the unrealized intention using P21 had general purpose (was purpose of): E55 Type and/or P33 used specific technique (was used by): E29 Design or Procedure.'),
	(64, 'P59', 'E53', 'E18', 'has section', 'is located on or within', 'This property links an area, i.e., an instance of E53 Place to the instance of E18 Physical Thing upon which it is found. This area may either be identified by a name, or by a geometry in terms of a coordinate system adapted to the shape of the respective instance of E18 Physical Thing. Typically, names identifying sections of physical objects are composed of the name of a kind of part and the name of the object itself, such as "The poop deck of H.M.S. Victory", which is composed of "poop deck" and "H.M.S. Victory".'),
	(65, 'P16', 'E70', 'E7', 'used specific object', 'was used for', 'This property describes the use of material or immaterial things in a way essential to the performance or the outcome of an instance of E7 Activity.
This property typically applies to tools, instruments, moulds, raw materials and items embedded in a product. It implies that the presence of the object in question was a necessary condition for the action. For example, the activity of writing this text required the use of a computer. An immaterial thing can be used if at least one of its carriers is present. For example, the software tools on a computer.
Another example is the use of a particular name by a particular group of people over some span to identify a thing, such as a settlement. In this case, the physical carriers of this name are at least the people understanding its use.'),
	(66, 'P107', 'E39', 'E74', 'has current or former member', 'is current or former member of', 'This property associates an instance of E74 Group with an instance of E39 Actor that is or has been a member thereof.
Instances of E74 Group and E21 Person, may all be members of instances of E74 Group.An instance of E74 Group may be founded initially without any member.
This property is a shortcut of the more fully developed path from E74 Group, P144i gained member by, E85 Joining, P143 joined to E39 Actor.
The property P107.1 kind of member can be used to specify the type of membership or the role the member has in the group.'),
	(67, 'P2', 'E55', 'E1', 'has type', 'is type of', 'This property allows sub typing of CIDOC CRM entities –a form of specialisation – through the use of a terminological hierarchy, or thesaurus.
The CIDOC CRM is intended to focus on the high-level entities and relationships needed to describe data structures. Consequently, it does not specialise entities any further than is required for this immediate purpose. However, entities in the isA hierarchy of the CIDOC CRM may by specialised into any number of sub entities, which can be defined in the E55 Type hierarchy. E41 Appellation, for example, may be specialised into “e-mail address”, “telephone number”, “post office box”, “URL” etc. none of which figures explicitly in the CIDOC CRM hierarchy. A comprehensive explanation about refining CIDOC CRM concepts by E55 Type is given in the section “About Types” in the section on “Specific Modelling Constructs” of this document.
This property is a shortcut for the path from E1 CRM Entity through P41i was classified by, E17 Type Assignment, P42 assigned to E55 Type.'),
	(68, 'P179', 'E97', 'E96', 'had sales price', 'was sales price of', 'This property establishes the relationship between an instance of E96 Purchase and the instance of E97 Monetary Amount that forms the compensation for the transaction. The monetary amount agreed upon may change in the course of the purchase activity.'),
	(69, 'P106', 'E90', 'E90', 'is composed of', 'forms part of', 'This property associates an instance of E90 Symbolic Object with a part of it that is by itself an instance of E90 Symbolic Object, such as fragments of texts or clippings from an image.
This property is transitive and non-reflexive.'),
	(70, 'P38', 'E42', 'E15', 'deassigned', 'was deassigned by', 'This property records the identifier that was deassigned from an instance of E1 CRM Entity.
De-assignment of an identifier may be necessary when an item is taken out of an inventory, a new numbering system is introduced or items are merged or split up.
The same identifier may be deassigned on more than one occasion.'),
	(71, 'P40', 'E54', 'E16', 'observed dimension', 'was observed in', 'This property records the dimension that was observed in an E16 Measurement Event.
E54 Dimension can be any quantifiable aspect of E70 Thing. Weight, image colour depth and monetary value are dimensions in this sense. One measurement activity may determine more than one dimension of one object.
Dimensions may be determined either by direct observation or using recorded evidence. In the latter case the measured Thing does not need to be present or extant.
Even though knowledge of the value of a dimension requires measurement, the dimension may be an object of discourse prior to, or even without, any measurement being made.'),
	(72, 'P188', 'E19', 'E99', 'requires production tool', 'is production tool for', 'This property associates an instance of E99 Product Type with an instance of E19 Physical Object that is needed for the production of an instance of E18 Physical Thing. When the process of production is correctly executed in accordance with the plan and using the specified instance of E19 Physical Object, the resulting instance of E18 Physical Thing is considered an exemplar of this instance of E99 Product Type. The instance of E19 Physical Object may bear distinct features that are transformed into characteristic features of the resulting instance of E18 Physical Thing. Examples include models and moulds.'),
	(73, 'P177', 'E55', 'E13', 'assigned property of type', 'is type of property assigned', 'This property associates an instance of E13 Attribute Assignment with the type of property or relation that this assignment maintains to hold between the item to which it assigns an attribute and the attribute itself. Note that the properties defined by the CIDOC CRM also constitute instances of E55 Type themselves. The direction of the assigned property type is understood to be from the attributed item (the range of property P140 assigned attribute to) to the attribute item (the range of the property P141 assigned). More than one property type may be assigned to hold between two items.
A comprehensive explanation about refining CIDOC CRM concepts by E55 Type is given in the section “About Types” in the section on “Specific Modelling Constructs” of this document.'),
	(74, 'P96', 'E21', 'E67', 'by mother', 'gave birth', 'This property links an instance of E67 Birth to an instance of E21 Person in the role of birth-giving mother.
Note that biological fathers are not necessarily participants in the Birth (see P97 from father (was father for)). The instance of P21 Person being born is linked to the instance of E67 Birth with the property P98 brought into life (was born). This is not intended for use with general natural history material, only people. There is no explicit method for modelling conception and gestation except by using extensions.'),
	(75, 'P143', 'E39', 'E85', 'joined', 'was joined by', 'This property identifies the instance of E39 Actor that becomes member of an instance of E74 Group in an instance of E85 Joining.
Joining events allow for describing people becoming members of a group with the more detailed path E74 Group, P144i gained member by, E85 Joining, P143 joined, E39 Actor, compared to the shortcut offered by P107 has current or former member (is current or former member of).'),
	(102, 'P110', 'E24', 'E79', 'augmented', 'was augmented by', 'This property identifies the instance of E24 Physical Human-Made Thing that is added to (augmented) in an instance of E79 Part Addition.
Although an instance of E79 Part Addition event normally concerns only one instance of E24 Physical Human-Made Thing, it is possible to imagine circumstances under which more than one item might be added to (augmented). For example, the artist Jackson Pollock trailing paint onto multiple canvasses.'),
	(76, 'P165', 'E90', 'E73', 'incorporates', 'is incorporated in', 'This property associates an instance of E73 Information Object with an instance of E90 Symbolic Object (or any of its subclasses) that was included in it.
This property makes it possible to recognise the autonomous status of the incorporated signs, which were created in a distinct context, and can be incorporated in many instances of E73 Information Object, and to highlight the difference between structural and accidental whole-part relationships between conceptual entities.
It accounts for many cultural facts that are quite frequent and significant: the inclusion of a poem in an anthology, the re-use of an operatic aria in a new opera, the use of a reproduction of a painting for a book cover or a CD booklet, the integration of textual quotations, the presence of lyrics in a song that sets those lyrics to music, the presence of the text of a play in a movie based on that play, etc.
In particular, this property allows for modelling relationships of different levels of symbolic specificity, such as the natural language words making up a particular text, the characters making up the words and punctuation, the choice of fonts and page layout for the characters.
When restricted to information objects, that is, seen as a property with E73 Information Object as domain and range the property is transitive.
A digital photograph of a manuscript page incorporates the text of a manuscript page, if the respective text is defined as a sequence of symbols of a particular type, such as Latin characters, and the resolution and quality of the digital image is sufficient to resolve these symbols so they are readable on the digital image.'),
	(77, 'P129', 'E1', 'E89', 'is about', 'is subject of', 'This property documents that an instance of E89 Propositional Object has as subject an instance of E1 CRM Entity.
This differs from P67 refers to (is referred to by), which refers to an instance of E1 CRM Entity, in that it describes the primary subject or subjects of an instance of E89 Propositional Object.'),
	(78, 'P127', 'E55', 'E55', 'has broader term', 'has narrower term', 'This property associates an instance of E55 Type with another instance of E55 Type that has a broader meaning.
It allows instances of E55 Types to be organised into hierarchies. This is the sense of "broader term generic (BTG)" as defined in ISO 25964-2:2013 (International Organization for Standardization 2013).
This property is transitive.'),
	(79, 'P126', 'E57', 'E11', 'employed', 'was employed in', 'This property identifies the instance of E57 Material employed in an instance of E11 Modification.
The instance of E57 Material used during the instance of E11 Modification does not necessarily become incorporated into the instance of E24 Physical Human-Made Thing that forms the subject of the instance of E11 Modification.'),
	(80, 'P125', 'E55', 'E7', 'used object of type', 'was type of object used in', 'This property associates an instance of E7 Activity to an instance of E55 Type, which classifies an instance of E70 Thing used in an instance of E7 Activity, when the specific instance is either unknown or not of interest, such as use of "a hammer".
This property is a shortcut of the more fully developed path from E7 Activity through P16 used specific object, E70 Thing, P2 has type, to E55 Type'),
	(81, 'P11', 'E39', 'E5', 'had participant', 'participated in', 'This property describes the active or passive participation of instances of E39 Actors in an instance of E5 Event.
It documents known events in which an instance of E39 Actor has participated during the course of that actor’s life or history. The instances of E53 Place and E52 Time-Span where and when these events happened provide us with constraints about the presence of the related instances of E39 Actor in the past. Collective actors, i.e., instances of E74 Group, may physically participate in events via their representing instances of E21 Persons only. The participation of multiple actors in an event is most likely an indication of their acquaintance and interaction.
The property implies that the actor was involved in the event but does not imply any causal relationship. For instance, someone having been portrayed can be said to have participated in the creation of the portrait.'),
	(82, 'P45', 'E57', 'E18', 'consists of', 'is incorporated in', 'This property identifies the instances of E57 Materials of which an instance of E18 Physical Thing is composed.
All physical things consist of physical materials. P45 consists of (is incorporated in) allows the different materials to be recorded. P45 consists of (is incorporated in) refers here to observed material as opposed to the consumed raw material.
A material, such as a theoretical alloy, may not have any physical instances.'),
	(83, 'P164', 'E52', 'E93', 'is temporally specified by', 'temporally specifies', 'This property relates an instance of E93 Presence with the instance of E52 Time-Span that defines the time-slice of the spacetime volume that this instance of E93 Presence is related to via the property P166 was a presence of (had presence).
There are two typical cases for the determination of the related instance of E52 Time-Span. In the first, it is the temporal extent of an instance of E2 Temporal Entity (documented with P4 has time-span (is time-span of)): this then documents the simultaneity of the instance of E93 Presence and the instance of E2 Temporal Entity, even if the absolute time-span is not known, and can be regarded as a phenomenal timespan. In the second, the instance of E52 Time-Span is a date range declared in or derived from historical sources or provided by dating methods: this is a declarative timespan.'),
	(84, 'P51', 'E39', 'E18', 'has former or current owner', 'is former or current owner of', 'This property identifies an instance of E39 Actor that is or had been the legal owner (i.e., title holder) of an instance of E18 Physical Thing at some time.
The distinction with P52 has current owner (is current owner of) is that P51 has former or current owner (is former or current owner of) does not indicate whether the specified owners are current.
This property is a shortcut for the more detailed path from E18 Physical Thing through P24i changed ownership through, E8 Acquisition, P23 transferred title from, or P22 transferred title to to E39 Actor.'),
	(85, 'P134', 'E7', 'E7', 'continued', 'was continued by', 'This property associates two instances of E7 Activity, where the domain is considered as an intentional continuation of the range. A continuation of an activity may happen when the continued activity is still ongoing or after the continued activity has completely ended. The continuing activity may have started already before it decided to continue the other one. Continuation implies a coherence of intentions and outcomes of the involved activities.
This property is not transitive.'),
	(103, 'P160', 'E52', 'E92', 'has temporal projection', 'is temporal projection of', 'This property describes the temporal projection of an instance of E92 Spacetime Volume. The property P4 has time-span is the same as P160 has temporal projection if it is used to document an instance of E4 Period or any subclass of it.'),
	(86, 'P62', 'E1', 'E24', 'depicts', 'is depicted by', 'This property identifies something that is depicted by an instance of E24 Physical Human-Made Thing. Depicting is meant in the sense that an instance of E24 Physical Human-Made Thing intentionally shows, through its optical qualities or form, a representation of the entity depicted. Photographs are by default regarded as being intentional in this sense. Anything that is designed to change the properties of the depiction, such as an e-book reader, is specifically excluded. The property does not pertain to inscriptions or any other information encoding.
This property is a shortcut of the more fully developed path from E24 Physical Human-Made Thing through P65 shows visual item, E36 Visual Item, P138 represents to E1 CRM Entity. P138.1 mode of depiction allows the nature of the depiction to be refined.'),
	(87, 'P24', 'E18', 'E8', 'transferred title of', 'changed ownership through', 'This property identifies the instance(s) of E18 Physical Thing involved in an instance of E8 Acquisition.
In reality, an acquisition must refer to at least one transferred item.'),
	(88, 'P67', 'E1', 'E89', 'refers to', 'is referred to by', 'This property documents that an instance of E89 Propositional Object makes a statement about an instance of E1 CRM Entity. P67 refers to (is referred to by) has the P67.1 has type link to an instance of E55 Type. This is intended to allow a more detailed description of the type of reference. This differs from P129 is about (is subject of), which describes the primary subject or subjects of the instance of E89 Propositional Object.'),
	(89, 'P14', 'E39', 'E7', 'carried out by', 'performed', 'This property describes the active participation of an instance of E39 Actor in an instance of E7 Activity.
It implies causal or legal responsibility. The P14.1 in the role of property of the property specifies the nature of an Actor’s participation.'),
	(90, 'P31', 'E18', 'E11', 'has modified', 'was modified by', 'This property identifies the instance of E18 Physical Thing modified in an instance of E11 Modification.'),
	(91, 'P103', 'E55', 'E71', 'was intended for', 'was intention of', 'This property links an instance of E71 Human-Made Thing to an instance of E55 Type describing its intended usage.
It creates a relation between specific human-made things, both physical and immaterial, to types of intended methods and techniques of use. Note: A link between specific human-made things and a specific use activity should be expressed using P19 was intended use of (was made for).'),
	(92, 'P5', 'E3', 'E3', 'consists of', 'forms part of', 'This property describes the decomposition of an instance of E3 Condition State into discrete, subsidiary states.
It is assumed that the sub-states into which the condition state is analysed form a logical whole - although the entire story may not be completely known – and that the sub-states are in fact constitutive of the general condition state. For example, a general condition state of “in ruins” may be decomposed into the individual stages of decay.
This property is transitive and non-reflexive.'),
	(93, 'P27', 'E53', 'E9', 'moved from', 'was origin of', 'This property identifies an origin, an instance of E53 Place, of an instance of E9 Move.
A move will be linked to an origin, such as the move of an artifact from storage to display. A move may be linked to many starting instances of E53 Place by multiple instances of this property. In this case the move describes the picking up of a set of objects. The area of the move includes the origin(s), route and destination(s).
Therefore, the described origin is an instance of E53 Place which P89 falls within (contains) the instance of E53 Place the move P7 took place at.'),
	(94, 'P86', 'E52', 'E52', 'falls within', 'contains', 'This property describes the inclusion relationship between two instances of E52 Time-Span.
This property supports the notion that the temporal extent of an instance of E52 Time-Span falls within the temporal extent of another instance of E52 Time-Span. It addresses temporal containment only, and no contextual link between the two instances of E52 Time-Span is implied. This property is transitive.'),
	(95, 'P89', 'E53', 'E53', 'falls within', 'contains', 'This property identifies an instance of E53 Place that falls wholly within the extent of another instance of E53 Place.
It addresses spatial containment only and does not imply any relationship between things or phenomena occupying these places.
This property is transitive and reflexive.'),
	(96, 'P133', 'E92', 'E92', 'is spatiotemporally separated from', NULL, 'This symmetric property associates two instances of E92 Spacetime Volume that have no extents in common. If only the fuzzy boundaries of the instances of E92 Spacetime Volume overlap, this property cannot be determined from observation alone and therefore should not be applied. However, there may be other forms of justification that the two instances of E92 Spacetime Volume must not have any of their extents in common regardless of where and when precisely.
If this property holds for two instances of E92 Spacetime Volume then it cannot be the case that P132 spatiotemporally overlaps with also holds for the same two instances. Furthermore, there are cases where neither P132 spatiotemporally overlaps with nor P133 is spatiotemporally separated from holds between two instances of E92 Spacetime Volume. This would occur where only an overlap of the fuzzy boundaries of the two instances of E92 Spacetime Volume occurs and no other evidence is available.
This property is not transitive. This property is symmetric.'),
	(97, 'P94', 'E28', 'E65', 'has created', 'was created by', 'This property links an instance of E65 Creation to the instance of E28 Conceptual Object created by it.
It represents the act of conceiving the intellectual content of the instance of E28 Conceptual Object. It does not represent the act of creating the first physical carrier of the instance of E28 Conceptual Object. As an example, this is the composition of a poem, not its commitment to paper.'),
	(98, 'P151', 'E74', 'E66', 'was formed from', 'participated in', 'This property associates an instance of E66 Formation with an instance of E74 Group from which the new group was formed preserving a sense of continuity such as in mission, membership or tradition.'),
	(99, 'P15', 'E1', 'E7', 'was influenced by', 'influenced', 'This is a high-level property, which captures the relationship between an instance of E7 Activity and anything, that is, an instance of E1 CRM Entity that may have had some bearing upon it.
The property has more specific sub properties.'),
	(100, 'P112', 'E24', 'E80', 'diminished', 'was diminished by', 'This property identifies the instance E24 Physical Human-Made Thing that was diminished by an instance of E80 Part Removal.
Although an instance of E80 Part removal activity normally concerns only one instance of E24 Physical Human-Made Thing, it is possible to imagine circumstances under which more than one item might be diminished by a single instance of E80 Part Removal activity.'),
	(101, 'P32', 'E55', 'E7', 'used general technique', 'was technique of', 'This property identifies the technique or method, modelled as an instance of E55 Type, that was employed in an instance of E7 Activity.
These techniques should be drawn from an external E55 Type hierarchy of consistent terminology of general techniques or methods such as embroidery, oil-painting, carbon dating, etc. Specific documented techniques should be described as instances of E29 Design or Procedure.'),
	(104, 'P122', 'E53', 'E53', 'borders with', NULL, 'This symmetric property associates an instance of E53 Place with another instance of E53 Place which shares a part of its border.
This property is purely spatial. It does not imply that the phenomena that define, by their extent, places related by P122 borders with have ever shared a respective border at the same time or even coexisted. In particular, this may be the case when the respective common border is formed by a natural feature.
This property is not transitive. This property is symmetric.'),
	(105, 'P26', 'E53', 'E9', 'moved to', 'was destination of', 'This property identifies a destination, an instance of E53 place, of an instance of E9 Move.
A move will be linked to a destination, such as the move of an artifact from storage to display. A move may be linked to many terminal instances of E53 Place by multiple instances of this property. In this case the move describes a distribution of a set of objects. The area of the move includes the origin(s), route and destination(s).
Therefore, the described destination is an instance of E53 Place which P89 falls within (contains) the instance of E53 Place the move P7 took place at.'),
	(106, 'P4', 'E52', 'E2', 'has time-span', 'is time-span of', 'This property associates an instance of E2 Temporal Entity with the instance of E52 Time-Span during which it was on-going. The associated instance of E52 Time-Span is understood as the real time-span during which the phenomena making up the temporal entity instance were active. More than one instance of E2 Temporal Entity may share a common instance of E52 Time-Span only if they come into being and end being due to identical declarations or events.'),
	(107, 'P113', 'E18', 'E80', 'removed', 'was removed by', 'This property identifies the instance of E18 Physical Thing that is removed during an instance of E80 Part Removal activity.'),
	(108, 'P157', 'E18', 'E53', 'is at rest relative to', 'provides reference space for', 'This property associates an instance of E53 Place with the instance of E18 Physical Thing that determines a reference space for this instance of E53 Place by being at rest with respect to this reference space. The relative stability of form of an instance of E18 Physical Thing defines its default reference space. The reference space is not spatially limited to the referred thing. For example, a ship determines a reference space in terms of which other ships in its neighbourhood may be described. Larger constellations of matter, such as continental plates, may comprise many physical features that are at rest with them and define the same reference space.'),
	(109, 'P30', 'E18', 'E10', 'transferred custody of', 'custody transferred through', 'This property identifies the instance(s) of E18 Physical Thing concerned in an instance of E10 Transfer of Custody.
The property will typically describe the object that is handed over by an instance of E39 Actor to to the custody of another instance of E39 Actor. On occasion, physical custody may be transferred involuntarily or illegally – through accident, unsolicited donation, or theft.'),
	(110, 'P109', 'E39', 'E78', 'has current or former curator', 'is current or former curator of', 'This property identifies the instance of E39 Actor who assumed or have assumed overall curatorial responsibility for an instance of E78 Curated Holding.
It does not allow a history of curation to be recorded. This would require use of an event initiating a curator being responsible for a collection.'),
	(111, 'P42', 'E55', 'E17', 'assigned', 'was assigned by', 'This property records the type that was assigned to an entity by an E17 Type Assignment activity.
Type assignment events allow a more detailed path from E1 CRM Entity through P41i was classified by, E17 Type Assignment, P42 assigned, to E55 Type for assigning types to objects compared to the shortcut offered by P2 has type (is type of).
For example, a fragment of an antique vessel could be assigned the type “attic red figured belly handled amphora” by expert A. The same fragment could be assigned the type “shoulder handled amphora” by expert B.
A Type may be intellectually constructed independent from assigning an instance of it.'),
	(112, 'P44', 'E3', 'E18', 'has condition', 'is condition of', 'This property records an E3 Condition State for some E18 Physical Thing.
This property is a shortcut of the more fully developed path from E18 Physical Thing through P34i was assessed by, E14 Condition Assessment, P35 has identified to E3 Condition State. It offers no information about how and when the E3 Condition State was established, nor by whom.
An instance of Condition State is specific to an instance of E18 Physical Thing.'),
	(113, 'P65', 'E36', 'E24', 'shows visual item', 'is shown by', 'This property documents an instance of E36 Visual Item shown by an instance of E24 Physical Human-Made Thing.
This property is similar to P62 depicts (is depicted by) in that it associates an instance of E24 Physical Human-Made Thing with a visual representation. However, P65 shows visual item (is shown by) differs from the P62 depicts (is depicted by) property in that it makes no claims about what the instance of E36 Visual Item is deemed to represent. An instance of E36 Visual Item identifies a recognisable image or visual symbol, regardless of what this image may or may not represent.
For example, all recent British coins bear a portrait of Queen Elizabeth II, a fact that is correctly documented using P62 depicts (is depicted by). Different portraits have been used at different periods, however. P65 shows visual item (is shown by) can be used to refer to a particular portrait.
P65 shows visual item (is shown by) may also be used for Visual Items such as signs, marks and symbols, for example the ''Maltese Cross'' or the ''copyright symbol’ that have no particular representational content.
This property is part of the fully developed path E24 Physical Human-Made Thing, P65 shows visual item, E36 Visual Item, P138 represents to E1 CRM Entity which is shortcut by, P62 depicts (is depicted by).'),
	(114, 'P176', 'E2', 'E2', 'starts before the start of', 'starts after the start of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity starts definitely before the start of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-start &lt; B-start is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to a disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets, overlaps, contains, finished-by}. This property is transitive.

Figure 14: Temporal entity A starts before the start of temporal entity B. Here A is longer than B

Figure 15: Temporal entity A starts before the start of temporal entity B. Here A is shorter than B'),
	(115, 'P34', 'E18', 'E14', 'concerned', 'was assessed by', 'This property identifies the instance of E18 Physical Thing that was assessed during an instance of E14 Condition Assessment activity.
Conditions may be assessed either by direct observation or using recorded evidence. In the latter case the instance of E18 Physical Thing does not need to be present or extant at the time of assessment.'),
	(116, 'P187', 'E29', 'E99', 'has production plan', 'is production plan for', 'This property associates an instance of E99 Product Type with an instance of E29 Design or Procedure that completely determines the production of instances of E18 Physical Thing. The resulting instances of E18 Physical Thing are considered exemplars of this instance of E99 Product Type when the process specified is correctly executed. Note that the respective instance of E29 Design or Procedure may not necessarily be fixed in a written/graphical form, and may require the use of tools or models unique to the product type. The same instance of E99 Product Type may be associated with several variant plans.'),
	(117, 'P130', 'E70', 'E70', 'shows features of', 'features are also found on', 'This property generalises the notions of "copy of" and "similar to" into a directed relationship, where the domain expresses the derivative or influenced item and the range the source or influencing item, if such a direction can be established. The property can also be used to express similarity in cases that can be stated between two objects only, without historical knowledge about its reasons. The property expresses a symmetric relationship in case no direction of influence can be established either from evidence on the item itself or from historical knowledge. This holds in particular for siblings of a derivation process from a common source or non-causal cultural parallels, such as some weaving patterns.
The P130.1 kind of similarity property of the P130 shows features of (features are also found on) property enables the relationship between the domain and the range to be further clarified, in the sense from domain to range, if applicable. For example, it may be expressed if both items are product “of the same mould”, or if two texts “contain identical paragraphs”.
If the reason for similarity is a sort of derivation process, i.e., that the creator has used or had in mind the form of a particular thing during the creation or production, this process should be explicitly modelled. In these cases, P130 shows features of can be regarded as a shortcut of such a process. However, the current model does not contain any path specific enough to infer this property. Specializations of the CIDOC CRM may however be more explicit, for instance describing the use of moulds etc.
This property is not transitive.'),
	(118, 'P70', 'E1', 'E31', 'documents', 'is documented in', 'This property describes the CRM Entities documented as instances of E31 Document.
Documents may describe any conceivable entity, hence the link to the highest-level entity in the CIDOC CRM class hierarchy. This property is intended for cases where a reference is regarded as making a proposition about reality. This may be of a documentary character, in the scholarly or scientific sense, or a more general statement.'),
	(119, 'P99', 'E74', 'E68', 'dissolved', 'was dissolved by', 'This property associates the instance of E68 Dissolution with the instance of E74 Group that it disbanded.'),
	(120, 'P48', 'E42', 'E1', 'has preferred identifier', 'is preferred identifier of', 'This property records the preferred instance of E42 Identifier that was used to identify an instance of E1 CRM Entity at the time this property was recorded.
More than one preferred identifier may have been assigned to an item over time.
Use of this property requires an external mechanism for assigning temporal validity to the respective CIDOC CRM instance.
The fact that an identifier is a preferred one for an organisation can be better expressed in a context independent form by assigning a suitable instance of E55 Type to the respective instance of E15 Identifier Assignment using the P2 has type property.'),
	(121, 'P166', 'E92', 'E93', 'was a presence of', 'had presence', 'This property associates an instance of E93 Presence with the instance of E92 Spacetime Volume of which it represents a temporal restriction (i.e.: a time-slice). Instantiating this property constitutes a necessary part of the identity of the respective instance of E93 Presence.'),
	(122, 'P197', 'E53', 'E93', 'covered parts of', 'was partially covered by', 'This property associates an instance of E93 Presence with an instance of E53 Place that geometrically overlaps with the spatial projection of the respective instance of E93 Presence. A use case of this property is to state through which places an object or an instance of E21 Person has or was moved within a given time-span. It may also be used to describe a partial or complete, temporary or permanent extension of the spatial extent of some realm into a neighbouring region during a known time-span. It may also be used to describe a partial or complete, temporary or permanent extension of the spatial extent of some realm into a neighbouring region during a known time-span.
This property is a shortcut of the more fully developed path from E93 Presence through P161 has spatial projection, E53 Place, P121 overlaps with, to E53 Place.'),
	(123, 'P97', 'E21', 'E67', 'from father', 'was father for', 'This property links an instance of E67 Birth to an instance of E21 Person in the role of biological father.
Note that biological fathers are not seen as necessary participants in the birth, whereas birth-giving mothers are (see P96 by mother (gave birth)). The Person being born is linked to the Birth with the property P98 brought into life (was born).
This is not intended for use with general natural history material, only people. There is no explicit method for modelling conception and gestation except by using extensions.
An instance of E67 Birth is normally (but not always) associated with one biological father.'),
	(124, 'P41', 'E1', 'E17', 'classified', 'was classified by', 'This property records the item to which a type was assigned in an E17 Type Assignment activity.
Any instance of a CIDOC CRM entity may be assigned a type through type assignment. Type assignment events allow a more detailed path from E1 CRM Entity through P41i was classified by, E17 Type Assignment, P42 assigned, to E55 Type for assigning types to objects compared to the shortcut offered by P2 has type (is type of).'),
	(125, 'P146', 'E74', 'E86', 'separated from', 'lost member by', 'This property identifies the instance of E74 Group an instance of E39 Actor leaves through an instance of E86 Leaving.
Although a leaving activity normally concerns only one instance of E74 Group, it is possible to imagine circumstances under which leaving one E74 Group implies leaving another E74 Group as well.'),
	(126, 'P186', 'E99', 'E12', 'produced thing of product type', 'is produced by', 'This property associates an instance of E12 Production with the instance of E99 Production Type, that is, the type of the things it produces.'),
	(127, 'P174', 'E2', 'E2', 'starts before the end of', 'ends after the start of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity starts definitely before the end of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-start &lt; B-end is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to a disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets, overlaps, starts, started-by, contains, finishes, finished-by, equals, during, overlapped by}
Typically, this property is a consequence of a known influence of some event on another event or activity, such as a novel written by someone being continued by someone else, or the knowledge of a defeat on a distant battlefield causing people to end their ongoing activities. This property is not transitive.

Figure 10: Temporal entity A starts before the end of temporal entity B. Here A is longer than B

Figure 11: Temporal entity A starts before the end of temporal entity B. Here A is shorter than B'),
	(128, 'P152', 'E21', 'E21', 'has parent', 'is parent of', 'This property associates an instance of E21 Person with another instance of E21 Person who plays the role of the first instance’s parent, regardless of whether the relationship is biological parenthood, assumed or pretended biological parenthood or an equivalent legal status of rights and obligations obtained by a social or legal act.
This property is, among others, a shortcut of the fully developed paths from E21 Person through P98i was born, E67 Birth, P96 by mother to E21 Person, and from E21 Person through P98i was born, E67 Birth, P97 from father to E21 Person.
This property is not transitive.'),
	(129, 'P196', 'E92', 'E18', 'defines', 'is defined by', 'This property associates an instance of E18 Physical Thing with the instance of E92 Spacetime Volume that constitutes the complete trajectory of its geometric extent through spacetime for the whole time of the existence of the instance of E18 Physical Thing.
An instance of E18 Physical Thing not only occupies a particular geometric space at each instant of its existence, but in the course of its existence it also forms a trajectory through spacetime, which occupies a real, that is phenomenal, volume in spacetime, i.e., the instance of E92 Spacetime Volume this property associates it with. This real spatiotemporal extent of the instance of E18 Physical Thing is regarded as being unique, in all its details and fuzziness; the identity and existence of the E92 Spacetime Volume depends uniquely on the identity of the instance of E18 Physical Thing, whose existence defines it. It constitutes a phenomenal spacetime volume as defined in CRMgeo (Doerr &amp; Hiebel, 2013).
Included in this spacetime volume are both the spaces filled by the matter of the physical thing and any inner space that may exist, for instance the interior of a box. Physical things consisting of aggregations of physically unconnected objects, such as a set of chessmen, occupy a finite number of individually contiguous subsets of this spacetime volume equal to the number of objects that constitute the set and that are never connected during its existence.'),
	(130, 'P28', 'E39', 'E10', 'custody surrendered by', 'surrendered custody through', 'This property identifies the instance(s) of E39 Actor who surrender custody of an instance of E18 Physical Thing in an instance of E10 Transfer of Custody.
The property will typically describe an Actor surrendering custody of an object when it is handed over to someone else’s care. On occasion, physical custody may be surrendered involuntarily – through accident, loss or theft.
In reality, custody is either transferred to someone or from someone, or both.'),
	(131, 'P156', 'E53', 'E18', 'occupies', 'is occupied by', 'This property describes the largest volume in space, an instance of E53 Place, that an instance of E18 Physical Thing has occupied at any time during its existence, with respect to the reference space relative to the physical thing itself. This allows for describing the thing itself as a place that may contain other things, such as a box that may contain coins. In other words, it is the volume that contains all the points which the thing has covered at some time during its existence. The reference space for the associated place must be the one that is permanently at rest (P157 is at rest relative to) relative to the physical thing. For instances of E19 Physical Objects it is the one which is at rest relative to the object itself, i.e., which moves together with the object. For instances of E26 Physical Feature it is one which is at rest relative to the physical feature itself and the surrounding matter immediately connected to it. Therefore, there is a 1:1 relation between the instance E18 Physical Thing and the instance of E53 Place it occupies. We include in the occupied space the space filled by the matter of the physical thing and all its inner spaces.
This property implies the fully developed path from E18 Physical Thing through P196 defines, E92 Spacetime Volume, P161 has spatial projection to E53 Place. However, in contrast to P156 occupies, the property P161 has spatial projection does not constrain the reference space of the referred instance of E53 Place.
In contrast to P156 occupies, for the property P53 has former or current location the following holds:
It does not constrain the reference space of the referred instance of E53 Place.
It identifies a possibly wider instance of E53 Place at which a thing is or has been for some unspecified time span.
If the reference space of the referred instance of E53 Place is not at rest with respect to the physical thing found there, the physical thing may move away after some time to another place and/or may have been at some other place before. The same holds for the fully developed path from E18 Physical Thing through P196 defines, E92 Spacetime Volume, P161 has spatial projection to E53 Place.'),
	(132, 'P180', 'E98', 'E97', 'has currency', 'was currency of', 'This property establishes the relationship between an instance of E97 Monetary Amount and the instance of E98 Currency that it is measured in.'),
	(133, 'P50', 'E39', 'E18', 'has current keeper', 'is current keeper of', 'This property identifies the instance of E39 Actor that had custody of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
This property is a shortcut for the more detailed path from E18 Physical Thing through, P30i custody transferred through, E10 Transfer of Custody, P29 custody received by to E39 Actor, if and only if the custody has not been surrendered by the receiving actor at any later time'),
	(134, 'P137', 'E55', 'E1', 'exemplifies', 'is exemplified by', 'This property associates an instance of E1 CRM Entity with an instance of E55 Type for which it has been declared to be a particularly characteristic example.
The P137.1 in the taxonomic role property of P137 exemplifies (is exemplified by) allows differentiation of taxonomic roles. The taxonomic role renders the specific relationship of this example to the type, such as "prototypical", "archetypical", "lectotype", etc. The taxonomic role "lectotype" is not associated with the instance of E83 Type Creation itself but is selected in a later phase.'),
	(135, 'P167', 'E53', 'E93', 'was within', 'includes', 'This property associates an instance of E93 Presence with an instance of E53 Place that geometrically includes the spatial projection of the respective instance of E93 Presence. Besides others, this property may be used to state in which space an object has been for some known time, such as a room of a castle or in a drawer. It may also be used to describe a confinement of the spatial extent of some realm during a known time-span.
This property is a shortcut of the more fully developed path from E93 Presence through P161 has spatial projection, E53 Place, P89 falls within (contains) to E53 Place.'),
	(136, 'P19', 'E71', 'E7', 'was intended use of', 'was made for', 'This property relates an instance of E7 Activity with instances of E71 Human-Made Thing, created specifically for use in the activity.
This is distinct from the intended use of an item in some general type of activity such as the book of common prayer which was intended for use in Church of England services (see P101 had as general use (was use of)).'),
	(137, 'P175', 'E2', 'E2', 'starts before or with the start of', 'starts after or with the start of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity starts before or simultaneously with the start of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-start ≤ B-start is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to a disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets, overlaps, starts, started-by, contains, finished-by, equals}
In a model with fuzzy borders, this property will not be transitive.

Figure 12: Temporal entity A starts before or with the start of temporal entity B. Here A is longer than B

Figure 13: Temporal entity A starts before or with the start of temporal entity B. Here A is shorter than B'),
	(138, 'P182', 'E2', 'E2', 'ends before or with the start of', 'starts after or with the end of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity ends before or simultaneously with the start of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-end ≤ B-start is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to a disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets}.

Figure 16: Temporal entity A ends before or with the start of temporal entity B. Here A is longer than B

Figure 17: Temporal entity A ends before or with the start of temporal entity B. Here A is shorter than B'),
	(139, 'P121', 'E53', 'E53', 'overlaps with', NULL, 'This symmetric property associates an instance of E53 Place with another instance of E53 Place geometrically overlapping it.
It does not specify anything about the shared area. This property is purely spatial. It does not imply that phenomena that define, by their extent, places related by P121 overlaps with have ever covered a common area at the same time or even coexisted. In contrast, spatiotemporal overlaps described by P132 spatiotemporally overlaps are the total of areas simultaneously covered by the related spacetime volumes.
This property is symmetric.'),
	(140, 'P17', 'E1', 'E7', 'was motivated by', 'motivated', 'This property describes an item or items that are regarded as a reason for carrying out the instance of E7 Activity.
For example, the discovery of a large hoard of treasure may call for a celebration, an order from headquarters can start a military manoeuvre.'),
	(141, 'P173', 'E2', 'E2', 'starts before or with the end of', 'ends after or with the start of', 'This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity starts before or simultaneously with the end of the temporal extent of the range instance B of E2 Temporal Entity.
In other words, if A = [A-start, A-end] and B = [B-start, B-end], we mean A-start ≤ B-end is true.
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to the disjunction (logical OR) of the following Allen temporal relations (Allen, 1983): {before, meets, met-by, overlaps, starts, started-by, contains, finishes, finished-by, equals, during, overlapped by}.

Figure 8: Temporal entity A starts before or with the end of temporal entity B. Here A is longer than B

Figure 9: Temporal entity A starts before or with the end of temporal entity B. Here A is shorter than B'),
	(142, 'P33', 'E29', 'E7', 'used specific technique', 'was used by', 'This property identifies a specific instance of E29 Design or Procedure in order to carry out an instance of E7 Activity or parts of it.
The property differs from P32 used general technique (was technique of) in that P33 refers to an instance of E29 Design or Procedure, which is a concrete information object in its own right rather than simply being a term or a method known by tradition.
Typical examples would include intervention plans for conservation or the construction plans of a building.'),
	(143, 'P150', 'E55', 'E55', 'defines typical parts of', 'defines typical wholes for', 'This property associates an instance of E55 Type “A” with an instance of E55 Type “B”, when items of type “A” typically form part of items of type “B”, such as “car motors” and “cars”.
It allows types to be organised into hierarchies based on one type describing a typical part of another. This property is equivalent to "broader term partitive (BTP)" as defined in ISO 2788 and “broaderPartitive” in SKOS.
This property is not transitive.'),
	(144, 'P195', 'E18', 'E93', 'was a presence of', 'had presence', 'This property associates an instance of E93 Presence with the instance of E18 Physical Thing of which it represents a temporal restriction (i.e.: a time-slice) of the thing’s trajectory through spacetime. In other words, it describes where the instance of E18 Physical Thing was or moved around within a given time-span. Instantiating this property constitutes a necessary part of the identity of the respective instance of E93 Presence.
This property is a strong shortcut of the fully developed path from E18 Physical Thing through P196 defines, E92 Spacetime Volume, P166 was a presence of (had presence) to E93 Presence.'),
	(145, 'P198', 'E18', 'E18', 'holds or supports', 'is held or supported by', 'This property relates one instance of E18 Physical Thing which acts as a container or support to a supported or contained instance of E18 Physical Thing. Typical examples of E18 Physical Things which are intended to function as a container or support include shelves, folders or boxes. These containers or supports provide a stable surface which is intended for other physical objects to be placed upon for storage, display, transport or other similar functions.
This property is a shortcut of the more fully developed path from E18 Physical Thing through P59 has section, E53 Place, P53i is former or current location of, to E18 Physical Thing. It is not a sub-property of P46 is composed of, as the held or supported object is not a component of the container or support.
This property can be used to avoid explicitly instantiating the E53 Place which is defined by an instance of E18 Physical Thing, especially when the only intended use of that instance of E18 Physical Thing is to act as a container or surface for the storage of other instances of E18 Physical Thing. The place’s existence is defined by the existence of the container or surface, and will go out of existence at the same time as the destruction of the container or surface.
This property is transitive.'),
	(146, 'P161', 'E53', 'E92', 'has spatial projection', 'is spatial projection of', 'This property associates an instance of an instance of E92 Spacetime Volume with an instance of E53 Place that is the result of the spatial projection of the instance of the E92 Spacetime Volume on a reference space.
In general, there can be more than one useful reference space (for reference space see P156 occupies and P157 is at rest relative to) to describe the spatial projection of a spacetime volume, for example, in describing a sea battle, the difference between the battle ship and the seafloor as reference spaces. Thus, it can be seen that the projection is not unique.
The spatial projection is the actual spatial coverage of a spacetime volume, which normally has fuzzy boundaries except for instances of E92 Spacetime Volumes which are geometrically defined in the same reference system as the range of this property are an exception to this and do not have fuzzy boundaries. Modelling explicitly fuzzy spatial projections serves therefore as a common topological reference of different spatial approximations rather than absolute geometric determination, for instance for relating outer or inner spatial boundaries for the respective spacetime volumes.
In case the domain of an instance of P161 has spatial projection is an instance of E4 Period, the spatial projection describes all areas that period was ever present at, for instance, the Roman Empire.
This property is part of the fully developed path from E18 Physical Thing through P196 defines, E92 Spacetime Volume, P161 has spatial projection to E53 Place, which in turn is implied by P156 occupies (is occupied by).
This property is part of the fully developed path from E4 Period through P161 has spatial projection, E53 Place, P89 falls within (contains) to E53 Place, which in turn is shortcut by P7 took place at (witnessed).'),
	(147, 'P144', 'E74', 'E85', 'joined with', 'gained member by', 'This property identifies the instance of E74 Group of which an instance of E39 Actor becomes a member through an instance of E85 Joining.
Although a joining activity normally concerns only one instance of E74 Group, it is possible to imagine circumstances under which becoming member of one Group implies becoming member of another Group as well.
Joining events allow for describing people becoming members of a group with a more detailed path from E74 Group through, P144i gained member by, E85 Joining, P143 joined, E39 Actor, compared to the shortcut offered by P107 has current or former member (is current or former member of).
The property P144.1 kind of member can be used to specify the type of membership or the role the member has in the group.'),
	(148, 'OA7', 'E39', 'E39', 'has relationship to', NULL, 'OA7 is used to link two Actors (E39) via a certain relationship E39 Actor linked with E39 Actor: E39 (Actor) - P11i (participated in) - E5 (Event) - P11 (had participant) - E39 (Actor) Example: [ Stefan (E21)] participated in [ Relationship from Stefan to Joachim (E5)] had participant [Joachim (E21)] The connecting event is defined by an entity of class E55 (Type): [Relationship from Stefan to Joachim (E5)] has type [Son to Father (E55)]'),
	(149, 'OA8', 'E53', 'E77', ' begins in', NULL, 'OA8 is used to link the beginning of a persistent item''s (E77) life span (or time of usage) with a certain place. E.g to document the birthplace of a person. E77 Persistent Item linked with a E53 Place: E77 (Persistent Item) - P92i (was brought into existence by) - E63 (Beginning of Existence) - P7 (took place at) - E53 (Place) Example: [Albert Einstein (E21)] was brought into existence by [Birth of Albert Einstein (E12)] took place at [Ulm (E53)]'),
	(150, 'OA9', 'E53', 'E77', ' begins in', NULL, 'OA9 is used to link the end of a persistent item''s (E77) life span (or time of usage) with a certain place. E.g to document a person''s place of death. E77 Persistent Item linked with a E53 Place: E77 (Persistent Item) - P93i (was taken out of existence by) - E64 (End of Existence) - P7 (took place at) - E53 (Place) Example: [Albert Einstein (E21)] was taken out of by [Death of Albert Einstein (E12)] took place at [Princeton (E53)]');

INSERT INTO model.property_inheritance (id, super_code, sub_code) VALUES
	(1, 'P12', 'P92'),
	(2, 'P14', 'P29'),
	(3, 'P53', 'P55'),
	(4, 'P12', 'P25'),
	(5, 'P140', 'P39'),
	(6, 'P182', 'P183'),
	(7, 'P14', 'P23'),
	(8, 'P92', 'P123'),
	(9, 'P67', 'P71'),
	(10, 'P46', 'P56'),
	(11, 'P1', 'P102'),
	(12, 'P93', 'P100'),
	(13, 'P174', 'P184'),
	(14, 'P141', 'P37'),
	(15, 'P16', 'P142'),
	(16, 'P105', 'P52'),
	(17, 'P51', 'P52'),
	(18, 'P92', 'P98'),
	(19, 'P184', 'P185'),
	(20, 'P12', 'P93'),
	(21, 'P31', 'P108'),
	(22, 'P92', 'P108'),
	(23, 'P67', 'P68'),
	(24, 'P141', 'P35'),
	(25, 'P130', 'P73'),
	(26, 'P93', 'P13'),
	(27, 'P15', 'P136'),
	(28, 'P132', 'P10'),
	(29, 'P92', 'P95'),
	(30, 'P11', 'P145'),
	(31, 'P94', 'P135'),
	(32, 'P10', 'P9'),
	(33, 'P67', 'P138'),
	(34, 'P14', 'P22'),
	(35, 'P130', 'P128'),
	(36, 'P16', 'P111'),
	(37, 'P93', 'P124'),
	(38, 'P157', 'P59'),
	(39, 'P12', 'P16'),
	(40, 'P15', 'P16'),
	(41, 'P141', 'P38'),
	(42, 'P141', 'P40'),
	(43, 'P2', 'P177'),
	(44, 'P11', 'P96'),
	(45, 'P11', 'P143'),
	(46, 'P106', 'P165'),
	(47, 'P67', 'P129'),
	(48, 'P12', 'P11'),
	(49, 'P160', 'P164'),
	(50, 'P15', 'P134'),
	(51, 'P176', 'P134'),
	(52, 'P11', 'P14'),
	(53, 'P12', 'P31'),
	(54, 'P92', 'P94'),
	(55, 'P11', 'P151'),
	(56, 'P31', 'P112'),
	(57, 'P125', 'P32'),
	(58, 'P31', 'P110'),
	(59, 'P12', 'P113'),
	(60, 'P49', 'P109'),
	(61, 'P141', 'P42'),
	(62, 'P128', 'P65'),
	(63, 'P175', 'P176'),
	(64, 'P140', 'P34'),
	(65, 'P67', 'P70'),
	(66, 'P93', 'P99'),
	(67, 'P11', 'P99'),
	(68, 'P1', 'P48'),
	(69, 'P10', 'P166'),
	(70, 'P140', 'P41'),
	(71, 'P11', 'P146'),
	(72, 'P173', 'P174'),
	(73, 'P14', 'P28'),
	(74, 'P53', 'P156'),
	(75, 'P157', 'P156'),
	(76, 'P91', 'P180'),
	(77, 'P49', 'P50'),
	(78, 'P2', 'P137'),
	(79, 'P174', 'P175'),
	(80, 'P176', 'P182'),
	(81, 'P185', 'P182'),
	(82, 'P15', 'P17'),
	(83, 'P16', 'P33'),
	(84, 'P7', 'P161'),
	(85, 'P11', 'P144');

INSERT INTO model.property_i18n (id, property_code, language_code, text, text_inverse) VALUES
	(1, 'P92', 'de', 'brachte in Existenz', 'wurde in Existenz gebracht durch'),
	(2, 'P92', 'en', 'brought into existence', 'was brought into existence by'),
	(3, 'P92', 'fr', 'a fait exister', 'a commencé à exister du fait de'),
	(4, 'P92', 'ru', 'создал', 'был создан посредством'),
	(5, 'P92', 'el', 'γέννησε', 'γεννήθηκε από'),
	(6, 'P92', 'pt', 'trouxe à existência', 'passou a existir por'),
	(7, 'P92', 'zh', '导致存在的是', '使导致存在'),
	(8, 'P101', 'de', 'hatte die allgemeine Verwendung', 'war die Verwendung von'),
	(9, 'P101', 'en', 'had as general use', 'was use of'),
	(10, 'P101', 'fr', 'avait comme utilisation générale', 'était l’utilisation de'),
	(11, 'P101', 'ru', 'имел основное применение', 'был применением для'),
	(12, 'P101', 'el', 'είχε ως γενική χρήση', 'ήταν χρήση του/της'),
	(13, 'P101', 'pt', 'tem como uso geral', 'foi uso de'),
	(14, 'P101', 'zh', '有一般用途', '被用于'),
	(15, 'P46', 'de', 'ist zusammengesetzt aus', 'bildet Teil von'),
	(16, 'P46', 'en', 'is composed of', 'forms part of'),
	(17, 'P46', 'fr', 'est composée de', 'fait partie de'),
	(18, 'P46', 'ru', 'составлен из', 'формирует часть'),
	(19, 'P46', 'el', 'αποτελείται από', 'αποτελεί μέρος του/της'),
	(20, 'P46', 'pt', 'é composto de', 'faz parte de'),
	(21, 'P46', 'zh', '组成成分是', '构成部分'),
	(22, 'P29', 'de', 'übertrug Gewahrsam auf', 'erhielt Gewahrsam durch'),
	(23, 'P29', 'en', 'custody received by', 'received custody through'),
	(24, 'P29', 'fr', 'changement de détenteur au profit de', 'est devenu détenteur grâce à'),
	(25, 'P29', 'ru', 'опека получена', 'получил опеку через'),
	(26, 'P29', 'el', 'μετεβίβασε κατοχή σε', 'παρέλαβε κατοχή μέσω'),
	(27, 'P29', 'pt', 'custódia recebida por', 'início da custódia por meio de'),
	(28, 'P29', 'zh', '监护权转至', '获得监护权'),
	(29, 'P55', 'de', 'hat derzeitigen Standort', 'hält derzeitig'),
	(30, 'P55', 'en', 'has current location', 'currently holds'),
	(31, 'P55', 'fr', 'a pour localisation actuelle', 'est localisation actuelle de'),
	(32, 'P55', 'ru', 'в данный момент находится в', 'в данный момент содержит'),
	(33, 'P55', 'el', 'βρίσκεται σε', 'είναι θέση του'),
	(34, 'P55', 'pt', 'é localizado em', 'é localização atual de'),
	(35, 'P55', 'zh', '有当前位置', '当前拥有'),
	(36, 'P141', 'de', 'wies zu', 'wurde zugewiesen durch'),
	(37, 'P141', 'en', 'assigned', 'was assigned by'),
	(38, 'P141', 'fr', 'a attribué', 'a été attribué par'),
	(39, 'P141', 'ru', 'присвоил', 'был присвоен посредством'),
	(40, 'P141', 'el', 'απέδωσε', 'αποδόθηκε από'),
	(41, 'P141', 'pt', 'atribuiu', 'foi atribuído por'),
	(42, 'P141', 'zh', '分配', '被分配'),
	(43, 'P25', 'de', 'bewegte', 'wurde bewegt durch'),
	(44, 'P25', 'en', 'moved', 'moved by'),
	(45, 'P25', 'fr', 'a déplacé', 'a été déplacé par'),
	(46, 'P25', 'ru', 'переместил', 'перемещен посредством'),
	(47, 'P25', 'el', 'μετεκίνησε', 'μετακινήθηκε από'),
	(48, 'P25', 'pt', 'locomoveu', 'foi locomovido por'),
	(49, 'P25', 'zh', '移动', '被移动'),
	(50, 'P39', 'de', 'vermaß', 'wurde vermessen durch'),
	(51, 'P39', 'en', 'measured', 'was measured by'),
	(52, 'P39', 'fr', 'a mesuré', 'a été mesuré par'),
	(53, 'P39', 'ru', 'измерил', 'был измерен посредством'),
	(54, 'P39', 'el', 'μέτρησε', 'μετρήθηκε από'),
	(55, 'P39', 'pt', 'mediu', 'foi medida por'),
	(56, 'P39', 'zh', '测量了', '被测量'),
	(57, 'P183', 'en', 'ends before the start of', 'starts after the end of'),
	(58, 'P23', 'de', 'übertrug Besitztitel von', 'trat Besitztitel ab in'),
	(59, 'P23', 'en', 'transferred title from', 'surrendered title through'),
	(60, 'P23', 'fr', 'a fait passer le droit de propriété de', 'a perdu le droit de propriété du fait de'),
	(61, 'P23', 'ru', 'передал право собственности от', 'право собственности отдано через'),
	(62, 'P23', 'el', 'μετεβίβασε τον τίτλο από', 'παρέδωσε τον τίτλο μέσω'),
	(63, 'P23', 'pt', 'transferiu os direitos de propriedade de', 'perdeu os direitos de propriedade por meio da'),
	(64, 'P23', 'zh', '转移所有权自', '出让所有权'),
	(65, 'P104', 'de', 'Gegenstand von', 'findet Anwendung auf'),
	(66, 'P104', 'en', 'is subject to', 'applies to'),
	(67, 'P104', 'fr', 'est sujet à', 's’applique à'),
	(68, 'P104', 'ru', 'является объектом для', 'применяется к'),
	(69, 'P104', 'el', 'υπόκειται σε', 'ισχύει για'),
	(70, 'P104', 'pt', 'está sujeito à', 'se aplicam à'),
	(71, 'P104', 'zh', '服从', '适用于'),
	(72, 'P123', 'de', 'ergab', 'ergab sich aus'),
	(73, 'P123', 'en', 'resulted in', 'resulted from'),
	(74, 'P123', 'fr', 'a eu pour résultat', 'est le résultat de'),
	(75, 'P123', 'ru', 'повлек появление', 'был результатом'),
	(76, 'P123', 'el', 'είχε ως αποτέλεσμα', 'προέκυψε από'),
	(77, 'P123', 'pt', 'resultou em', 'resultado de'),
	(78, 'P123', 'zh', '结果造成', '起因于'),
	(79, 'P148', 'de', 'hat Bestandteil', 'ist Bestandteil von'),
	(80, 'P148', 'en', 'has component', 'is component of'),
	(81, 'P148', 'zh', '有组件', '是组件'),
	(82, 'P71', 'de', 'listet', 'wird aufgelistet in'),
	(83, 'P71', 'en', 'lists', 'is listed in'),
	(84, 'P71', 'fr', 'définit', 'est défini par'),
	(85, 'P71', 'ru', 'перечисляет', 'перечислен в'),
	(86, 'P71', 'el', 'περιλαμβάνει', 'περιλαμβάνεται σε'),
	(87, 'P71', 'pt', 'define', 'é definido por'),
	(88, 'P71', 'zh', '列出', '列于'),
	(89, 'P75', 'de', 'besitzt', 'sind im Besitz von'),
	(90, 'P75', 'en', 'possesses', 'is possessed by'),
	(91, 'P75', 'fr', 'est détenteur de', 'est détenu par'),
	(92, 'P75', 'ru', 'владеет', 'принадлежит'),
	(93, 'P75', 'el', 'κατέχει', 'κατέχεται από'),
	(94, 'P75', 'pt', 'é detentor de', 'são detidos por'),
	(95, 'P75', 'zh', '拥有', '被拥有'),
	(96, 'P56', 'de', 'trägt Merkmal', 'wird gefunden auf'),
	(97, 'P56', 'en', 'bears feature', 'is found on'),
	(98, 'P56', 'fr', 'présente pour caractéristique', 'se trouve sur'),
	(99, 'P56', 'ru', 'несет признак', 'найден на'),
	(100, 'P56', 'el', 'φέρει μόρφωμα', 'βρίσκεται σε'),
	(101, 'P56', 'pt', 'possui característica', 'é encontrada em'),
	(102, 'P56', 'zh', '有特征', '发现于'),
	(103, 'P102', 'de', 'trägt den Titel', 'ist der Titel von'),
	(104, 'P102', 'en', 'has title', 'is title of'),
	(105, 'P102', 'fr', 'a pour titre', 'est le titre de'),
	(106, 'P102', 'ru', 'имеет заголовок', 'является заголовком для'),
	(107, 'P102', 'el', 'έχει τίτλο', 'είναι τίτλος του/της'),
	(108, 'P102', 'pt', 'tem título', 'é título de'),
	(109, 'P102', 'zh', '有题名', '题名是'),
	(110, 'P100', 'de', 'Tod von', 'starb in'),
	(111, 'P100', 'en', 'was death of', 'died in'),
	(112, 'P100', 'fr', 'a été la mort de', 'est mort par'),
	(113, 'P100', 'ru', 'был смертью для', 'умер в'),
	(114, 'P100', 'el', 'ήταν θάνατος του/της', 'πέθανε σε'),
	(115, 'P100', 'pt', 'foi a morte para', 'morreu em'),
	(116, 'P100', 'zh', '死亡的是', '死于'),
	(117, 'P184', 'en', 'ends before or with the end of', 'ends with or after the end of'),
	(118, 'P1', 'de', 'wird bezeichnet als', 'bezeichnet'),
	(119, 'P1', 'en', 'is identified by', 'identifies'),
	(120, 'P1', 'fr', 'est identifiée par', 'identifie'),
	(121, 'P1', 'ru', 'идентифицируется посредством', 'идентифицирует'),
	(122, 'P1', 'el', 'αναγνωρίζεται ως', 'είναι αναγνωριστικό'),
	(123, 'P1', 'pt', 'é identificado por', 'identifica'),
	(124, 'P1', 'zh', '被标识为', '标识'),
	(125, 'P76', 'de', 'hat Kontaktpunkt', 'bietet Zugang zu'),
	(126, 'P76', 'en', 'has contact point', 'provides access to'),
	(127, 'P76', 'fr', 'a pour coordonnées individuelles', 'permettent de contacter'),
	(128, 'P76', 'ru', 'имеет контакт', 'предоставляет доступ к'),
	(129, 'P76', 'el', 'έχει σημείο επικοινωνίας', 'παρέχει πρόσβαση σε'),
	(130, 'P76', 'pt', 'possui ponto de contato', 'é ponto de contado de'),
	(131, 'P76', 'zh', '有联系方式', '提供访问'),
	(132, 'P139', 'de', 'hat alternative Form', NULL),
	(133, 'P139', 'en', 'has alternative form', NULL),
	(134, 'P139', 'fr', 'a pour autre forme', NULL),
	(135, 'P139', 'ru', 'имеет альтернативную форму', NULL),
	(136, 'P139', 'el', 'έχει εναλλακτική μορφή', NULL),
	(137, 'P139', 'pt', 'tem forma alternativa', NULL),
	(138, 'P139', 'zh', '有交替形式', NULL),
	(139, 'P37', 'de', 'wies zu', 'wurde zugewiesen durch'),
	(140, 'P37', 'en', 'assigned', 'was assigned by'),
	(141, 'P37', 'fr', 'a attribué', 'a été attribuée par'),
	(142, 'P37', 'ru', 'назначил', 'был присвоен посредством'),
	(143, 'P37', 'el', 'απέδωσε', 'αποδόθηκε ως ιδιότητα από'),
	(144, 'P37', 'pt', 'atribuiu', 'foi atribuído por'),
	(145, 'P37', 'zh', '分配了', '被分配'),
	(146, 'P142', 'de', 'benutzte Bestandteil', 'wurde benutzt in'),
	(147, 'P142', 'en', 'used constituent', 'was used in'),
	(148, 'P142', 'zh', '使用构成成分', '用于'),
	(149, 'P7', 'de', 'fand statt in', 'bezeugte'),
	(150, 'P7', 'en', 'took place at', 'witnessed'),
	(151, 'P7', 'fr', 'a eu lieu dans', 'a été témoin de'),
	(152, 'P7', 'ru', 'совершался на', 'был местом совершения'),
	(153, 'P7', 'el', 'έλαβε χώρα σε', 'υπήρξε τόπος του'),
	(154, 'P7', 'pt', 'ocorreu em', 'testemunhou'),
	(155, 'P7', 'zh', '发生地在', '发生过'),
	(156, 'P140', 'de', 'wies Merkmal zu', 'bekam Merkmal zugewiesen durch'),
	(157, 'P140', 'en', 'assigned attribute to', 'was attributed by'),
	(158, 'P140', 'fr', 'a affecté un attribut à', 'a reçu un attribut par'),
	(159, 'P140', 'ru', 'присвоил атрибут для', 'получил атрибут посредством'),
	(160, 'P140', 'el', 'απέδωσε ιδιότητα σε', 'χαρακτηρίστηκε από'),
	(161, 'P140', 'pt', 'atribuiu atributo para', 'foi atribuído por'),
	(162, 'P140', 'zh', '分配属性于', '接受属性'),
	(163, 'P52', 'de', 'hat derzeitigen Besitzer', 'ist derzeitiger Besitzer von'),
	(164, 'P52', 'en', 'has current owner', 'is current owner of'),
	(165, 'P52', 'fr', 'est actuellement possédée par', 'est le propriétaire actuel de'),
	(166, 'P52', 'ru', 'имеет текущего владельца', 'является текущим владельцем для'),
	(167, 'P52', 'el', 'έχει ιδιοκτήτη', 'είναι ιδιοκτήτης του'),
	(168, 'P52', 'pt', 'é propriedade de', 'é proprietário de'),
	(169, 'P52', 'zh', '有当前所有者', '是当前所有者'),
	(170, 'P98', 'de', 'brachte zur Welt', 'wurde geboren durch'),
	(171, 'P98', 'en', 'brought into life', 'was born'),
	(172, 'P98', 'fr', 'a donné vie à', 'est né'),
	(173, 'P98', 'ru', 'породил', 'был рожден'),
	(174, 'P98', 'el', 'έφερε στη ζωή', 'γεννήθηκε'),
	(175, 'P98', 'pt', 'trouxe à vida', 'veio à vida pelo'),
	(176, 'P98', 'zh', '诞生了', '被诞生'),
	(177, 'P185', 'en', 'ends before the end of', 'ends after the end of'),
	(178, 'P21', 'de', 'hatte den allgemeinen Zweck', 'war Zweck von'),
	(179, 'P21', 'en', 'had general purpose', 'was purpose of'),
	(180, 'P21', 'fr', 'avait pour but général', 'était le but de'),
	(181, 'P21', 'ru', 'имел общую цель', 'был целью для'),
	(182, 'P21', 'el', 'είχε γενικό σκοπό', 'ήταν σκοπός του/της'),
	(183, 'P21', 'pt', 'tinha propósito geral', 'era o propósito de'),
	(184, 'P21', 'zh', '有一般目的', '是为了'),
	(185, 'P93', 'de', 'beendete die Existenz von', 'wurde seiner Existenz beraubt durch'),
	(186, 'P93', 'en', 'took out of existence', 'was taken out of existence by'),
	(187, 'P93', 'fr', 'a fait cesser d’exister', 'a cessé d’exister du fait de'),
	(188, 'P93', 'ru', 'положил конец существованию', 'прекратил существование посредством'),
	(189, 'P93', 'el', 'αναίρεσε', 'αναιρέθηκε από'),
	(190, 'P93', 'pt', 'cessou a existência de', 'deixou de existir'),
	(191, 'P93', 'zh', '结束存在的是', '被结束存在'),
	(192, 'P108', 'de', 'hat hergestellt', 'wurde hergestellt durch'),
	(193, 'P108', 'en', 'has produced', 'was produced by'),
	(194, 'P108', 'fr', 'a produit', 'a été produit par'),
	(195, 'P108', 'ru', 'произвел', 'был произведен посредством'),
	(196, 'P108', 'el', 'παρήγαγε', 'παρήχθη από'),
	(197, 'P108', 'pt', 'produziu', 'foi produzido por'),
	(198, 'P108', 'zh', '已产生了', '被产生'),
	(199, 'P54', 'de', 'hat derzeitigen permanenten Standort', 'ist derzeitiger permanenter Standort von'),
	(200, 'P54', 'en', 'has current permanent location', 'is current permanent location of'),
	(201, 'P54', 'fr', 'a actuellement pour localisation à demeure', 'est actuellement localisation à demeure de'),
	(202, 'P54', 'ru', 'имеет текущее постоянное местоположение', 'является текущим постоянным местоположением для'),
	(203, 'P54', 'el', 'έχει μόνιμη θέση', 'είναι μόνιμη θέση του/της'),
	(204, 'P54', 'pt', 'é localizado permanentemente em', 'é localização permanente de'),
	(205, 'P54', 'zh', '有当前永久位置', '是当前永久位置'),
	(206, 'P69', 'de', 'ist verbunden mit', NULL),
	(207, 'P69', 'en', 'has association with', 'is associated with'),
	(208, 'P69', 'fr', 'est associée à', NULL),
	(209, 'P69', 'ru', 'ассоциирован с', NULL),
	(210, 'P69', 'el', 'σχετίζεται με', NULL),
	(211, 'P69', 'pt', 'é associado com', NULL),
	(212, 'P69', 'zh', '关联', NULL),
	(213, 'P105', 'de', 'Rechte stehen zu', 'hat Rechte an'),
	(214, 'P105', 'en', 'right held by', 'has right on'),
	(215, 'P105', 'fr', 'droit détenu par', 'détient un droit sur'),
	(216, 'P105', 'ru', 'право принадлежит', 'владеет правом на'),
	(217, 'P105', 'el', 'δικαίωμα κατέχεται από', 'έχει δικαίωμα σε'),
	(218, 'P105', 'pt', 'são direitos de', 'possui direitos sobre'),
	(219, 'P105', 'zh', '持有权利的是', '有权利'),
	(220, 'P68', 'de', 'sieht den Gebrauch vor von', 'vorgesehen für Gebrauch durch defined'),
	(221, 'P68', 'en', 'foresees use of', 'use foreseen by'),
	(222, 'P68', 'fr', 'utilise habituellement', 'est habituellement utilisé par'),
	(223, 'P68', 'ru', 'обычно применяет', 'обычно используется посредством'),
	(224, 'P68', 'el', 'συνήθως χρησιμοποιεί', 'συνήθως χρησιμοποιείται από'),
	(225, 'P68', 'pt', 'normalmente emprega', 'é empregado por'),
	(226, 'P68', 'zh', '预知使用', '被预知使用'),
	(227, 'P35', 'de', 'hat identifiziert', 'wurde identifiziert durch'),
	(228, 'P35', 'en', 'has identified', 'was identified by'),
	(229, 'P35', 'fr', 'a identifié', 'est identifié par'),
	(230, 'P35', 'ru', 'идентифицировал', 'идентифицирован посредством'),
	(231, 'P35', 'el', 'έχει διαπιστώσει', 'έχει διαπιστωθεί από'),
	(232, 'P35', 'pt', 'identificou', 'foi identificado por'),
	(233, 'P35', 'zh', '有标识', '被标识'),
	(234, 'P73', 'de', 'hat Übersetzung', 'ist Übersetzung von'),
	(235, 'P73', 'en', 'has translation', 'is translation of'),
	(236, 'P73', 'fr', 'a pour traduction', 'est la traduction de'),
	(237, 'P73', 'ru', 'имеет перевод', 'является переводом'),
	(238, 'P73', 'el', 'έχει μετάφραση', 'είναι μετάφραση του/της'),
	(239, 'P73', 'pt', 'tem tradução', 'é tradução de'),
	(240, 'P73', 'zh', '有译文', '是译文'),
	(241, 'P13', 'de', 'zerstörte', 'wurde zerstört durch'),
	(242, 'P13', 'en', 'destroyed', 'was destroyed by'),
	(243, 'P13', 'fr', 'a détruit', 'a été détruite par'),
	(244, 'P13', 'ru', 'уничтожил', 'был уничтожен посредством'),
	(245, 'P13', 'el', 'κατέστρεψε', 'καταστράφηκε από'),
	(246, 'P13', 'pt', 'destruiu', 'foi destruído por'),
	(247, 'P13', 'zh', '破坏了', '被破坏'),
	(248, 'P136', 'de', 'stützte sich auf', 'belegte'),
	(249, 'P136', 'en', 'was based on', 'supported type creation'),
	(250, 'P136', 'fr', 's’est fondée sur', 'a justifié la création de type'),
	(251, 'P136', 'ru', 'был основан на', 'поддержал создание типа'),
	(252, 'P136', 'el', 'βασίστηκε σε', 'υποστήριξε τη δημιουργία τύπου'),
	(253, 'P136', 'pt', 'foi baseado em', 'suportou a criação de tipo'),
	(254, 'P136', 'zh', '基于', '支持类型创建'),
	(255, 'P10', 'de', 'fällt in', 'enthält'),
	(256, 'P10', 'en', 'falls within', 'contains'),
	(257, 'P10', 'fr', 's’insère dans le cours de', 'contient'),
	(258, 'P10', 'ru', 'находится в пределах', 'содержит'),
	(259, 'P10', 'el', 'εμπίπτει', 'περιλαμβάνει'),
	(260, 'P10', 'pt', 'está contido em', 'contém'),
	(261, 'P10', 'zh', '属于', '包含'),
	(262, 'P8', 'de', 'fand statt auf oder innerhalb von', 'bezeugte'),
	(263, 'P8', 'en', 'took place on or within', 'witnessed'),
	(264, 'P8', 'fr', 'a eu lieu sur ou dans', 'a été témoin de'),
	(265, 'P8', 'ru', 'имел место на или в', 'являлся местом для'),
	(266, 'P8', 'el', 'έλαβε χώρα σε ή εντός', 'υπήρξε τόπος του'),
	(267, 'P8', 'pt', 'ocorreu em ou dentro', 'testemunhou'),
	(268, 'P8', 'zh', '发生的所在对象是', '发生过'),
	(269, 'P95', 'de', 'hat gebildet', 'wurde gebildet von'),
	(270, 'P95', 'en', 'has formed', 'was formed by'),
	(271, 'P95', 'fr', 'a fondé', 'a été fondé par'),
	(272, 'P95', 'ru', 'сформировал', 'была сформирована посредством'),
	(273, 'P95', 'el', 'σχημάτισε', 'σχηματίστηκε από'),
	(274, 'P95', 'pt', 'formou', 'foi formado por'),
	(275, 'P95', 'zh', '已经组成', '被组成'),
	(276, 'P132', 'en', 'spatiotemporally overlaps with', NULL),
	(277, 'P145', 'de', 'entließ', 'wurde entlassen durch'),
	(278, 'P145', 'en', 'separated', 'left by'),
	(279, 'P145', 'zh', '离开', '留下'),
	(280, 'P74', 'de', 'hat derzeitigen oder früheren Sitz', 'ist derzeitiger oder früherer Sitz von'),
	(281, 'P74', 'en', 'has current or former residence', 'is current or former residence of'),
	(282, 'P74', 'fr', 'réside ou a résidé à', 'est ou a été la résidence de'),
	(283, 'P74', 'ru', 'имеет текущее или бывшее местожительства', 'является текущим или бывшим местом жительства для'),
	(284, 'P74', 'el', 'έχει ή είχε κατοικία', 'είναι ή ήταν κατοικία του/της'),
	(285, 'P74', 'pt', 'reside ou residiu em', 'é ou foi residência de'),
	(286, 'P74', 'zh', '有当前或曾经居住地', '是当前或曾经居住地'),
	(287, 'P135', 'de', 'erschuf Typus', 'wurde geschaffen durch'),
	(288, 'P135', 'en', 'created type', 'was created by'),
	(289, 'P135', 'fr', 'a créé le type', 'a été créé par'),
	(290, 'P135', 'ru', 'создал тип', 'был создан посредством'),
	(291, 'P135', 'el', 'δημιούργησε τύπο', 'δημιουργήθηκε από'),
	(292, 'P135', 'pt', 'criou tipo', 'foi criado por'),
	(293, 'P135', 'zh', '创建类型', '被创建'),
	(294, 'P72', 'de', 'hat Sprache', 'ist Sprache von'),
	(295, 'P72', 'en', 'has language', 'is language of'),
	(296, 'P72', 'fr', 'est en langue', 'est la langue de'),
	(297, 'P72', 'ru', 'имеет язык', 'является языком для'),
	(298, 'P72', 'el', 'έχει γλώσσα', 'είναι γλώσσα του/της'),
	(299, 'P72', 'pt', 'é da língua', 'é a língua de'),
	(300, 'P72', 'zh', '有语种', '是语种'),
	(301, 'P9', 'de', 'setzt sich zusammen aus', 'bildet Teil von'),
	(302, 'P9', 'en', 'consists of', 'forms part of'),
	(303, 'P9', 'fr', 'consiste en', 'fait partie de'),
	(304, 'P9', 'ru', 'состоит из', 'формирует часть'),
	(305, 'P9', 'el', 'αποτελείται από', 'αποτελεί μέρος του/της'),
	(306, 'P9', 'pt', 'consiste de', 'faz parte de'),
	(307, 'P9', 'zh', '包括', '组成部分'),
	(308, 'P138', 'de', 'stellt dar', 'wird dargestellt durch'),
	(309, 'P138', 'en', 'represents', 'has representation'),
	(310, 'P138', 'fr', 'représente', 'est représentée par'),
	(311, 'P138', 'ru', 'представляет', 'имеет представление'),
	(312, 'P138', 'el', 'παριστάνει', 'παριστάνεται από'),
	(313, 'P138', 'pt', 'representa', 'tem representação'),
	(314, 'P138', 'zh', '描绘', '有描绘'),
	(315, 'P43', 'de', 'hat Dimension', 'ist Dimension von'),
	(316, 'P43', 'en', 'has dimension', 'is dimension of'),
	(317, 'P43', 'fr', 'a pour dimension', 'est dimension de'),
	(318, 'P43', 'ru', 'имеет величину', 'является величиной для'),
	(319, 'P43', 'el', 'έχει μέγεθος', 'είναι μέγεθος του'),
	(320, 'P43', 'pt', 'tem dimensão', 'é dimensão de'),
	(321, 'P43', 'zh', '有度量规格', '是度量规格'),
	(322, 'P49', 'de', 'hat früheren oder derzeitigen Betreuer', 'ist früherer oder derzeitiger Betreuer von'),
	(323, 'P49', 'en', 'has former or current keeper', 'is former or current keeper of'),
	(324, 'P49', 'fr', 'est ou a été détenu par', 'est ou a été détenteur de'),
	(325, 'P49', 'ru', 'имеет бывшего или текущего смотрителя', 'является бывшим или текущим смотрителем для'),
	(326, 'P49', 'el', 'είναι ή ήταν στην κατοχή του', 'κατέχει ή κατείχε'),
	(327, 'P49', 'pt', 'é ou foi guardada por', 'é ou foi guardador de'),
	(328, 'P49', 'zh', '有以往或当前保管者', '是以往或当前保管者'),
	(329, 'P22', 'de', 'übertrug Besitztitel auf', 'erwarb Besitztitel durch'),
	(330, 'P22', 'en', 'transferred title to', 'acquired title through'),
	(331, 'P22', 'fr', 'a fait passer le droit de propriété à', 'a acquis le droit de propriété du fait de'),
	(332, 'P22', 'ru', 'передал право собственности', 'получил право собственности через'),
	(333, 'P22', 'el', 'μετεβίβασε τον τίτλο σε', 'απέκτησε τον τίτλο μέσω'),
	(334, 'P22', 'pt', 'transferiu os direitos de propriedade para', 'adquiriu os direitos de propriedade por meio da'),
	(335, 'P22', 'zh', '转移所有权至', '获得所有权'),
	(336, 'P128', 'de', 'trägt', 'wird getragen von'),
	(337, 'P128', 'en', 'carries', 'is carried by'),
	(338, 'P128', 'fr', 'est le support de', 'a pour support'),
	(339, 'P128', 'ru', 'несет', 'переносится посредством'),
	(340, 'P128', 'el', 'φέρει', 'φέρεται από'),
	(341, 'P128', 'pt', 'é o suporte de', 'é suportado por'),
	(342, 'P128', 'zh', '承载', '被承载'),
	(343, 'P147', 'de', 'betreute kuratorisch', 'wurde kuratorisch betreut durch'),
	(344, 'P147', 'en', 'curated', 'was curated by'),
	(345, 'P147', 'zh', '管理', '被管理'),
	(346, 'P111', 'de', 'fügte hinzu', 'wurde hinzugefügt durch'),
	(347, 'P111', 'en', 'added', 'was added by'),
	(348, 'P111', 'fr', 'a ajouté', 'a été ajouté par'),
	(349, 'P111', 'ru', 'добавил', 'был добавлен посредством'),
	(350, 'P111', 'el', 'προσέθεσε', 'προστέθηκε από'),
	(351, 'P111', 'pt', 'adicionou', 'foi adicionado por'),
	(352, 'P111', 'zh', '增加了', '被增加'),
	(353, 'P91', 'de', 'hat Einheit', 'ist Einheit von'),
	(354, 'P91', 'en', 'has unit', 'is unit of'),
	(355, 'P91', 'fr', 'a pour unité', 'est l''unité de'),
	(356, 'P91', 'ru', 'имеет единицу', 'является единицей для'),
	(357, 'P91', 'el', 'έχει μονάδα μέτρησης', 'αποτελεί μονάδα μέτρησης του/της'),
	(358, 'P91', 'pt', 'tem unidade', 'é unidade de'),
	(359, 'P91', 'zh', '有单位', '所属单位'),
	(360, 'P191', 'en', 'had duration', 'was duration of'),
	(361, 'P53', 'de', 'hat früheren oder derzeitigen Standort', 'ist früherer oder derzeitiger Standort von'),
	(362, 'P53', 'en', 'has former or current location', 'is former or current location of'),
	(363, 'P53', 'fr', 'a ou a eu pour localisation', 'est ou a été localisation de'),
	(364, 'P53', 'ru', 'имеет текущее или бывшее местоположение', 'является текущим или бывшим местоположением для'),
	(365, 'P53', 'el', 'βρίσκεται ή βρισκόταν σε', 'είναι ή ήταν θέση του'),
	(366, 'P53', 'pt', 'é ou foi localizada em', 'é ou foi localização de'),
	(367, 'P53', 'zh', '有之前或当前位置', '是之前或当前位置'),
	(368, 'P12', 'de', 'fand statt im Beisein von', 'war anwesend bei'),
	(369, 'P12', 'en', 'occurred in the presence of', 'was present at'),
	(370, 'P12', 'fr', 'est arrivé en présence de', 'était présent à'),
	(371, 'P12', 'ru', 'появился в присутствии', 'присутствовал при'),
	(372, 'P12', 'el', 'συνέβη παρουσία του/της', 'ήταν παρών/παρούσα/παρόν σε'),
	(373, 'P12', 'pt', 'ocorreu na presença de', 'estava presente no'),
	(374, 'P12', 'zh', '已出现', '出现在'),
	(375, 'P189', 'en', 'approximates', 'is approximated by'),
	(376, 'P124', 'de', 'wandelte um', 'wurde umgewandelt durch'),
	(377, 'P124', 'en', 'transformed', 'was transformed by'),
	(378, 'P124', 'fr', 'a transformé', 'a été transformé par'),
	(379, 'P124', 'ru', 'трансформировал', 'был трансформирован посредством'),
	(380, 'P124', 'el', 'μετέτρεψε', 'μετατράπηκε από'),
	(381, 'P124', 'pt', 'transformou', 'foi transformado por'),
	(382, 'P124', 'zh', '转变了', '被转变'),
	(383, 'P20', 'de', 'hatte den bestimmten Zweck', 'war Zweck von'),
	(384, 'P20', 'en', 'had specific purpose', 'was purpose of'),
	(385, 'P20', 'fr', 'avait pour but spécifique', 'était le but de'),
	(386, 'P20', 'ru', 'имел конкретную цель', 'был целью для'),
	(387, 'P20', 'el', 'είχε συγκεκριμένο σκοπό', 'ήταν σκοπός του/της'),
	(388, 'P20', 'pt', 'tinha propósito específico', 'era o propósito de'),
	(389, 'P20', 'zh', '有特定目的', '是为了'),
	(390, 'P59', 'de', 'hat Bereich', 'befindet sich auf oder in'),
	(391, 'P59', 'en', 'has section', 'is located on or within'),
	(392, 'P59', 'fr', 'a pour section', 'se situe sur ou dans'),
	(393, 'P59', 'ru', 'имеет район', 'находится на или внутри'),
	(394, 'P59', 'el', 'έχει τομέα', 'βρίσκεται σε ή εντός'),
	(395, 'P59', 'pt', 'tem seção', 'está localizada sobre ou dentro de'),
	(396, 'P59', 'zh', '有区域', '位于'),
	(397, 'P16', 'de', 'benutzte das bestimmte Objekt', 'wurde benutzt für'),
	(398, 'P16', 'en', 'used specific object', 'was used for'),
	(399, 'P16', 'fr', 'a utilisé l''objet spécifique', 'a été utilisé pour'),
	(400, 'P16', 'ru', 'использовал особый объект', 'был использован для'),
	(401, 'P16', 'el', 'χρησιμοποίησε αντικείμενο', 'χρησιμοποιήθηκε για'),
	(402, 'P16', 'pt', 'usou objeto específico', 'foi usado por'),
	(403, 'P16', 'zh', '使用特定对象', '用于'),
	(404, 'P107', 'de', 'hat derzeitiges oder früheres Mitglied', 'ist derzeitiges oder früheres Mitglied von'),
	(405, 'P107', 'en', 'has current or former member', 'is current or former member of'),
	(406, 'P107', 'fr', 'a pour membre actuel ou ancien', 'est actuel ou ancien membre de'),
	(407, 'P107', 'ru', 'имеет действующего или бывшего члена', 'является действующим или бывшим членом'),
	(408, 'P107', 'el', 'έχει ή είχε μέλος', 'είναι ή ήταν μέλος του/της'),
	(409, 'P107', 'pt', 'tem ou teve membro', 'é ou foi membro de'),
	(410, 'P107', 'zh', '有当前或以往成员', '是当前或以往成员'),
	(411, 'P2', 'de', 'hat den Typus', 'ist Typus von'),
	(412, 'P2', 'en', 'has type', 'is type of'),
	(413, 'P2', 'fr', 'est de type', 'est le type de'),
	(414, 'P2', 'ru', 'имеет тип', 'является типом для'),
	(415, 'P2', 'el', 'έχει τύπο', 'είναι ο τύπος του/της'),
	(416, 'P2', 'pt', 'é do tipo', 'é o tipo de'),
	(417, 'P2', 'zh', '有类型', '是类型'),
	(418, 'P179', 'en', 'had sales price', 'was sales price of'),
	(419, 'P106', 'de', 'ist zusammengesetzt aus', 'bildet Teil von'),
	(420, 'P106', 'en', 'is composed of', 'forms part of'),
	(421, 'P106', 'fr', 'est composé de', 'fait partie de'),
	(422, 'P106', 'ru', 'составлен из', 'формирует часть'),
	(423, 'P106', 'el', 'αποτελείται από', 'αποτελεί μέρος του/της'),
	(424, 'P106', 'pt', 'é composto de', 'faz parte de'),
	(425, 'P106', 'zh', '组成成分是', '构成部分'),
	(426, 'P38', 'de', 'hob Zuweisung auf von', 'wurde aufgehoben durch'),
	(427, 'P38', 'en', 'deassigned', 'was deassigned by'),
	(428, 'P38', 'fr', 'a désattribué', 'a été désattribué par'),
	(429, 'P38', 'ru', 'отменил назначение', 'был отменен посредством'),
	(430, 'P38', 'el', 'ακύρωσε', 'ακυρώθηκε από'),
	(431, 'P38', 'pt', 'retirou a atribuição do', 'foi retirada a atribuição por'),
	(432, 'P38', 'zh', '取消了', '被取消'),
	(433, 'P40', 'de', 'beobachtete Dimension', 'wurde beobachtet in'),
	(434, 'P40', 'en', 'observed dimension', 'was observed in'),
	(435, 'P40', 'fr', 'a relevé comme dimension', 'a été relevée au cours de'),
	(436, 'P40', 'ru', 'определил величину', 'наблюдался в'),
	(437, 'P40', 'el', 'παρατήρησε', 'παρατηρήθηκε από'),
	(438, 'P40', 'pt', 'verificou a dimensão', 'foi verificada durante'),
	(439, 'P40', 'zh', '观测度量规格', '被观测'),
	(440, 'P188', 'en', 'requires production tool', 'is production tool for'),
	(441, 'P177', 'en', 'assigned property of type', 'is type of property assigned'),
	(442, 'P96', 'de', 'durch Mutter', 'gebar'),
	(443, 'P96', 'en', 'by mother', 'gave birth'),
	(444, 'P96', 'fr', 'de mère', 'a donné naissance à'),
	(445, 'P96', 'ru', 'посредством матери', 'дал рождение'),
	(446, 'P96', 'el', 'είχε μητέρα', 'ήταν μητέρα του/της'),
	(447, 'P96', 'pt', 'pela mãe', 'deu nascimento'),
	(448, 'P96', 'zh', '来自母亲', '生育'),
	(449, 'P143', 'de', 'verband', 'wurde verbunden durch'),
	(450, 'P143', 'en', 'joined', 'was joined by'),
	(451, 'P143', 'zh', '加入', '被加入'),
	(452, 'P165', 'en', 'incorporates', 'is incorporated in'),
	(453, 'P129', 'de', 'handelt über', 'wird behandelt in'),
	(454, 'P129', 'en', 'is about', 'is subject of'),
	(455, 'P129', 'fr', 'est au sujet de', 'est le sujet de'),
	(456, 'P129', 'ru', 'касается', 'является предметом для'),
	(530, 'P67', 'zh', '涉及', '被涉及'),
	(457, 'P129', 'el', 'έχει ως θέμα', 'είναι θέμα του/της'),
	(458, 'P129', 'pt', 'é sobre', 'é assunto de'),
	(459, 'P129', 'zh', '有关', '是主题'),
	(460, 'P127', 'de', 'hat den Oberbegriff', 'hat den Unterbegriff'),
	(461, 'P127', 'en', 'has broader term', 'has narrower term'),
	(462, 'P127', 'fr', 'a pour terme générique', 'a pour terme spécifique'),
	(463, 'P127', 'ru', 'имеет вышестоящий термин', 'имеет нижестоящий термин'),
	(464, 'P127', 'el', 'έχει ευρύτερο όρο', 'έχει στενότερο όρο'),
	(465, 'P127', 'pt', 'tem termo genérico', 'tem termo específico'),
	(466, 'P127', 'zh', '上位词', '下位词'),
	(467, 'P126', 'de', 'verwendete', 'wurde verwendet bei'),
	(468, 'P126', 'en', 'employed', 'was employed in'),
	(469, 'P126', 'fr', 'a employé', 'a été employé dans'),
	(470, 'P126', 'ru', 'использовал', 'использовался в'),
	(471, 'P126', 'el', 'χρησιμοποίησε', 'χρησιμοποιήθηκε σε'),
	(472, 'P126', 'pt', 'empregou', 'foi empregado em'),
	(473, 'P126', 'zh', '使用', '被用于'),
	(474, 'P125', 'de', 'benutzte Objekt des Typus', 'Objekt des Typus ... wurde benutzt in'),
	(475, 'P125', 'en', 'used object of type', 'was type of object used in'),
	(476, 'P125', 'fr', 'a employé un objet du type', 'était le type d’objet employé par'),
	(477, 'P125', 'ru', 'использовал объект типа', 'был типом объекта использованного в'),
	(478, 'P125', 'el', 'χρησιμοποίησε αντικείμενο τύπου', 'ήταν o τύπος αντικείμενου που χρησιμοποιήθηκε σε'),
	(479, 'P125', 'pt', 'usou objeto do tipo', 'foi tipo do objeto usado em'),
	(480, 'P125', 'zh', '使用对象类型', '是使用的对象类型'),
	(481, 'P11', 'de', 'hatte Teilnehmer', 'nahm Teil an'),
	(482, 'P11', 'en', 'had participant', 'participated in'),
	(483, 'P11', 'fr', 'a eu pour participant', 'a participé à'),
	(484, 'P11', 'ru', 'имел участника', 'участвовал в'),
	(485, 'P11', 'el', 'είχε συμμέτοχο', 'συμμετείχε σε'),
	(486, 'P11', 'pt', 'tem participante', 'participa em'),
	(487, 'P11', 'zh', '有参与者', '参与'),
	(488, 'P45', 'de', 'besteht aus', 'ist enthalten in'),
	(489, 'P45', 'en', 'consists of', 'is incorporated in'),
	(490, 'P45', 'fr', 'consiste en', 'est présent dans'),
	(491, 'P45', 'ru', 'составлен из', 'входит в состав'),
	(492, 'P45', 'el', 'αποτελείται από', 'είναι ενσωματωμένος/η/ο σε'),
	(493, 'P45', 'pt', 'consiste de', 'está presente em'),
	(494, 'P45', 'zh', '包含', '结合在'),
	(495, 'P164', 'en', 'is temporally specified by', 'temporally specifies'),
	(496, 'P51', 'de', 'hat früheren oder derzeitigen Besitzer', 'ist früherer oder derzeitiger Besitzer von'),
	(497, 'P51', 'en', 'has former or current owner', 'is former or current owner of'),
	(498, 'P51', 'fr', 'est ou a été possédée par', 'est ou a été propriétaire de'),
	(499, 'P51', 'ru', 'имеет бывшего или текущего владельца', 'является бывшим или текущим владельцем для'),
	(500, 'P51', 'el', 'έχει ή είχε ιδιοκτήτη', 'είναι ή ήταν ιδιοκτήτης του/της'),
	(501, 'P51', 'pt', 'é ou foi propriedade de', 'é ou foi proprietário de'),
	(502, 'P51', 'zh', '有以往或当前所有者', '是以往或当前所有者'),
	(503, 'P134', 'de', 'setzte sich fort in', 'wurde fortgesetzt durch'),
	(504, 'P134', 'en', 'continued', 'was continued by'),
	(505, 'P134', 'fr', 'est la suite de', 'a été continuée par'),
	(506, 'P134', 'ru', 'продолжил', 'был продолжен'),
	(507, 'P134', 'el', 'συνέχισε', 'συνεχίστηκε από'),
	(508, 'P134', 'pt', 'continuou', 'foi continuada por'),
	(509, 'P134', 'zh', '继续', '被继续'),
	(510, 'P62', 'de', 'bildet ab', 'wird abgebildet durch'),
	(511, 'P62', 'en', 'depicts', 'is depicted by'),
	(512, 'P62', 'fr', 'figure', 'est figurée sur'),
	(513, 'P62', 'ru', 'описывает', 'описан посредством'),
	(514, 'P62', 'el', 'απεικονίζει', 'απεικονίζεται σε'),
	(515, 'P62', 'pt', 'retrata', 'é retratada por'),
	(516, 'P62', 'zh', '描绘了', '被描绘'),
	(517, 'P24', 'de', 'übertrug Besitz über', 'ging über in Besitz durch'),
	(518, 'P24', 'en', 'transferred title of', 'changed ownership through'),
	(519, 'P24', 'fr', 'a fait passer le droit de propriété sur', 'a changé de mains du fait de'),
	(520, 'P24', 'ru', 'передал право собственности на', 'сменил владельца через'),
	(521, 'P24', 'el', 'μετεβίβασε τον τίτλο του/της', 'άλλαξε ιδιοκτησία μέσω'),
	(522, 'P24', 'pt', 'transferiu os direitos de propriedade sobre o', 'mudou de proprietário por meio de'),
	(523, 'P24', 'zh', '转移所有权的是', '变更所有权'),
	(524, 'P67', 'de', 'verweist auf', 'wird angeführt von'),
	(525, 'P67', 'en', 'refers to', 'is referred to by'),
	(526, 'P67', 'fr', 'fait référence à', 'est référencé par'),
	(527, 'P67', 'ru', 'ссылается на', 'имеет ссылку на себя от'),
	(528, 'P67', 'el', 'αναφέρεται σε', 'αναφέρεται από'),
	(529, 'P67', 'pt', 'referencia', 'é referenciado por'),
	(531, 'P14', 'de', 'wurde ausgeführt von', 'führte aus'),
	(532, 'P14', 'en', 'carried out by', 'performed'),
	(533, 'P14', 'fr', 'réalisée par', 'a exécuté'),
	(534, 'P14', 'ru', 'выполнялся', 'выполнял'),
	(535, 'P14', 'el', 'πραγματοποιήθηκε από', 'πραγματοποίησε'),
	(536, 'P14', 'pt', 'realizada por', 'executou'),
	(537, 'P14', 'zh', '执行者是', '执行'),
	(538, 'P31', 'de', 'veränderte', 'wurde verändert durch'),
	(539, 'P31', 'en', 'has modified', 'was modified by'),
	(540, 'P31', 'fr', 'a modifié', 'a été modifié par'),
	(541, 'P31', 'ru', 'изменил', 'был изменен посредством'),
	(542, 'P31', 'el', 'τροποποίησε', 'τροποποιήθηκε από'),
	(543, 'P31', 'pt', 'modificou', 'foi modificada por'),
	(544, 'P31', 'zh', '已更改', '被更改'),
	(545, 'P103', 'de', 'bestimmt für', 'war Bestimmung von'),
	(546, 'P103', 'en', 'was intended for', 'was intention of'),
	(547, 'P103', 'fr', 'était destiné à', 'était la raison d''être de'),
	(548, 'P103', 'ru', 'был задуман для', 'был интенцией для'),
	(549, 'P103', 'el', 'προοριζόταν για', 'ήταν προορισμός του'),
	(550, 'P103', 'pt', 'era destinado à', 'era a destinação de'),
	(551, 'P103', 'zh', '被用于', '目的是'),
	(552, 'P5', 'de', 'besteht aus', 'bildet Teil von'),
	(553, 'P5', 'en', 'consists of', 'forms part of'),
	(554, 'P5', 'fr', 'consiste en', 'fait partie de'),
	(555, 'P5', 'ru', 'состоит из', 'формирует часть'),
	(556, 'P5', 'el', 'αποτελείται από', 'αποτελεί μέρος του/της'),
	(557, 'P5', 'pt', 'consiste de', 'faz parte de'),
	(558, 'P5', 'zh', '包括', '组成部分'),
	(559, 'P27', 'de', 'bewegte weg von', 'war Ausgangsort von'),
	(560, 'P27', 'en', 'moved from', 'was origin of'),
	(561, 'P27', 'fr', 'a retiré de', 'a été l''origine de'),
	(562, 'P27', 'ru', 'перемещен из', 'был исходной точкой для'),
	(563, 'P27', 'el', 'μετακινήθηκε από', 'ήταν αφετηρία του/της'),
	(564, 'P27', 'pt', 'locomoveu de', 'era origem de'),
	(565, 'P27', 'zh', '移自', '是起点'),
	(566, 'P86', 'de', 'fällt in', 'enthält'),
	(567, 'P86', 'en', 'falls within', 'contains'),
	(568, 'P86', 'fr', 's’insère dans', 'inclut'),
	(569, 'P86', 'ru', 'содержится в', 'содержит'),
	(570, 'P86', 'el', 'περιέχεται σε', 'περιέχει'),
	(571, 'P86', 'pt', 'está contido em', 'contém'),
	(572, 'P86', 'zh', '属于', '包含'),
	(573, 'P89', 'de', 'fällt in', 'enthält'),
	(574, 'P89', 'en', 'falls within', 'contains'),
	(575, 'P89', 'fr', 's’insère dans', 'inclut'),
	(576, 'P89', 'ru', 'содержится в', 'содержит'),
	(577, 'P89', 'el', 'περιέχεται σε', 'περιέχει'),
	(578, 'P89', 'pt', 'está contido em', 'contém'),
	(579, 'P89', 'zh', '位于', '包括'),
	(580, 'P133', 'en', 'is spatiotemporally separated from', NULL),
	(581, 'P94', 'de', 'hat erschaffen', 'wurde erschaffen durch'),
	(582, 'P94', 'en', 'has created', 'was created by'),
	(583, 'P94', 'fr', 'a créé', 'a été créé par'),
	(584, 'P94', 'ru', 'создал', 'был создан посредством'),
	(585, 'P94', 'el', 'δημιούργησε', 'δημιουργήθηκε από'),
	(586, 'P94', 'pt', 'criou', 'foi criado por'),
	(587, 'P94', 'zh', '已创建了', '被创建'),
	(588, 'P151', 'en', 'was formed from', 'participated in'),
	(589, 'P15', 'de', 'wurde beeinflußt durch', 'beeinflußte'),
	(590, 'P15', 'en', 'was influenced by', 'influenced'),
	(591, 'P15', 'fr', 'a été influencée par', 'a influencé'),
	(592, 'P15', 'ru', 'находился под влиянием', 'оказал влияние на'),
	(593, 'P15', 'el', 'επηρεάστηκε από', 'επηρέασε'),
	(594, 'P15', 'pt', 'foi influenciado por', 'influenciou'),
	(595, 'P15', 'zh', '被影响', '影响'),
	(596, 'P112', 'de', 'verminderte', 'wurde vermindert durch'),
	(597, 'P112', 'en', 'diminished', 'was diminished by'),
	(598, 'P112', 'fr', 'a diminué', 'a été diminué par'),
	(599, 'P112', 'ru', 'уменьшил', 'был уменьшен посредством'),
	(600, 'P112', 'el', 'εξάλειψε', 'εξαλείφθηκε από'),
	(601, 'P112', 'pt', 'diminuiu', 'foi diminuído por'),
	(602, 'P112', 'zh', '减少了', '被减少'),
	(603, 'P32', 'de', 'benutzte das allgemeine Verfahren', 'war Verfahren von'),
	(604, 'P32', 'en', 'used general technique', 'was technique of'),
	(605, 'P32', 'fr', 'a employé comme technique générique', 'a été la technique mise en œuvre dans'),
	(606, 'P32', 'ru', 'использовал общую технику', 'был техникой для'),
	(607, 'P32', 'el', 'χρησιμοποίησε γενική τεχνική', 'ήταν τεχνική του/της'),
	(608, 'P32', 'pt', 'usou técnica geral', 'foi técnica da'),
	(609, 'P32', 'zh', '使用通用技术', '是技术'),
	(610, 'P110', 'de', 'erweiterte', 'wurde erweitert durch'),
	(611, 'P110', 'en', 'augmented', 'was augmented by'),
	(612, 'P110', 'fr', 'a augmenté', 'a été augmenté par'),
	(613, 'P110', 'ru', 'увеличил', 'был увеличен посредством'),
	(614, 'P110', 'el', 'επαύξησε', 'επαυξήθηκε από'),
	(615, 'P110', 'pt', 'aumentou', 'foi aumentada por'),
	(616, 'P110', 'zh', '增强了', '被增强'),
	(617, 'P160', 'en', 'has temporal projection', 'is temporal projection of'),
	(618, 'P122', 'de', 'grenzt an', NULL),
	(619, 'P122', 'en', 'borders with', NULL),
	(620, 'P122', 'fr', 'jouxte', NULL),
	(621, 'P122', 'ru', 'граничит с', NULL),
	(622, 'P122', 'el', 'συνορεύει με', NULL),
	(623, 'P122', 'pt', 'fronteira com', NULL),
	(624, 'P122', 'zh', '接壤于', NULL),
	(625, 'P26', 'de', 'bewegte bis zu', 'war Zielort von'),
	(626, 'P26', 'en', 'moved to', 'was destination of'),
	(627, 'P26', 'fr', 'a déplacé vers', 'a été la destination de'),
	(628, 'P26', 'ru', 'перемещен в', 'был пунктом назначения для'),
	(629, 'P26', 'el', 'μετακινήθηκε προς', 'ήταν προορισμός του/της'),
	(630, 'P26', 'pt', 'locomoveu para', 'era destinação de'),
	(631, 'P26', 'zh', '移至', '是目的地'),
	(632, 'P4', 'de', 'hat Zeitspanne', 'ist Zeitspanne von'),
	(633, 'P4', 'en', 'has time-span', 'is time-span of'),
	(634, 'P4', 'fr', 'a pour durée', 'est la durée de'),
	(635, 'P4', 'ru', 'имеет временной отрезок', 'является временным отрезком для'),
	(636, 'P4', 'el', 'βρισκόταν σε εξέλιξη', 'είναι χρονικό διάστημα του/της'),
	(637, 'P4', 'pt', 'tem período de tempo', 'é o período de tempo de'),
	(638, 'P4', 'zh', '发生时段是', '是时段'),
	(639, 'P113', 'de', 'entfernte', 'wurde entfernt durch'),
	(640, 'P113', 'en', 'removed', 'was removed by'),
	(641, 'P113', 'fr', 'a enlevé', 'a été enlevée par'),
	(642, 'P113', 'ru', 'удален', 'был удален посредством'),
	(643, 'P113', 'el', 'αφαίρεσε', 'αφαιρέθηκε από'),
	(644, 'P113', 'pt', 'removeu', 'foi removido por'),
	(645, 'P113', 'zh', '去除了', '被去除'),
	(646, 'P157', 'en', 'is at rest relative to', 'provides reference space for'),
	(647, 'P30', 'de', 'übertrug Gewahrsam über', 'wechselte Gewahrsam durch'),
	(648, 'P30', 'en', 'transferred custody of', 'custody transferred through'),
	(649, 'P30', 'fr', 'changement de détenteur concernant', 'a changé de détenteur du fait de'),
	(650, 'P30', 'ru', 'передало опеку на', 'опека передана через'),
	(651, 'P30', 'el', 'μετεβίβασε κατοχή του/της/των', 'άλλαξε κατοχή μέσω'),
	(652, 'P30', 'pt', 'transferida custódia de', 'custódia transferida por meio de'),
	(653, 'P30', 'zh', '转移监护权的是', '变更监护权'),
	(654, 'P109', 'de', 'hat derzeitigen oder früheren Kurator', 'ist derzeitiger oder früherer Kurator von'),
	(655, 'P109', 'en', 'has current or former curator', 'is current or former curator of'),
	(656, 'P109', 'fr', 'a pour conservateur actuel ou ancien', 'est ou a été le conservateur de'),
	(657, 'P109', 'ru', 'имеет действующего или бывшего хранителя', 'является действующим или бывшим хранителем'),
	(658, 'P109', 'el', 'έχει ή είχε επιμελητή', 'είναι ή ήταν επιμελητής του/της'),
	(659, 'P109', 'pt', 'tem ou teve curador', 'é ou foi curador de'),
	(660, 'P109', 'zh', '有当前或以往管理者', '是当前或以往管理者'),
	(661, 'P42', 'de', 'wies zu', 'wurde zugewiesen durch'),
	(662, 'P42', 'en', 'assigned', 'was assigned by'),
	(663, 'P42', 'fr', 'a attribué', 'a été attribué par'),
	(664, 'P42', 'ru', 'назначил', 'был присвоен посредством'),
	(665, 'P42', 'el', 'απέδωσε ως ιδιότητα', 'αποδόθηκε από'),
	(666, 'P42', 'pt', 'atribuiu', 'foi atribuído por'),
	(667, 'P42', 'zh', '分配类型', '被分配类型'),
	(668, 'P44', 'de', 'hat Zustand', 'ist Zustand von'),
	(669, 'P44', 'en', 'has condition', 'is condition of'),
	(670, 'P44', 'fr', 'a pour état matériel', 'état matériel de'),
	(671, 'P44', 'ru', 'имеет условие', 'является условием для'),
	(672, 'P44', 'el', 'έχει κατάσταση', 'είναι κατάσταση του'),
	(673, 'P44', 'pt', 'tem estado material', 'estado material de'),
	(674, 'P44', 'zh', '有状况', '是状况'),
	(675, 'P65', 'de', 'zeigt Bildliches', 'wird gezeigt durch'),
	(676, 'P65', 'en', 'shows visual item', 'is shown by'),
	(677, 'P65', 'fr', 'présente l''item visuel', 'est présenté par'),
	(678, 'P65', 'ru', 'показывает визуальный предмет', 'показан посредством'),
	(679, 'P65', 'el', 'εμφανίζει οπτικό στοιχείο', 'εμφανίζεται σε'),
	(680, 'P65', 'pt', 'apresenta item visual', 'é apresentado por'),
	(681, 'P65', 'zh', '展示可视项', '被展示'),
	(682, 'P176', 'en', 'starts before the start of', 'starts after the start of'),
	(683, 'P34', 'de', 'betraf', 'wurde beurteilt durch'),
	(684, 'P34', 'en', 'concerned', 'was assessed by'),
	(685, 'P34', 'fr', 'a concerné', 'expertisé par le biais de'),
	(686, 'P34', 'ru', 'имел дело с', 'был оценен посредством'),
	(687, 'P34', 'el', 'αφορούσε σε', 'εκτιμήθηκε από'),
	(688, 'P34', 'pt', 'interessada', 'foi avaliada por'),
	(689, 'P34', 'zh', '已评估', '被评估'),
	(690, 'P187', 'en', 'has production plan', 'is production plan for'),
	(691, 'P130', 'de', 'zeigt Merkmale von', 'Merkmale auch auf'),
	(692, 'P130', 'en', 'shows features of', 'features are also found on'),
	(693, 'P130', 'fr', 'présente des caractéristiques de', 'a des caractéristiques se trouvant aussi sur'),
	(694, 'P130', 'ru', 'демонстрирует признаки', 'признаки также найдены на'),
	(695, 'P130', 'el', 'παρουσιάζει χαρακτηριστικά του/της', 'χαρακτηριστικά του βρίσκονται επίσης σε'),
	(696, 'P130', 'pt', 'apresenta características de', 'características são também encontradas em'),
	(697, 'P130', 'zh', '显示特征', '发现特征'),
	(698, 'P70', 'de', 'belegt', 'wird belegt in'),
	(699, 'P70', 'en', 'documents', 'is documented in'),
	(700, 'P70', 'fr', 'mentionne', 'est mentionnée dans'),
	(701, 'P70', 'ru', 'документирует', 'документирован в'),
	(702, 'P70', 'el', 'τεκμηριώνει', 'τεκμηριώνεται σε'),
	(703, 'P70', 'pt', 'documenta', 'é documentado em'),
	(704, 'P70', 'zh', '记录了', '记录在'),
	(705, 'P99', 'de', 'löste auf', 'wurde aufgelöst durch'),
	(706, 'P99', 'en', 'dissolved', 'was dissolved by'),
	(707, 'P99', 'fr', 'a dissous', 'a été dissous par'),
	(708, 'P99', 'ru', 'распустил', 'был распущен посредством'),
	(709, 'P99', 'el', 'διέλυσε', 'διαλύθηκε από'),
	(710, 'P99', 'pt', 'dissolveu', 'foi dissolvido por'),
	(711, 'P99', 'zh', '解散了', '被解散'),
	(712, 'P48', 'de', 'hat bevorzugtes Kennzeichen', 'ist bevorzugtes Kennzeichen für'),
	(713, 'P48', 'en', 'has preferred identifier', 'is preferred identifier of'),
	(714, 'P48', 'fr', 'a pour identificateur retenu', 'est l’identificateur retenu de'),
	(715, 'P48', 'ru', 'имеет предпочтительный идентификатор', 'является предпочтительным идентификатором для'),
	(716, 'P48', 'el', 'έχει προτιμώμενο αναγνωριστικό', 'είναι προτιμώμενο αναγνωριστικό'),
	(717, 'P48', 'pt', 'tem identificador preferido', 'é o identificador preferido de'),
	(718, 'P48', 'zh', '有优选标识符', '是优选标识符'),
	(719, 'P166', 'en', 'was a presence of', 'had presence'),
	(720, 'P197', 'en', 'covered parts of', 'was partially covered by'),
	(721, 'P97', 'de', 'gab Vaterschaft', 'war Vater für'),
	(722, 'P97', 'en', 'from father', 'was father for'),
	(723, 'P97', 'fr', 'de père', 'a été père dans'),
	(724, 'P97', 'ru', 'от отца', 'был отцом для'),
	(725, 'P97', 'el', 'είχε πατέρα', 'ήταν πατέρας του/της'),
	(726, 'P97', 'pt', 'pelo pai', 'foi pai para'),
	(727, 'P97', 'zh', '来自父亲', '是父亲'),
	(728, 'P41', 'de', 'klassifizierte', 'wurde klassifiziert durch'),
	(729, 'P41', 'en', 'classified', 'was classified by'),
	(730, 'P41', 'fr', 'a classifié', 'a été classifiée par le biais de'),
	(731, 'P41', 'ru', 'классифицировал', 'был классифицирован посредством'),
	(732, 'P41', 'el', 'χαρακτήρισε', 'χαρακτηρίσθηκε από'),
	(733, 'P41', 'pt', 'classificou', 'foi classificada por'),
	(734, 'P41', 'zh', '分类', '被分类'),
	(735, 'P146', 'de', 'entließ von', 'verlor Mitglied durch'),
	(736, 'P146', 'en', 'separated from', 'lost member by'),
	(737, 'P146', 'zh', '脱离', '失去成员'),
	(738, 'P186', 'en', 'produced thing of product type', 'is produced by'),
	(739, 'P174', 'en', 'starts before the end of', 'ends after the start of'),
	(740, 'P152', 'en', 'has parent', 'is parent of'),
	(741, 'P196', 'en', 'defines', 'is defined by'),
	(742, 'P28', 'de', 'übergab Gewahrsam an', 'wurde Gewahrsam übergeben durch'),
	(743, 'P28', 'en', 'custody surrendered by', 'surrendered custody through'),
	(744, 'P28', 'fr', 'changement de détenteur au détriment de', 'a cessé d’être détenteur à cause de'),
	(745, 'P28', 'ru', 'опека отдана', 'опека отдана через'),
	(746, 'P28', 'el', 'μετεβίβασε κατοχή από', 'παρέδωσε κατοχή μέσω'),
	(747, 'P28', 'pt', 'custódia concedida por', 'final da custódia por meio de'),
	(748, 'P28', 'zh', '监护权转自', '出让监护权'),
	(749, 'P156', 'en', 'occupies', 'is occupied by'),
	(750, 'P180', 'en', 'has currency', 'was currency of'),
	(751, 'P50', 'de', 'hat derzeitigen Betreuer', 'ist derzeitiger Betreuer von'),
	(752, 'P50', 'en', 'has current keeper', 'is current keeper of'),
	(753, 'P50', 'fr', 'est actuellement détenu par', 'est actuel détenteur de'),
	(754, 'P50', 'ru', 'имеет текущего смотрителя', 'является текущим смотрителем для'),
	(755, 'P50', 'el', 'είναι στην κατοχή του', 'κατέχει'),
	(756, 'P50', 'pt', 'é guardada por', 'é guardador de'),
	(757, 'P50', 'zh', '有当前保管者', '是当前保管者'),
	(758, 'P137', 'de', 'erläutert', 'erläutert durch Beispiel'),
	(759, 'P137', 'en', 'exemplifies', 'is exemplified by'),
	(760, 'P137', 'fr', 'exemplifie', 'est exemplifié par'),
	(761, 'P137', 'ru', 'поясняет', 'поясняется посредством'),
	(762, 'P137', 'el', 'δειγματίζει', 'δειγματίζεται από'),
	(763, 'P137', 'pt', 'é exemplificado por', 'exemplifica'),
	(764, 'P137', 'zh', '例示', '被例示'),
	(765, 'P167', 'en', 'was within', 'includes'),
	(766, 'P19', 'de', 'war beabsichtigteter Gebrauch von', 'wurde hergestellt für'),
	(767, 'P19', 'en', 'was intended use of', 'was made for'),
	(768, 'P19', 'fr', 'était l''utilisation prévue de', 'a été fabriquée pour'),
	(769, 'P19', 'ru', 'был предполагаемым использованием для', 'был создан для'),
	(770, 'P19', 'el', 'ήταν προορισμένη χρήση του', 'έγινε για'),
	(771, 'P19', 'pt', 'era prevista a utilização de', 'foi feito para'),
	(772, 'P19', 'zh', '特定用途是', '用于'),
	(773, 'P175', 'en', 'starts before or with the start of', 'starts after or with the start of'),
	(774, 'P182', 'en', 'ends before or with the start of', 'starts after or with the end of'),
	(775, 'P121', 'de', 'überlappt mit', NULL),
	(776, 'P121', 'en', 'overlaps with', NULL),
	(777, 'P121', 'fr', 'chevauche', NULL),
	(778, 'P121', 'ru', 'пересекается с', NULL),
	(779, 'P121', 'el', 'επικαλύπτεται με', NULL),
	(780, 'P121', 'pt', 'sobrepõe com', NULL),
	(781, 'P121', 'zh', '重叠于', NULL),
	(782, 'P17', 'de', 'wurde angeregt durch', 'regte an'),
	(783, 'P17', 'en', 'was motivated by', 'motivated'),
	(784, 'P17', 'fr', 'a été motivée par', 'a motivé'),
	(785, 'P17', 'ru', 'был обусловлен посредством', 'обусловил'),
	(786, 'P17', 'el', 'είχε ως αφορμή', 'ήταν αφορμή'),
	(787, 'P17', 'pt', 'foi motivado por', 'motivou'),
	(788, 'P17', 'zh', '被促动', '促动'),
	(789, 'P173', 'en', 'starts before or with the end of', 'ends after or with the start of'),
	(790, 'P33', 'de', 'benutzte das bestimmte Verfahren', 'wurde benutzt von'),
	(791, 'P33', 'en', 'used specific technique', 'was used by'),
	(792, 'P33', 'fr', 'a employé comme technique spécifique', 'a été employée par'),
	(793, 'P33', 'ru', 'использовал особую технику', 'был использован посредством'),
	(794, 'P33', 'el', 'χρησιμοποίησε συγκεκριμένη τεχνική', 'χρησιμοποιήθηκε για'),
	(795, 'P33', 'pt', 'usou técnica específica', 'foi usada por'),
	(796, 'P33', 'zh', '使用特定技术', '被使用'),
	(797, 'P150', 'en', 'defines typical parts of', 'defines typical wholes for'),
	(798, 'P195', 'en', 'was a presence of', 'had presence'),
	(799, 'P198', 'en', 'holds or supports', 'is held or supported by'),
	(800, 'P161', 'en', 'has spatial projection', 'is spatial projection of'),
	(801, 'P144', 'de', 'verband mit', 'erwarb Mitglied durch'),
	(802, 'P144', 'en', 'joined with', 'gained member by'),
	(803, 'P144', 'zh', '加入', '获得成员'),
	(804, 'OA7', 'en', 'has relationship to', NULL),
	(805, 'OA7', 'de', 'hat Beziehung zu', NULL),
	(806, 'OA8', 'en', 'begins in', NULL),
	(807, 'OA8', 'de', 'beginnt in', NULL),
	(808, 'OA9', 'en', 'ends in', NULL),
	(809, 'OA9', 'de', 'endet in', NULL);


ALTER TABLE ONLY model.entity ADD CONSTRAINT entity_class_code_fkey FOREIGN KEY (cidoc_class_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.link ADD CONSTRAINT link_property_code_fkey FOREIGN KEY (property_code) REFERENCES model.property(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.cidoc_class_inheritance ADD CONSTRAINT class_inheritance_super_code_fkey FOREIGN KEY (super_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.cidoc_class_inheritance ADD CONSTRAINT class_inheritance_sub_code_fkey FOREIGN KEY (sub_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.cidoc_class_i18n ADD CONSTRAINT class_i18n_class_code_fkey FOREIGN KEY (class_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.property ADD CONSTRAINT property_domain_class_code_fkey FOREIGN KEY (domain_class_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.property ADD CONSTRAINT property_range_class_code_fkey FOREIGN KEY (range_class_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.property_inheritance ADD CONSTRAINT property_inheritance_super_code_fkey FOREIGN KEY (super_code) REFERENCES model.property(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.property_inheritance ADD CONSTRAINT property_inheritance_sub_code_fkey FOREIGN KEY (sub_code) REFERENCES model.property(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.property_i18n ADD CONSTRAINT property_i18n_property_code_fkey FOREIGN KEY (property_code) REFERENCES model.property(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.entity ADD CONSTRAINT entity_openatlas_class_name_fkey FOREIGN KEY (openatlas_class_name) REFERENCES model.openatlas_class(name) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.openatlas_class ADD CONSTRAINT openatlas_class_cidoc_class_code_fkey FOREIGN KEY (cidoc_class_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY web.reference_system_openatlas_class ADD CONSTRAINT reference_system_openatlas_class_openatlas_class_name_fkey FOREIGN KEY (openatlas_class_name) REFERENCES model.openatlas_class(name) ON UPDATE CASCADE ON DELETE CASCADE;

COMMIT;
