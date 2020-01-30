-- Upgrade 4.x.x to 4.2.0
-- Be sure to backup the database and read the update notes before executing this!

BEGIN;

-- #1089 Body Parts User Interface
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Human Remains', 'Categories for human remains');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Arm', 'You have to arm yourself!');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Leg', 'One leg is never enough.');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES ('P127', (SELECT id FROM model.entity WHERE name='Human Remains' AND class_code = 'E55'), (SELECT id FROM model.entity WHERE name='Arm'));
INSERT INTO model.link (property_code, range_id, domain_id) VALUES ('P127', (SELECT id FROM model.entity WHERE name='Human Remains' AND class_code = 'E55'), (SELECT id FROM model.entity WHERE name='Leg'));
INSERT INTO web.hierarchy (id, name, multiple, system, directional, value_type) VALUES ((SELECT id FROM model.entity WHERE name='Human Remains' AND class_code = 'E55'), 'Human Remains', False, True, False, False);
INSERT INTO web.form (name, extendable) VALUES ('Human Remains', True);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES ((SELECT id FROM web.hierarchy WHERE name='Human Remains'),(SELECT id FROM web.form WHERE name='Human Remains'));

COMMIT;
