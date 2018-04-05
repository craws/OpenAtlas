-- Upgrade to 3.3.0, be sure to backup the database and read the update notes before executing this!

SET search_path = model;
BEGIN;

-- Add system_type place to existing places
UPDATE model.entity SET system_type = 'place' WHERE class_code = 'E18';

-- Add archaeological types

INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Feature', 'Classification of the archaeological feature e.g. grave, pit, ...');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Grave'), ('E55', 'Pit');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Feature'), (SELECT id FROM entity WHERE name='Grave')),
('P127', (SELECT id FROM entity WHERE name='Feature'), (SELECT id FROM entity WHERE name='Pit'));

INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Stratigraphical Unit', 'Classification of the archaeological SU e.g. burial, deposit, ...');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Burial'), ('E55', 'Deposit');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Stratigraphical Unit'), (SELECT id FROM entity WHERE name='Burial')),
('P127', (SELECT id FROM entity WHERE name='Stratigraphical Unit'), (SELECT id FROM entity WHERE name='Deposit'));

INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Find', 'Classification of the archaeological find e.g. weapon, jewellery ...');
INSERT INTO entity (class_code, name) VALUES ('E55', 'Weapon'), ('E55', 'Jewellery');
INSERT INTO link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM entity WHERE name='Find'), (SELECT id FROM entity WHERE name='Weapon')),
('P127', (SELECT id FROM entity WHERE name='Find'), (SELECT id FROM entity WHERE name='Jewellery'));

INSERT INTO web.hierarchy (id, name, multiple, system, directional) VALUES
((SELECT id FROM entity WHERE name='Feature'), 'Feature', False, True, False),
((SELECT id FROM entity WHERE name='Stratigraphical Unit'), 'Stratigraphical Unit', False, True, False),
((SELECT id FROM entity WHERE name='Find'), 'Find', False, True, False);

INSERT INTO web.form (name, extendable) VALUES ('Feature', True), ('Stratigraphical Unit', True), ('Find', True);

INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
((SELECT id FROM web.hierarchy WHERE name LIKE 'Feature'),(SELECT id FROM web.form WHERE name LIKE 'Feature')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Stratigraphical Unit'),(SELECT id FROM web.form WHERE name LIKE 'Stratigraphical Unit')),
((SELECT id FROM web.hierarchy WHERE name LIKE 'Find'),(SELECT id FROM web.form WHERE name LIKE 'Find'));

COMMIT;
