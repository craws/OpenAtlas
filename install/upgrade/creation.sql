
BEGIN;

-- #2743 Add creation event
INSERT INTO model.openatlas_class (name, cidoc_class_code, new_types_allowed, write_access_group_name, standard_type_id) VALUES
  ('creation', 'E65', true, 'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1));

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'creation');

END;
