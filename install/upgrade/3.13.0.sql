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


-- Persons, Groups appears first without place (718)
CREATE FUNCTION model.update_actors() RETURNS void
    LANGUAGE plpgsql
    AS $$DECLARE

    start_time timestamp;
    end_time timestamp;
    delta double precision;

    actor RECORD;
    new_event_id int;

    begin_from_id int;
    begin_from_date timestamp;
    begin_to_id int;
    begin_to_date timestamp;
    begin_property text;
    begin_desc text;
    begin_place_id int;

    end_from_id int;
    end_from_date timestamp;
    end_to_id int;
    end_to_date timestamp;
    end_property text;
    end_desc text;
    end_place_id int;

    count_actor_birth int;
    count_actor_begin_and_place int;
    count_actor_begin int;
    count_actor_begin_place int;
    count_actor_no_begin_data_or_place int;
    count_actor_death int;
    count_actor_end_and_place int;
    count_actor_end int;
    count_actor_end_place int;
    count_actor_no_end_data_or_place int;

BEGIN

start_time := clock_timestamp();
count_actor_birth = 0;
count_actor_begin_and_place = 0;
count_actor_begin = 0;
count_actor_begin_place = 0;
count_actor_no_begin_data_or_place = 0;
count_actor_death = 0;
count_actor_end_and_place = 0;
count_actor_end = 0;
count_actor_end_place = 0;
count_actor_no_end_data_or_place = 0;

RAISE NOTICE 'Begin Loop';
FOR actor IN SELECT id, name FROM model.entity WHERE class_code IN ('E21', 'E40', 'E74') LOOP

    -- Begin from
    SELECT t.id, t.value_timestamp, t.description, l.property_code INTO begin_from_id, begin_from_date, begin_desc, begin_property FROM model.link l
    JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code IN ('OA1', 'OA3') AND e.system_type IN ('exact date value', 'from date value')
    JOIN model.entity t ON l.range_id = t.id;

    -- Begin to
    IF begin_from_date IS NOT NULL THEN
        SELECT t.id, t.value_timestamp INTO begin_to_id, begin_to_date FROM model.link l
        JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code IN ('OA1', 'OA3') AND e.system_type = 'to date value'
        JOIN model.entity t ON l.range_id = t.id;
    END IF;

    -- Begin place
    SELECT l.range_id INTO begin_place_id FROM model.link l
    JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code = 'OA8' AND l.domain_id = actor.id;

    -- End from
    SELECT t.id, t.value_timestamp, t.description, l.property_code INTO end_from_id, end_from_date, end_desc, end_property FROM model.link l
    JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code IN ('OA2', 'OA4') AND e.system_type IN ('exact date value', 'from date value')
    JOIN model.entity t ON l.range_id = t.id;

    -- End to
    IF end_from_date IS NOT NULL THEN
        SELECT t.id, t.value_timestamp INTO end_to_id, end_to_date FROM model.link l
        JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code IN ('OA2', 'OA4') AND e.system_type = 'to date value'
        JOIN model.entity t ON l.range_id = t.id;
    END IF;

    -- End place
    SELECT l.range_id INTO end_place_id FROM model.link l
    JOIN model.entity e ON l.domain_id = actor.id AND l.range_id = e.id AND l.property_code = 'OA9' AND l.domain_id = actor.id;

    -- Update begin of actors
    IF begin_property = 'OA3' THEN
        -- If birth: move dates to entities
        UPDATE model.entity SET begin_from = begin_from_date, begin_to = begin_to_date, begin_comment = begin_desc WHERE id = actor.id;
        IF begin_place_id IS NOT NULL THEN
            -- If place move place to an event
            INSERT INTO model.entity (class_code, name) VALUES ('E7', 'Appearance of ' || actor.name) RETURNING id INTO new_event_id;
            INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P7', begin_place_id);
            INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        END IF;
        count_actor_birth := count_actor_birth + 1;
    ELSEIF begin_from_id IS NOT NULL AND begin_place_id IS NOT NULL THEN
        -- IF first appearance date and place create an event with both
        INSERT INTO model.entity (class_code, name, begin_from, begin_to, begin_comment) VALUES ('E7', 'Appearance of ' || actor.name, begin_from_date, begin_to_date, begin_desc) RETURNING id INTO new_event_id;
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P7', begin_place_id);
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        count_actor_begin_and_place := count_actor_begin_and_place + 1;
    ELSEIF begin_from_id IS NOT NULL THEN
        -- IF begin_from create an event for for it
        INSERT INTO model.entity (class_code, name, begin_from, begin_to, begin_comment) VALUES ('E7', 'Appearance of ' || actor.name, begin_from_date, begin_to_date, begin_desc) RETURNING id INTO new_event_id;
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        count_actor_begin := count_actor_begin + 1;
    ELSEIF begin_place_id IS NOT NULL THEN
        -- IF begin_place create an event for it
        INSERT INTO model.entity (class_code, name) VALUES ('E7', 'Appearance of ' || actor.name) RETURNING id INTO new_event_id;
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P7', begin_place_id);
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        count_actor_begin_place := count_actor_begin_place + 1;
    ELSE
        count_actor_no_begin_data_or_place := count_actor_no_begin_data_or_place + 1;
    END IF;

    -- Update end of actors
    IF end_property = 'OA4' THEN
        -- If death: move dates to entities
        UPDATE model.entity SET end_from = end_from_date, end_to = end_to_date, end_comment = end_desc WHERE id = actor.id;
        IF end_place_id IS NOT NULL THEN
            -- If place move place to an event
            INSERT INTO model.entity (class_code, name) VALUES ('E7', 'Appearance of ' || actor.name) RETURNING id INTO new_event_id;
            INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P7', end_place_id);
            INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        END IF;
        count_actor_death := count_actor_death + 1;
    ELSEIF end_from_id IS NOT NULL AND end_place_id IS NOT NULL THEN
        -- IF first appearance date and place create an event with both
        INSERT INTO model.entity (class_code, name, end_from, end_to, end_comment) VALUES ('E7', 'Appearance of ' || actor.name, end_from_date, end_to_date, end_desc) RETURNING id INTO new_event_id;
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P7', end_place_id);
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        count_actor_end_and_place := count_actor_end_and_place + 1;
    ELSEIF end_from_id IS NOT NULL THEN
        -- IF end_from create an event for for it
        INSERT INTO model.entity (class_code, name, end_from, end_to, end_comment) VALUES ('E7', 'Appearance of ' || actor.name, end_from_date, end_to_date, end_desc) RETURNING id INTO new_event_id;
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        count_actor_end := count_actor_end + 1;
    ELSEIF end_place_id IS NOT NULL THEN
        -- IF end_place create an event for it
        INSERT INTO model.entity (class_code, name) VALUES ('E7', 'Appearance of ' || actor.name) RETURNING id INTO new_event_id;
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P7', end_place_id);
        INSERT INTO model.link (domain_id, property_code, range_id) VALUES (new_event_id, 'P11', actor.id);
        count_actor_end_place := count_actor_end_place + 1;
    ELSE
        count_actor_no_end_data_or_place := count_actor_no_end_data_or_place + 1;
    END IF;

END LOOP;

RAISE NOTICE 'Actor: % birth, % begin date and place, % begin date, % begin place, % no begin date or place', count_actor_birth, count_actor_begin_and_place, count_actor_begin, count_actor_begin_place, count_actor_no_begin_data_or_place;
RAISE NOTICE 'Actor: % death, % end date and place, % end date, % end place, % no end date or place', count_actor_death, count_actor_end_and_place, count_actor_end, count_actor_end_place, count_actor_no_end_data_or_place;

end_time := clock_timestamp();
delta := extract(epoch from end_time) - extract(epoch from start_time);
RAISE NOTICE 'Runtime seconds=%', delta;

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

-- Delete former place links
DELETE FROM model.link WHERE link.property_code IN ('OA8', 'OA9');

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
