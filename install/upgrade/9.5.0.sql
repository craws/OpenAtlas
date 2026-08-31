BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.5.0' WHERE name = 'database_version';

-- Remove cidoc_class_code FROM model.entity
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
