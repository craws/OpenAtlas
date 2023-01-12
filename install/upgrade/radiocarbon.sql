

-- #1090 Radiocarbon Dating

BEGIN;

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
  ('E55', 'type_anthropology', 'Radiocarbon', 'Used for radiocarbon dating');

INSERT INTO web.hierarchy (id, name, category, multiple, directional) VALUES
  ((SELECT id FROM model.entity WHERE name='Radiocarbon'), 'Radiocarbon', 'anthropology', False, False);

END;
