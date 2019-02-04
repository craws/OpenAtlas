-- Upgrade to 3.12.0 to 3.13.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Complete rebuild of date implementation

-- Add new date fields
ALTER TABLE model.entity ADD COLUMN begin_from timestamp without time zone;
ALTER TABLE model.entity ADD COLUMN begin_to timestamp without time zone;
ALTER TABLE model.entity ADD COLUMN begin_comment text;
ALTER TABLE model.entity ADD COLUMN end_from timestamp without time zone;
ALTER TABLE model.entity ADD COLUMN end_to timestamp without time zone;
ALTER TABLE model.entity ADD COLUMN end_comment text;

ALTER TABLE model.link ADD COLUMN begin_from timestamp without time zone;
ALTER TABLE model.link ADD COLUMN begin_to timestamp without time zone;
ALTER TABLE model.link ADD COLUMN begin_comment text;
ALTER TABLE model.link ADD COLUMN end_from timestamp without time zone;
ALTER TABLE model.link ADD COLUMN end_to timestamp without time zone;
ALTER TABLE model.link ADD COLUMN end_comment text;

-- Drop delete trigger, an adapted version will be recreated later
DROP FUNCTION IF EXISTS model.delete_entity_related() CASCADE;

-- Update event dates
UPDATE model.entity e SET begin_from = (
    SELECT value_timestamp FROM model.entity t JOIN model.link l ON l.range_id = t.id AND l.property_code = 'OA5' AND domain_id = e.id AND t.system_type IN ('exact date value', 'from date value')
) WHERE e.class_code IN ('E6', 'E7', 'E8', 'E12');
UPDATE model.entity e SET begin_to = (
    SELECT value_timestamp FROM model.entity t JOIN model.link l ON l.range_id = t.id AND l.property_code = 'OA5' AND domain_id = e.id AND t.system_type = 'to date value'
) WHERE e.class_code IN ('E6', 'E7', 'E8', 'E12');
UPDATE model.entity e SET end_from = (
    SELECT value_timestamp FROM model.entity t JOIN model.link l ON l.range_id = t.id AND l.property_code = 'OA6' AND domain_id = e.id AND t.system_type IN ('exact date value', 'from date value')
) WHERE e.class_code IN ('E6', 'E7', 'E8', 'E12');
UPDATE model.entity e SET end_to = (
    SELECT value_timestamp FROM model.entity t JOIN model.link l ON l.range_id = t.id AND l.property_code = 'OA6' AND domain_id = e.id AND t.system_type = 'to date value')
) WHERE e.class_code IN ('E6', 'E7', 'E8', 'E12');

-- Update involvement dates
UPDATE model.link el SET begin_from = (
    SELECT value_timestamp FROM model.entity t JOIN model.link_property l ON l.range_id = t.id AND l.property_code = 'OA5' AND domain_id = el.id AND t.system_type IN ('exact date value', 'from date value')
) WHERE el.property_code IN ('P11', 'P14', 'P22', 'P23');
UPDATE model.link el SET begin_to = (
    SELECT value_timestamp FROM model.entity t JOIN model.link_property l ON l.range_id = t.id AND l.property_code = 'OA5' AND domain_id = el.id AND t.system_type = 'to date value'
) WHERE el.property_code IN ('P11', 'P14', 'P22', 'P23');
UPDATE model.link el SET end_from = (
    SELECT value_timestamp FROM model.entity t JOIN model.link_property l ON l.range_id = t.id AND l.property_code = 'OA6' AND domain_id = el.id AND t.system_type IN ('exact date value', 'from date value')
) WHERE el.property_code IN ('P11', 'P14', 'P22', 'P23');
UPDATE model.link el SET end_to = (
    SELECT value_timestamp FROM model.entity t JOIN model.link_property l ON l.range_id = t.id AND l.property_code = 'OA6' AND domain_id = el.id AND t.system_type = 'to date value'
) WHERE el.property_code IN ('P11', 'P14', 'P22', 'P23');

-- Drop obsolete fields
ALTER TABLE model.entity DROP COLUMN value_integer;
ALTER TABLE model.entity DROP COLUMN value_timestamp;

-- Delete obsolete OA classes
DELETE FROM model.property WHERE code IN ('OA1', 'OA2', 'OA3', 'OA4', 'OA5', 'OA6');

-- Recreate delete trigger
CREATE FUNCTION model.delete_entity_related() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            -- Delete aliases (P1, P131)
            IF OLD.class_code IN ('E18', 'E21', 'E40', 'E74') THEN
                DELETE FROM model.entity WHERE id IN (
                    SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code IN ('P1', 'P131'));
            END IF;

            -- Delete location (E53) if it was a place or find
            IF OLD.class_code IN ('E18', 'E22') THEN
                DELETE FROM model.entity WHERE id = (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code = 'P53');
            END IF;

            -- Delete translations (E33) if it was a document
            IF OLD.class_code = 'E33' THEN
                DELETE FROM model.entity WHERE id IN (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code = 'P73');
            END IF;

            RETURN OLD;
        END;
    $$;
ALTER FUNCTION model.delete_entity_related() OWNER TO openatlas;
CREATE TRIGGER on_delete_entity BEFORE DELETE ON model.entity FOR EACH ROW EXECUTE PROCEDURE model.delete_entity_related();

COMMIT;
