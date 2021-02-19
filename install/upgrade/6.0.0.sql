-- Upgrade 5.7.x to 6.0.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- #1456 Artificial objects
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Artificial Object', '');
INSERT INTO model.entity (class_code, name) VALUES ('E55', 'Coin'), ('E55', 'Statue');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM model.entity WHERE name='Artificial Object'), (SELECT id FROM model.entity WHERE name='Coin')),
('P127', (SELECT id FROM model.entity WHERE name='Artificial Object'), (SELECT id FROM model.entity WHERE name='Statue'));

INSERT INTO web.form (name, extendable) VALUES ('Artificial Object', True);
INSERT INTO web.hierarchy (id, name, multiple, standard, directional, value_type, locked) VALUES
((SELECT id FROM model.entity WHERE name='Artificial Object'), 'Artificial Object', False, True, False, False, False);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
((SELECT id FROM web.hierarchy WHERE name='Artificial Object'), (SELECT id FROM web.form WHERE name='Artificial Object'));

-- If you executed above at an upgrade of a development version before use this instead
-- UPDATE model.entity SET name = 'Artifact' WHERE name = 'Artificial Object';
-- UPDATE model.entity SET system_type = 'artifact' WHERE system_type = 'artificial object';
-- UPDATE web.form SET name = 'Artifact' WHERE name = 'Artificial Object';

-- #1091 Reference systems for types
INSERT INTO web.form (name, extendable) VALUES ('Type', True);

END;
