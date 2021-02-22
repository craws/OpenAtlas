SET search_path = model;

------------------
-- Bibliography --
------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Bibliography', 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Inbook'), ('E55', 'Article'), ('E55', 'Book');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Bibliography'), (SELECT id FROM entity WHERE name='Inbook')),
('P127', (SELECT id FROM entity WHERE name='Bibliography'), (SELECT id FROM entity WHERE name='Article')),
('P127', (SELECT id FROM entity WHERE name='Bibliography'), (SELECT id FROM entity WHERE name='Book'));

-------------
-- Edition --
-------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Edition', 'Categories for the classification of written sources'' editions like charter editions, chronicle edition etc.');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Charter Edition'), ('E55', 'Letter Edition'), ('E55', 'Chronicle Edition');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Edition'), (SELECT id FROM entity WHERE name='Charter Edition')),
('P127', (SELECT id FROM entity WHERE name='Edition'), (SELECT id FROM entity WHERE name='Letter Edition')),
('P127', (SELECT id FROM entity WHERE name='Edition'), (SELECT id FROM entity WHERE name='Chronicle Edition'));

------------------------
-- External reference --
------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'External reference', 'Categories for the classification of external references like a link to Wikipedia');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Link');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='External reference'), (SELECT id FROM entity WHERE name='Link'));

------------------------
-- External reference match--
------------------------
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'External reference match', 'SKOS based definition of the confidence degree that concepts can be used interchangeable.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'exact match', 'High degree of confidence that the concepts can be used interchangeably.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'close match', 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM model.entity WHERE name='External reference match'), (SELECT id FROM model.entity WHERE name='exact match')),
('P127', (SELECT id FROM model.entity WHERE name='External reference match'), (SELECT id FROM model.entity WHERE name='close match'));

--------------------
-- Actor function --
--------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Actor function', 'Definitions of an actor''s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Bishop'),
('E55', 'Abbot'),
('E55', 'Pope'),
('E55', 'Emperor'),
('E55', 'Count'),
('E55', 'King');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Actor function'), (SELECT id FROM entity WHERE name='Bishop')),
('P127', (SELECT id FROM entity WHERE name='Actor function'), (SELECT id FROM entity WHERE name='Abbot')),
('P127', (SELECT id FROM entity WHERE name='Actor function'), (SELECT id FROM entity WHERE name='Pope')),
('P127', (SELECT id FROM entity WHERE name='Actor function'), (SELECT id FROM entity WHERE name='Emperor')),
('P127', (SELECT id FROM entity WHERE name='Actor function'), (SELECT id FROM entity WHERE name='Count')),
('P127', (SELECT id FROM entity WHERE name='Actor function'), (SELECT id FROM entity WHERE name='King'));

-----------------
-- Involvement --
-----------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Involvement', 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Creator'),
('E55', 'Sponsor'),
('E55', 'Victim'),
('E55', 'Offender');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Involvement'), (SELECT id FROM entity WHERE name='Creator')),
('P127', (SELECT id FROM entity WHERE name='Involvement'), (SELECT id FROM entity WHERE name='Sponsor')),
('P127', (SELECT id FROM entity WHERE name='Involvement'), (SELECT id FROM entity WHERE name='Victim')),
('P127', (SELECT id FROM entity WHERE name='Involvement'), (SELECT id FROM entity WHERE name='Offender'));

---------
-- Sex --
---------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Sex', 'Categories for sex like female, male.');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Female'), ('E55', 'Male');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Sex'), (SELECT id FROM entity WHERE name='Female')),
('P127', (SELECT id FROM entity WHERE name='Sex'), (SELECT id FROM entity WHERE name='Male'));

-----------
-- Event --
-----------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Event', 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Change of Property'),
('E55', 'Donation'),
('E55', 'Sale'),
('E55', 'Exchange'),
('E55', 'Conflict'),
('E55', 'Battle'),
('E55', 'Raid');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Event'), (SELECT id FROM entity WHERE name='Change of Property')),
('P127', (SELECT id FROM entity WHERE name='Event'), (SELECT id FROM entity WHERE name='Conflict')),
('P127', (SELECT id FROM entity WHERE name='Change of Property'), (SELECT id FROM entity WHERE name='Donation')),
('P127', (SELECT id FROM entity WHERE name='Change of Property'), (SELECT id FROM entity WHERE name='Sale')),
('P127', (SELECT id FROM entity WHERE name='Change of Property'), (SELECT id FROM entity WHERE name='Exchange')),
('P127', (SELECT id FROM entity WHERE name='Conflict'), (SELECT id FROM entity WHERE name='Battle')),
('P127', (SELECT id FROM entity WHERE name='Conflict'), (SELECT id FROM entity WHERE name='Raid'));

------------
-- Source --
------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Source', 'Types for historical sources like charter, chronicle, letter etc.');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Charter'),
('E55', 'Testament'),
('E55', 'Letter'),
('E55', 'Contract');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Source'), (SELECT id FROM entity WHERE name='Charter')),
('P127', (SELECT id FROM entity WHERE name='Source'), (SELECT id FROM entity WHERE name='Testament')),
('P127', (SELECT id FROM entity WHERE name='Source'), (SELECT id FROM entity WHERE name='Letter')),
('P127', (SELECT id FROM entity WHERE name='Source'), (SELECT id FROM entity WHERE name='Contract'));

-------------
-- License --
-------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'License', 'Types for the licensing of a file');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Proprietary license'),
('E55', 'Open license'),
('E55', 'Public domain'),
('E55', 'CC BY 4.0'),
('E55', 'CC BY-SA 4.0');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='License'), (SELECT id FROM entity WHERE name='Proprietary license')),
('P127', (SELECT id FROM entity WHERE name='License'), (SELECT id FROM entity WHERE name='Open license')),
('P127', (SELECT id FROM entity WHERE name='Open license'), (SELECT id FROM entity WHERE name='Public domain')),
('P127', (SELECT id FROM entity WHERE name='Open license'), (SELECT id FROM entity WHERE name='CC BY 4.0')),
('P127', (SELECT id FROM entity WHERE name='Open license'), (SELECT id FROM entity WHERE name='CC BY-SA 4.0'));

--------------------------
-- Actor actor relation --
--------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Actor actor relation', 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Kindredship'),
('E55', 'Parent of (Child of)'),
('E55', 'Social'),
('E55', 'Friend of'),
('E55', 'Enemy of'),
('E55', 'Mentor of (Student of)'),
('E55', 'Political'),
('E55', 'Ally of'),
('E55', 'Leader of (Retinue of)'),
('E55', 'Economical'),
('E55', 'Provider of (Customer of)');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Actor actor relation'), (SELECT id FROM entity WHERE name='Kindredship')),
('P127', (SELECT id FROM entity WHERE name='Actor actor relation'), (SELECT id FROM entity WHERE name='Social')),
('P127', (SELECT id FROM entity WHERE name='Actor actor relation'), (SELECT id FROM entity WHERE name='Political')),
('P127', (SELECT id FROM entity WHERE name='Actor actor relation'), (SELECT id FROM entity WHERE name='Economical')),
('P127', (SELECT id FROM entity WHERE name='Kindredship'), (SELECT id FROM entity WHERE name='Parent of (Child of)')),
('P127', (SELECT id FROM entity WHERE name='Social'), (SELECT id FROM entity WHERE name='Friend of')),
('P127', (SELECT id FROM entity WHERE name='Social'), (SELECT id FROM entity WHERE name='Enemy of')),
('P127', (SELECT id FROM entity WHERE name='Social'), (SELECT id FROM entity WHERE name='Mentor of (Student of)')),
('P127', (SELECT id FROM entity WHERE name='Political'), (SELECT id FROM entity WHERE name='Ally of')),
('P127', (SELECT id FROM entity WHERE name='Political'), (SELECT id FROM entity WHERE name='Leader of (Retinue of)')),
('P127', (SELECT id FROM entity WHERE name='Economical'), (SELECT id FROM entity WHERE name='Provider of (Customer of)'));

----------
-- Place --
----------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Place', 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Settlement'),
('E55', 'Military Facility'),
('E55', 'Ritual Site'),
('E55', 'Burial Site'),
('E55', 'Infrastructure'),
('E55', 'Economic Site'),
('E55', 'Boundary Mark'),
('E55', 'Topographical Entity');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Settlement')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Military Facility')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Ritual Site')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Burial Site')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Infrastructure')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Economic Site')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Boundary Mark')),
('P127', (SELECT id FROM entity WHERE name='Place'), (SELECT id FROM entity WHERE name='Topographical Entity'));

-------------
-- Feature --
-------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Feature', 'Classification of the archaeological feature e.g. grave, pit, ...');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Grave'), ('E55', 'Pit');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Feature'), (SELECT id FROM entity WHERE name='Grave')),
('P127', (SELECT id FROM entity WHERE name='Feature'), (SELECT id FROM entity WHERE name='Pit'));

------------------------
-- Stratigraphic unit --
------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Stratigraphic unit', 'Classification of the archaeological SU e.g. burial, deposit, ...');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Burial'), ('E55', 'Deposit');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Stratigraphic unit'), (SELECT id FROM entity WHERE name='Burial')),
('P127', (SELECT id FROM entity WHERE name='Stratigraphic unit'), (SELECT id FROM entity WHERE name='Deposit'));

-------------------
-- Human remains --
-------------------
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Human remains', 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Upper Body', '');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Lower Body', '');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES ('P127', (SELECT id FROM model.entity WHERE name='Human remains' AND class_code = 'E55'), (SELECT id FROM model.entity WHERE name='Upper Body'));
INSERT INTO model.link (property_code, range_id, domain_id) VALUES ('P127', (SELECT id FROM model.entity WHERE name='Human remains' AND class_code = 'E55'), (SELECT id FROM model.entity WHERE name='Lower Body'));
INSERT INTO web.hierarchy (id, name, multiple, standard, directional, value_type) VALUES ((SELECT id FROM model.entity WHERE name='Human remains' AND class_code = 'E55'), 'Human remains', False, True, False, False);
INSERT INTO web.form (name, extendable) VALUES ('Human remains', True);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES ((SELECT id FROM web.hierarchy WHERE name='Human remains'),(SELECT id FROM web.form WHERE name='Human remains'));

-------------------------
-- Administrative unit --
-------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E53', 'Administrative unit', 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.');
INSERT INTO entity (class_code, name) VALUES
('E53', 'Austria'),
('E53', 'Wien'),
('E53', 'Niederösterreich'),
('E53', 'Germany'),
('E53', 'Italy'),
('E53', 'Czech Republic'),
('E53', 'Slovakia'),
('E53', 'Slovenia');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P89', (SELECT id FROM entity WHERE name='Administrative unit'), (SELECT id FROM entity WHERE name='Austria')),
('P89', (SELECT id FROM entity WHERE name='Administrative unit'), (SELECT id FROM entity WHERE name='Italy')),
('P89', (SELECT id FROM entity WHERE name='Administrative unit'), (SELECT id FROM entity WHERE name='Germany')),
('P89', (SELECT id FROM entity WHERE name='Administrative unit'), (SELECT id FROM entity WHERE name='Czech Republic')),
('P89', (SELECT id FROM entity WHERE name='Administrative unit'), (SELECT id FROM entity WHERE name='Slovakia')),
('P89', (SELECT id FROM entity WHERE name='Administrative unit'), (SELECT id FROM entity WHERE name='Slovenia')),
('P89', (SELECT id FROM entity WHERE name='Austria'), (SELECT id FROM entity WHERE name='Wien')),
('P89', (SELECT id FROM entity WHERE name='Austria'), (SELECT id FROM entity WHERE name='Niederösterreich'));

----------------------
-- Historical place --
----------------------
INSERT INTO entity (class_code, name, description) VALUES ('E53', 'Historical place', 'Hierarchy of historical places respectively historical administrative units like: Duchy of Bavaria, Lombard Kingdom etc.');
INSERT INTO entity (class_code, name) VALUES
('E53', 'Carantania'),
('E53', 'Marcha Orientalis'),
('E53', 'Comitatus Iauntal'),
('E53', 'Kingdom of Serbia');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P89', (SELECT id FROM entity WHERE name='Historical place'), (SELECT id FROM entity WHERE name='Carantania')),
('P89', (SELECT id FROM entity WHERE name='Historical place'), (SELECT id FROM entity WHERE name='Marcha Orientalis')),
('P89', (SELECT id FROM entity WHERE name='Historical place'), (SELECT id FROM entity WHERE name='Comitatus Iauntal')),
('P89', (SELECT id FROM entity WHERE name='Historical place'), (SELECT id FROM entity WHERE name='Kingdom of Serbia'));

------------------------
-- Source translation --
------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Source translation', '');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Original Text'), ('E55', 'Translation'), ('E55', 'Transliteration');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Source translation'), (SELECT id FROM entity WHERE name='Original Text')),
('P127', (SELECT id FROM entity WHERE name='Source translation'), (SELECT id FROM entity WHERE name='Translation')),
('P127', (SELECT id FROM entity WHERE name='Source translation'), (SELECT id FROM entity WHERE name='Transliteration'));

-----------------
-- Value types --
-----------------
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Dimensions', 'Physical dimensions like weight and height.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Height', 'centimeter'), ('E55', 'Weight', 'gram');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Height')),
('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Weight'));

--------------
-- Artifact --
--------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Artifact', '');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Coin'), ('E55', 'Statue');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Artifact'), (SELECT id FROM entity WHERE name='Coin')),
('P127', (SELECT id FROM entity WHERE name='Artifact'), (SELECT id FROM entity WHERE name='Statue'));

---------------
-- Web forms --
---------------
INSERT INTO web.form (name, extendable) VALUES
('actor_actor_relation', False),
('artifact', True),
('bibliography', True),
('edition', True),
('event', True),
('external_reference', True),
('feature', True),
('file', True),
('find', True),
('group', True),
('human_remains', True)
('involvement', False),
('member', False),
('source', True),
('person', True),
('place', True),
('stratigraphic_unit', True),
('source_translation', False),
('type', True);

INSERT INTO web.hierarchy (id, name, multiple, standard, directional, value_type, locked) VALUES
((SELECT id FROM entity WHERE name='Actor function'), 'Actor function', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Actor actor relation'), 'Actor actor relation', False, True, True, False, False),
((SELECT id FROM entity WHERE name='Administrative unit'), 'Administrative unit', True, True, False, False, False),
((SELECT id FROM entity WHERE name='Artifact'), 'Artifact', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Bibliography'), 'Bibliography', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Edition'), 'Edition', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Event'), 'Event', False, True, False, False, False),
((SELECT id FROM entity WHERE name='External reference'), 'External reference', False, True, False, False, False),
((SELECT id FROM entity WHERE name='External reference match'), 'External reference match', False, True, False, False, True),
((SELECT id FROM entity WHERE name='Feature'), 'Feature', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Historical place'), 'Historical place', True, True, False, False, False),
((SELECT id FROM entity WHERE name='Involvement'), 'Involvement', False, True, False, False, False),
((SELECT id FROM entity WHERE name='License'), 'License', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Source'), 'Source', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Place'), 'Place', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Stratigraphic unit'), 'Stratigraphic unit', False, True, False, False, False),
((SELECT id FROM entity WHERE name='Source translation'), 'Source translation', False, False, False, False, False),
-- custom examples
((SELECT id FROM entity WHERE name='Dimensions'), 'Dimensions', True, False, False, True, False),
((SELECT id FROM entity WHERE name='Sex'), 'Sex', False, False, False, False, False);

INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
((SELECT id FROM web.hierarchy WHERE name='Actor function'),(SELECT id FROM web.form WHERE name='member')),
((SELECT id FROM web.hierarchy WHERE name='Actor actor relation'),(SELECT id FROM web.form WHERE name='actor_actor_relation')),
((SELECT id FROM web.hierarchy WHERE name='Administrative unit'),(SELECT id FROM web.form WHERE name='place')),
((SELECT id FROM web.hierarchy WHERE name='Artifact'),(SELECT id FROM web.form WHERE name='artifact')),
((SELECT id FROM web.hierarchy WHERE name='Bibliography'),(SELECT id FROM web.form WHERE name='bibliography')),
((SELECT id FROM web.hierarchy WHERE name='Edition'),(SELECT id FROM web.form WHERE name='edition')),
((SELECT id FROM web.hierarchy WHERE name='Event'),(SELECT id FROM web.form WHERE name='event')),
((SELECT id FROM web.hierarchy WHERE name='External reference'),(SELECT id FROM web.form WHERE name='external_reference'));
((SELECT id FROM web.hierarchy WHERE name='Feature'),(SELECT id FROM web.form WHERE name='feature')),
((SELECT id FROM web.hierarchy WHERE name='Historical place'),(SELECT id FROM web.form WHERE name='place')),
((SELECT id FROM web.hierarchy WHERE name='Involvement'),(SELECT id FROM web.form WHERE name='involvement')),
((SELECT id FROM web.hierarchy WHERE name='License'),(SELECT id FROM web.form WHERE name='file')),
((SELECT id FROM web.hierarchy WHERE name='Source'),(SELECT id FROM web.form WHERE name='source')),
((SELECT id FROM web.hierarchy WHERE name='Place'),(SELECT id FROM web.form WHERE name='place')),
((SELECT id FROM web.hierarchy WHERE name='Stratigraphic unit'),(SELECT id FROM web.form WHERE name='stratigraphic_unit')),
((SELECT id FROM web.hierarchy WHERE name='Source translation'),(SELECT id FROM web.form WHERE name='source_translation')),
-- custom examples
((SELECT id FROM web.hierarchy WHERE name='Dimensions'),(SELECT id FROM web.form WHERE name='artifact')),
((SELECT id FROM web.hierarchy WHERE name='Sex'),(SELECT id FROM web.form WHERE name='person'));

INSERT INTO web.reference_system_form (reference_system_id, form_id) VALUES
((SELECT entity_id FROM web.reference_system WHERE name='GeoNames'), (SELECT id FROM web.form WHERE name='Place')),
((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), (SELECT id FROM web.form WHERE name='Place')),
((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), (SELECT id FROM web.form WHERE name='Person')),
((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), (SELECT id FROM web.form WHERE name='Group')),
((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), (SELECT id FROM web.form WHERE name='Event'));
