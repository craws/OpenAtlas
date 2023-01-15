



BEGIN;

-- #1090 Radiocarbon Dating
UPDATE model.openatlas_class SET name = 'type_tools' WHERE name = 'type_anthropology';
UPDATE web.hierarchy SET category = 'tools' WHERE category = 'anthropology';

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
  ('E55', 'type_tools', 'Radiocarbon', 'Used for radiocarbon dating');

INSERT INTO web.hierarchy (id, name, category, multiple, directional) VALUES
  ((SELECT id FROM model.entity WHERE name='Radiocarbon'), 'Radiocarbon', 'tools', False, False);

END;
