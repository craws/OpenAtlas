BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.5.0' WHERE name = 'database_version';

-- Add creation event for sources (#2743)
INSERT INTO model.openatlas_class (name, cidoc_class_code, new_types_allowed, write_access_group_name, standard_type_id) VALUES
  ('creation', 'E65', true, 'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1));

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'creation');

-- Remove cidoc_class_code FROM model.entity (#2875)
ALTER TABLE model.entity DROP COLUMN IF EXISTS cidoc_class_code;
DROP FUNCTION IF EXISTS model.delete_entity_related() CASCADE;

CREATE FUNCTION model.delete_entity_related() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            -- Delete aliases
            IF OLD.openatlas_class_name IN ('place', 'person', 'group') THEN
                DELETE FROM model.entity WHERE id IN (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code IN ('P1', 'P131'));
            END IF;

            -- Delete location if it was an artifact, human remains or place
            IF OLD.openatlas_class_name IN ('place', 'human_remains', 'artifact') THEN
                DELETE FROM model.entity WHERE id = (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code = 'P53');
            END IF;

            -- Delete text if it was a document not attached to a source anymore
            IF OLD.openatlas_class_name = 'text' THEN
                DELETE FROM model.entity WHERE id IN (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code = 'P73');
            END IF;

            RETURN OLD;
        END;

    $$;
ALTER FUNCTION model.delete_entity_related() OWNER TO openatlas;
CREATE TRIGGER on_delete_entity BEFORE DELETE ON model.entity FOR EACH ROW EXECUTE FUNCTION model.delete_entity_related();

END;
