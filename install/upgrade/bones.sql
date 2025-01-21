BEGIN;

-- Feature: Bone inventory (#1473)

INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_allowed, reference_system_allowed, new_types_allowed, write_access_group_name, layout_color, layout_icon, standard_type_id) VALUES
  ('bone',          'E20',  false, true,  true,  'contributor', NULL, 'mdi-map-marker',   NULL);


INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_tools', 'Bone preservation'),
    ('E55', 'type_tools', '0%'),
    ('E55', 'type_tools', '1-24%'),
    ('E55', 'type_tools', '25-74%'),
    ('E55', 'type_tools', '75-99%'),
    ('E55', 'type_tools', '100%');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='0%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='1-24%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='25-74%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='75-99%'), (SELECT id FROM model.entity WHERE name='Bone preservation')),
    ('P127', (SELECT id FROM model.entity WHERE name='100%'), (SELECT id FROM model.entity WHERE name='Bone preservation'));

INSERT INTO web.hierarchy (id, name, category, multiple, directional) VALUES
  ((SELECT id FROM model.entity WHERE name='Bone preservation'), 'Bone preservation', 'tools', False, False);

END;
