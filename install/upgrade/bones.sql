BEGIN;

-- Feature: Bone inventory (#1473)

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_tools', 'Bone preservation'),
    ('E55', 'type_tools', 'absent'),
    ('E55', 'type_tools', 'less than 25%'),
    ('E55', 'type_tools', '25-75%'),
    ('E55', 'type_tools', '75-99%'),
    ('E55', 'type_tools', '100%');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='absent'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='less than 25%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='25-75%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='75-99%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='100%'), (SELECT id FROM model.entity WHERE name='Bone preservation'));

END;
