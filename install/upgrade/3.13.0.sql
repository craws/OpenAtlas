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

-------------------------------
-- Below is work in progress --
-------------------------------

-- Persons, Groups appears first with place (578)
SELECT t.value_timestamp, e.id, pl.id
FROM model.entity t
JOIN model.link tl ON t.id = tl.range_id AND tl.property_code = 'OA1' AND t.system_type IN ('exact date value', 'from date value')
JOIN model.entity e ON tl.domain_id = e.id AND e.class_code IN ('E21', 'E74')
JOIN model.link pl ON e.id = pl.domain_id AND pl.property_code = 'OA8'

-- Persons, Groups appears first without place (718)
CREATE FUNCTION model.update_actors() RETURNS integer
    LANGUAGE plpgsql
    AS $$DECLARE
    actor RECORD;
    begin_from_id int;
    begin_to_id int;
    begin_property text;
    begin_place_id int;
    end_from_id int;
    end_to_id int;
    end_property text;
    end_place_id int;
BEGIN
RAISE NOTICE 'Begin Loop';
FOR actor IN SELECT id, name FROM model.entity WHERE class_code IN ('E21', 'E40', 'E74') LOOP

    -- begin from
    SELECT l.range_id, l.property_code INTO begin_from_id, begin_property FROM model.link l
    JOIN model.entity e ON l.range_id = e.id AND l.property_code IN ('OA1', 'OA3') AND e.system_type IN ('exact date value', 'from date value')
    WHERE l.domain_id = actor.id;

    -- begin to
    IF begin_from_id IS NOT NULL THEN
        SELECT l.range_id INTO begin_to_id FROM model.link l
        JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code IN ('OA1', 'OA3') AND e.system_type = 'to date value';
    END IF;

    -- begin place
    SELECT l.range_id INTO begin_place_id FROM model.link l
    JOIN model.entity e ON l.range_id = e.id AND l.property_code = 'OA8' AND l.domain_id = actor.id
    WHERE l.domain_id = actor.id;

    -- end from
    SELECT l.range_id, l.property_code INTO end_from_id, end_property FROM model.link l
    JOIN model.entity e ON l.range_id = e.id AND l.property_code IN ('OA2', 'OA4') AND e.system_type IN ('exact date value', 'from date value')
    WHERE l.domain_id = actor.id;

    -- end to
    IF end_from_id IS NOT NULL THEN
        SELECT l.range_id INTO end_to_id FROM model.link l
        JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code IN ('OA2', 'OA4') AND e.system_type = 'to date value';
    END IF;

    -- end place
    SELECT l.range_id INTO end_place_id FROM model.link l
    JOIN model.entity e ON l.range_id = e.id AND l.property_code = 'OA9' AND l.domain_id = actor.id
    WHERE l.domain_id = actor.id;

    IF begin_from_id IS NOT NULL AND begin_to_id IS NOT NULL AND begin_place_id IS NOT NULL THEN
        RAISE NOTICE 'actor.id: (%)', actor.id;
        RAISE NOTICE 'begin_from: (%) begin_property: (%), begin_to: (%), begin_place_id (%)', begin_from_id, begin_property, begin_to_id, begin_place_id;
        RAISE NOTICE 'end_from: (%) end_property: (%), end_to: (%), end_place_id (%)', end_from_id, end_property, end_to_id, end_place_id;
    END IF;
END LOOP;
RETURN 1;
END;$$;
ALTER FUNCTION model.update_actors() OWNER TO openatlas;

-- Update event dates
-- To do: descriptions
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
-- To do: descriptions
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
