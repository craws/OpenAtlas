-- Upgrade to 3.2.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Delete logged locations from user logs because they are just duplicates from places
DELETE FROM web.user_log WHERE entity_id IN (SELECT id FROM model.entity WHERE system_type = 'place location');

-- License for file upload
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'License', 'Types for a file license');

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

INSERT INTO web.hierarchy (id, name, multiple, system, directional) VALUES ((SELECT id FROM entity WHERE name='License'), 'License', False, True, False);
INSERT INTO web.form (name, extendable) VALUES ('File', True);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES ((SELECT id FROM web.hierarchy WHERE name LIKE 'License'),(SELECT id FROM web.form WHERE name LIKE 'File'));

COMMIT;
