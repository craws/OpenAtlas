-- Upgrade to 3.3.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Add system_type place to existing places
UPDATE model.entity SET system_type = 'place' WHERE class_code = 'E18';

-- Add types for subunits
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Feature', '');
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Stratigraphical Unit', '');
INSERT INTO entity (class_code, name, description) VALUES ('E55', 'Find', '');

INSERT INTO web.hierarchy (id, name, multiple, system, directional) VALUES
((SELECT id FROM entity WHERE name='Feature'), 'Feature', False, True, False),
((SELECT id FROM entity WHERE name='Stratigraphical Unit'), 'Stratigraphical Unit', False, True, False),
((SELECT id FROM entity WHERE name='Find'), 'Find', False, True, False);

INSERT INTO web.form (name, extendable) VALUES
('Feature', True),
('Stratigraphical Unit', True),
('Find', True);

COMMIT;
