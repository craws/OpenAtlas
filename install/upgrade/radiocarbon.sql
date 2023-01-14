



BEGIN;

-- #1090 Radiocarbon Dating
UPDATE model.entity SET name = 'type_tools'
INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
  ('E55', 'type_anthropology', 'Radiocarbon', 'Used for radiocarbon dating');

UPDATE web.hierarchy SET category = 'tools' WHERE category = 'anthropology';
INSERT INTO web.hierarchy (id, name, category, multiple, directional) VALUES
  ((SELECT id FROM model.entity WHERE name='Radiocarbon'), 'Radiocarbon', 'tools', False, False);

END;
