SET search_path = model;

-------------------------
-- Information Carrier --
-------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Information Carrier', 'Categories for information carriers. A medieval charter for example may be an information carrier that has a specific content. A later copy of that charter that may be stored in another place/archive will also contain the same content. Therefore we provide different types of information carriers like: Original document, Copy of document etc.');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Original Document'), ('E55', 'Copy of Document');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Information Carrier'), (SELECT id FROM entity WHERE name='Original Document')),
('P127', (SELECT id FROM entity WHERE name='Information Carrier'), (SELECT id FROM entity WHERE name='Copy of Document'));

---------------
-- Bibliography
---------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Bibliography', 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Inbook'), ('E55', 'Article'), ('E55', 'Book');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Bibliography'), (SELECT id FROM entity WHERE name='Inbook')),
('P127', (SELECT id FROM entity WHERE name='Bibliography'), (SELECT id FROM entity WHERE name='Article')),
('P127', (SELECT id FROM entity WHERE name='Bibliography'), (SELECT id FROM entity WHERE name='Book'));

----------
-- Edition
----------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Edition', 'Categories for the classification of written sources'' editions like charter editions, chronicle edition etc.');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Charter Edition'), ('E55', 'Letter Edition'), ('E55', 'Chronicle Edition');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Edition'), (SELECT id FROM entity WHERE name='Charter Edition')),
('P127', (SELECT id FROM entity WHERE name='Edition'), (SELECT id FROM entity WHERE name='Letter Edition')),
('P127', (SELECT id FROM entity WHERE name='Edition'), (SELECT id FROM entity WHERE name='Chronicle Edition'));

-----------------
-- Actor Function
-----------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Actor Function', 'Definitions of an actor''s function within a group or legal body. An actor can for example be member of a legal body and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the legal body "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the legal body "Roman Empire" from 800 to 814 in the function "Emperor".');
INSERT INTO entity (class_code, name) VALUES
('E55', 'Bishop'),
('E55', 'Abbot'),
('E55', 'Pope'),
('E55', 'Emperor'),
('E55', 'Count'),
('E55', 'King');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Actor Function'), (SELECT id FROM entity WHERE name='Bishop')),
('P127', (SELECT id FROM entity WHERE name='Actor Function'), (SELECT id FROM entity WHERE name='Abbot')),
('P127', (SELECT id FROM entity WHERE name='Actor Function'), (SELECT id FROM entity WHERE name='Pope')),
('P127', (SELECT id FROM entity WHERE name='Actor Function'), (SELECT id FROM entity WHERE name='Emperor')),
('P127', (SELECT id FROM entity WHERE name='Actor Function'), (SELECT id FROM entity WHERE name='Count')),
('P127', (SELECT id FROM entity WHERE name='Actor Function'), (SELECT id FROM entity WHERE name='King'));

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
-- Actor Actor Relation --
--------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Actor Actor Relation', 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).');
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
('P127', (SELECT id FROM entity WHERE name='Actor Actor Relation'), (SELECT id FROM entity WHERE name='Kindredship')),
('P127', (SELECT id FROM entity WHERE name='Actor Actor Relation'), (SELECT id FROM entity WHERE name='Social')),
('P127', (SELECT id FROM entity WHERE name='Actor Actor Relation'), (SELECT id FROM entity WHERE name='Political')),
('P127', (SELECT id FROM entity WHERE name='Actor Actor Relation'), (SELECT id FROM entity WHERE name='Economical')),
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

-------------------------
-- Administrative Unit --
-------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E53', 'Administrative Unit', 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.');
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
('P89', (SELECT id FROM entity WHERE name='Administrative Unit'), (SELECT id FROM entity WHERE name='Austria')),
('P89', (SELECT id FROM entity WHERE name='Administrative Unit'), (SELECT id FROM entity WHERE name='Italy')),
('P89', (SELECT id FROM entity WHERE name='Administrative Unit'), (SELECT id FROM entity WHERE name='Germany')),
('P89', (SELECT id FROM entity WHERE name='Administrative Unit'), (SELECT id FROM entity WHERE name='Czech Republic')),
('P89', (SELECT id FROM entity WHERE name='Administrative Unit'), (SELECT id FROM entity WHERE name='Slovakia')),
('P89', (SELECT id FROM entity WHERE name='Administrative Unit'), (SELECT id FROM entity WHERE name='Slovenia')),
('P89', (SELECT id FROM entity WHERE name='Austria'), (SELECT id FROM entity WHERE name='Wien')),
('P89', (SELECT id FROM entity WHERE name='Austria'), (SELECT id FROM entity WHERE name='Niederösterreich'));

----------------------
-- Historical Place --
----------------------
INSERT INTO entity (class_code, name, description) VALUES ('E53', 'Historical Place', 'Hierarchy of historical places respectively historical administrative units like: Duchy of Bavaria, Lombard Kingdom etc.');
INSERT INTO entity (class_code, name) VALUES
('E53', 'Carantania'),
('E53', 'Marcha Orientalis'),
('E53', 'Comitatus Iauntal'),
('E53', 'Kingdom of Serbia');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P89', (SELECT id FROM entity WHERE name='Historical Place'), (SELECT id FROM entity WHERE name='Carantania')),
('P89', (SELECT id FROM entity WHERE name='Historical Place'), (SELECT id FROM entity WHERE name='Marcha Orientalis')),
('P89', (SELECT id FROM entity WHERE name='Historical Place'), (SELECT id FROM entity WHERE name='Comitatus Iauntal')),
('P89', (SELECT id FROM entity WHERE name='Historical Place'), (SELECT id FROM entity WHERE name='Kingdom of Serbia'));

------------------------
-- Source translation --
------------------------
INSERT INTO entity (class_code, name, description) VALUES ('E53', 'Source translation', '');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Original Text'), ('E55', 'Translation'), ('E55', 'Transliteration');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Source translation'), (SELECT id FROM entity WHERE name='Original Text')),
('P127', (SELECT id FROM entity WHERE name='Source translation'), (SELECT id FROM entity WHERE name='Translation')),
('P127', (SELECT id FROM entity WHERE name='Source translation'), (SELECT id FROM entity WHERE name='Transliteration'));

-------------------------------
-- Web hierarchies and forms --
-------------------------------
INSERT INTO web.hierarchy (id, name, multiple, system, directional) VALUES
((SELECT id FROM entity WHERE name='License'), 'License', False, True, False),
((SELECT id FROM entity WHERE name='Source'), 'Source', False, True, False),
((SELECT id FROM entity WHERE name='Event'), 'Event', False, True, False),
((SELECT id FROM entity WHERE name='Actor Actor Relation'), 'Actor Actor Relation', False, True, True),
((SELECT id FROM entity WHERE name='Actor Function'), 'Actor Function', False, True, False),
((SELECT id FROM entity WHERE name='Involvement'), 'Involvement', False, True, False),
((SELECT id FROM entity WHERE name='Sex'), 'Sex', False, False, False),
((SELECT id FROM entity WHERE name='Place'), 'Place', False, True, False),
((SELECT id FROM entity WHERE name='Information Carrier'), 'Information Carrier', False, True, False),
((SELECT id FROM entity WHERE name='Bibliography'), 'Bibliography', False, True, False),
((SELECT id FROM entity WHERE name='Edition'), 'Edition', False, True, False),
((SELECT id FROM entity WHERE name='Source translation'), 'Source translation', False, False, False),
((SELECT id FROM entity WHERE name='Administrative Unit'), 'Administrative Unit', True, True, False),
((SELECT id FROM entity WHERE name='Historical Place'), 'Historical Place', True, True, False);

INSERT INTO web.form (name, extendable) VALUES
('File', True),
('Source', True),
('Event', True),
('Person', True),
('Group', True),
('Legal Body', True),
('Place', True),
('Bibliography', True),
('Edition', True),
('Information Carrier', True),
('Actor Actor Relation', False),
('Involvement', False),
('Member', False),
('Source translation', False);

INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
((SELECT id FROM web.hierarchy WHERE name LIKE 'License'),(SELECT id FROM web.form WHERE name LIKE 'File')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Sex'),(SELECT id FROM web.form WHERE name LIKE 'Person')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Source'),(SELECT id FROM web.form WHERE name LIKE 'Source')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Event'),(SELECT id FROM web.form WHERE name LIKE 'Event')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Place'),(SELECT id FROM web.form WHERE name LIKE 'Place')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Administrative Unit'),(SELECT id FROM web.form WHERE name LIKE 'Place')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Historical Place'),(SELECT id FROM web.form WHERE name LIKE 'Place')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Bibliography'),(SELECT id FROM web.form WHERE name LIKE 'Bibliography')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Edition'),(SELECT id FROM web.form WHERE name LIKE 'Edition')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Information Carrier'),(SELECT id FROM web.form WHERE name LIKE 'Information Carrier')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Actor Actor Relation'),(SELECT id FROM web.form WHERE name LIKE 'Actor Actor Relation')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Involvement'),(SELECT id FROM web.form WHERE name LIKE 'Involvement')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Actor Function'),(SELECT id FROM web.form WHERE name LIKE 'Member')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Source translation'),(SELECT id FROM web.form WHERE name LIKE 'Source translation'));
